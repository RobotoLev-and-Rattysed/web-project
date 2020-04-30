from flask import Blueprint, render_template, redirect
from flask_login import login_user, logout_user, current_user, login_required


from data import db_session
from data.db_session import User, Book, Author, Genre
from web_infrastructure.forms_models import RegisterForm, LoginForm, AddBookForm


blueprint = Blueprint(__name__, 'web', template_folder='templates')


@blueprint.route('/')
def main():
    return render_template('greeting.html', title='Электронная библиотека')


@blueprint.route('/books')
def all_books():
    session = db_session.create_session()
    books = session.query(Book).filter(Book.id <= 10)
    return render_template('books.html', title='Популярные книги', books=books)


@blueprint.route('/my')
@login_required
def my_books():
    return render_template('books.html', title='Мои книги', books=current_user.books)


@blueprint.route('/new_book', methods=['GET', 'POST'])
@login_required
def add_book():
    session = db_session.create_session()
    form = AddBookForm()

    template_params = {
        'template_name_or_list': 'new_book.html',
        'form': form,
        'title': 'Добавление книги'
    }

    if form.validate_on_submit():
        session = db_session.create_session()
        if not session.query(Author).get(form.author.data):
            return render_template(**template_params,
                                   message="Такого автора нет в базе")
        if not session.query(Genre).get(form.genre.data):
            return render_template(**template_params,
                                   message="Такого жанра нет в базе")

        session.add(Book(
            user_id=current_user.id,
            name=form.name.data,
            author_id=form.author.data,
            genre_id=form.genre.data,
            description=form.description.data
        ))
        session.commit()

        return redirect('/my')
    return render_template(**template_params)


# <---Регистрация и авторизация--->


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
        if session.query(User).filter(User.nickname == form.nickname.data).first():
            return render_template('register.html', form=form, title="Регистрация",
                                   message="Пользователь с таким ником уже существует")

        user = User(email=form.email.data,
                    nickname=form.nickname.data)
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
