import flask
from flask import Blueprint, request, render_template, redirect
from flask_login import login_user, logout_user, current_user, login_required


from data import db_session
from data.db_session import User
from data.forms_models import RegisterForm, LoginForm


blueprint = Blueprint(__name__, 'web', template_folder='templates')


@blueprint.route('/')
def main():
    return render_template('base.html', title='Администрирование ботов')


@blueprint.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect('/')

    form = RegisterForm()
    if form.validate_on_submit():
        if form.password.data != form.password_again.data:
            return render_template('register.html', title="Регистрация",
                                   form=form, message="Пароли не совпадают")

        session = db_session.create_session()
        if session.query(User).filter(User.email == form.email.data).first():
            return render_template('register.html', form=form, title="Регистрация",
                                   message="Пользователь с таким e-mail уже существует")

        user = User(email=form.email.data)
        user.set_password(form.password.data)
        session.add(user)
        session.commit()

        return redirect('/')
    return render_template('register.html', title="Регистрация", form=form)


@blueprint.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect('/')

    form = LoginForm()
    if form.validate_on_submit():
        session = db_session.create_session()
        user = session.query(User).filter(User.email == form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user)
            return redirect('/')
        return render_template('login.html',
                               message="Неправильный e-mail или пароль",
                               form=form)
    return render_template('login.html', title="Авторизация", form=form)


@blueprint.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect('/')
