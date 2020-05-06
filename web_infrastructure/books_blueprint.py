from flask import Blueprint, render_template, redirect, request
from flask_login import current_user, login_required

from data import db_session
from data.db_session import Book, Author, Genre
from data.db_functions import generate_random_filename, get_image_by_book, set_image_by_book

from web_infrastructure.forms_models import BookForm, DeleteBookForm

import os


blueprint = Blueprint(__name__, 'books_blueprint', template_folder='templates')


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

        author = session.query(Author).get(form.author.data)
        genre = session.query(Genre).get(form.genre.data)
        if not author or author.status != 1:
            return render_template(**template_params,
                                   message="Некорректный ID автора")
        if not genre or genre.status != 1:
            return render_template(**template_params,
                                   message="Некорректный ID жанра")

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


@blueprint.route('/delete_book/<int:book_id>', methods=['GET', 'POST'])
@login_required
def delete_book(book_id):
    session = db_session.create_session()
    book = session.query(Book).get(book_id)

    if book and ((book.user == current_user and book.status == -1) or current_user.is_moderator):
        form = DeleteBookForm()
        template_params = {
            'template_name_or_list': 'delete_book.html',
            'title': 'Удаление книги',
            'form': form,
            'book': book,
            'to_redirect': request.args.get('from', default='/my', type=str)
        }

        if not form.validate_on_submit():
            return render_template(**template_params)
        session.delete(book)
        session.commit()
    return redirect(request.args.get('from', default='/my', type=str))
