from flask import Blueprint, render_template, redirect
from flask_login import login_user, logout_user, current_user, login_required

from data import db_session
from data.db_session import User

from web_infrastructure.forms_models import RegisterForm, LoginForm


blueprint = Blueprint(__name__, 'users_blueprint', template_folder='templates')


@blueprint.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect('/')

    form = RegisterForm()
    template_params = {
        'template_name_or_list': 'register.html',
        'form': form,
        'title': 'Регистрация'
    }

    if form.validate_on_submit():
        if form.password.data != form.password_again.data:
            return render_template(**template_params, message="Пароли не совпадают")

        session = db_session.create_session()
        if session.query(User).filter(User.email == form.email.data).first():
            return render_template(**template_params,
                                   message="Пользователь с таким e-mail уже существует")
        if session.query(User).filter(User.nickname == form.nickname.data).first():
            return render_template(**template_params,
                                   message="Пользователь с таким ником уже существует")

        user = User(email=form.email.data,
                    nickname=form.nickname.data)
        user.set_password(form.password.data)
        session.add(user)
        session.commit()

        return redirect('/')
    return render_template(**template_params, )


@blueprint.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect('/')

    form = LoginForm()
    template_params = {
        'template_name_or_list': 'login.html',
        'form': form,
        'title': 'Авторизация'
    }

    if form.validate_on_submit():
        session = db_session.create_session()
        user = session.query(User).filter(User.email == form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user)
            return redirect('/')
        return render_template(**template_params, message="Неправильный e-mail или пароль")
    return render_template(**template_params)


@blueprint.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect('/')
