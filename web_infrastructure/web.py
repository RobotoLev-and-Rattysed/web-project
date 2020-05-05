from flask import Blueprint, render_template, redirect, request, abort
from flask_login import login_user, logout_user, current_user, login_required

from data import db_session
from data.db_session import User, Book, Author, Genre
from data.db_functions import generate_random_filename, get_image_by_book, set_image_by_book

from web_infrastructure.forms_models import RegisterForm, LoginForm, BookForm

import os.path


blueprint = Blueprint(__name__, 'web', template_folder='templates')


# <---Главная страница--->


@blueprint.route('/')
def main():
    return render_template('greeting.html', title='Электронная библиотека')


# <---Все о книгах--->


@blueprint.route('/books')
def all_books():
    session = db_session.create_session()
    # books = session.query(Book).filter(Book.id <= 10)
    books = session.query(Book).filter(Book.status == 1).order_by(Book.id).all()
    return render_template('books.html', title='Все книги', books=books, current_address='/books')


@blueprint.route('/my')
@login_required
def my_books():
    session = db_session.create_session()
    books = session.query(Book).filter(Book.user == current_user).order_by(Book.id).all()
    return render_template('books.html', title='Мои книги', books=books, my_books=True,
                           current_address='/my')


@blueprint.route('/book/<int:book_id>')
def one_book(book_id):
    session = db_session.create_session()
    template_params = {
        'template_name_or_list': 'one_book.html',
        'title': f'Книга id{book_id}'
    }

    book = session.query(Book).get(book_id)
    image_url = get_image_by_book(book)
    return render_template(**template_params, book=book, image_url=image_url)


@blueprint.route('/new_book', methods=['GET', 'POST'])
@login_required
def new_book():
    form = BookForm()

    template_params = {
        'template_name_or_list': 'new_book.html',
        'form': form,
        'title': 'Добавление книги',
        'show_edit_image': False
    }

    if form.validate_on_submit():
        session = db_session.create_session()
        if not session.query(Author).get(form.author.data):
            return render_template(**template_params,
                                   message="Такого автора нет в базе")
        if not session.query(Genre).get(form.genre.data):
            return render_template(**template_params,
                                   message="Такого жанра нет в базе")

        book = Book(
            user_id=current_user.id,
            name=form.name.data,
            author_id=form.author.data,
            genre_id=form.genre.data,
            description=form.description.data
        )

        filename = form.image.data.filename
        if filename and filename.split('.')[-1] != 'jpg':
            template_params['message'] = 'Принимаются только картинки с расширением .jpg'
            return render_template(**template_params)

        if filename:
            local_filename = generate_random_filename(extension='.jpg')
            form.image.data.save(os.path.abspath(
                os.path.join(__file__, f'../../static/img/books/{local_filename}')))
            set_image_by_book(book, local_filename)

        session.add(book)
        session.commit()

        return redirect('/my')
    return render_template(**template_params)


@blueprint.route('/edit_book/<int:book_id>', methods=['GET', 'POST'])
@login_required
def edit_book(book_id):
    session = db_session.create_session()
    form = BookForm()

    book = session.query(Book).get(book_id)
    if not book:
        return redirect('/my')

    if (book.user == current_user and book.status == -1) or current_user.is_moderator:
        template_params = {
            'template_name_or_list': 'new_book.html',
            'form': form,
            'title': 'Редактирование книги',
            'show_edit_image': True
        }

        if form.validate_on_submit():
            if not session.query(Author).get(form.author.data):
                return render_template(**template_params,
                                       message="Такого автора нет в базе")
            if not session.query(Genre).get(form.genre.data):
                return render_template(**template_params,
                                       message="Такого жанра нет в базе")

            book.name = form.name.data
            book.author_id = form.author.data
            book.genre_id = form.genre.data
            book.description = form.description.data

            if form.edit_image.data:
                filename = form.image.data.filename
                if filename and filename.split('.')[-1] != 'jpg':
                    template_params['message'] = 'Принимаются только картинки с расширением .jpg'
                    return render_template(**template_params)

                if filename:
                    local_filename = generate_random_filename(extension='.jpg')
                    form.image.data.save(os.path.abspath(
                        os.path.join(__file__, f'../../static/img/books/{local_filename}')))
                    set_image_by_book(book, local_filename)
                else:
                    book.image = None
                    book.image_name = 'no_image.jpg'

            session.add(book)
            session.commit()

            return redirect(request.args.get('from', default='/my', type=str))

        form.name.data = book.name
        form.author.data = book.author_id
        form.genre.data = book.genre_id
        form.description.data = book.description

        return render_template(**template_params)
    return redirect('/my')


@blueprint.route('/requests/<string:requests_type>')
@login_required
def get_requests(requests_type):
    if not current_user.is_moderator:
        return redirect('/my')

    session = db_session.create_session()
    template_params = {
        'template_name_or_list': 'books.html',
        'current_address': f'/requests/{requests_type}'
    }

    books = None
    if requests_type == 'all':
        books = session.query(Book).filter(Book.status < 1).order_by(Book.id).all()
        template_params['title'] = 'Все заявки'
    elif requests_type == 'active':
        books = session.query(Book).filter(Book.status == 0).order_by(Book.id).all()
        template_params['title'] = 'Активные заявки'
    elif requests_type == 'rejected':
        books = session.query(Book).filter(Book.status == -1).order_by(Book.id).all()
        template_params['title'] = 'Отклоненные заявки'
    else:
        abort(404)

    template_params['books'] = books
    return render_template(**template_params)


@blueprint.route('/request/<int:request_id>/<string:new_request_status>')
@login_required
def request_action(request_id, new_request_status):
    if not current_user.is_moderator:
        return redirect('/my')

    session = db_session.create_session()
    book = session.query(Book).get(request_id)

    if (book and
            (new_request_status.isdigit() or
             (new_request_status[0] == '-' and new_request_status[1:].isdigit()))
            and -1 <= int(new_request_status) <= 1):
        book.status = int(new_request_status)
        print(int(new_request_status))
        session.commit()

    return redirect(request.args.get('from', default='/my', type=str))


# <---Регистрация и авторизация--->


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
