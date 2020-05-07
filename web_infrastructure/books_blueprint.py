from flask import Blueprint, render_template, redirect, request, send_file
from flask_login import current_user, login_required

from data import db_session
from data.db_session import User, Book, Author, Genre
from data.db_functions import *

from web_infrastructure.forms_models import RegisterForm, LoginForm, BookForm, DeleteForm

import os
import os.path

import wikipedia
from PIL import Image

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
        'show_edit_booleans': False
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

        description = wiki_description(form.description.data,
                                       form.name.data,
                                       author.name,
                                       genre.name)

        book = Book(
            user_id=current_user.id,
            name=form.name.data,
            author_id=form.author.data,
            genre_id=form.genre.data,
            description=description
        )

        if not handle_text(form, book, template_params):
            return render_template(**template_params)
        if not handle_image(form, book, template_params):
            return render_template(**template_params)

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
            'show_edit_booleans': True
        }

        if form.validate_on_submit():
            author = session.query(Author).get(form.author.data)
            genre = session.query(Genre).get(form.genre.data)
            if not author or author.status != 1:
                return render_template(**template_params,
                                       message="Некорректный ID автора")
            if not genre or genre.status != 1:
                return render_template(**template_params,
                                       message="Некорректный ID жанра")

            description = wiki_description(form.description.data,
                                           form.name.data,
                                           author.name,
                                           genre.name)

            book.name = form.name.data
            book.author_id = form.author.data
            book.genre_id = form.genre.data
            book.description = description

            if not handle_text(form, book, template_params):
                return render_template(**template_params)
            if not handle_image(form, book, template_params):
                return render_template(**template_params)

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
        form = DeleteForm()
        template_params = {
            'template_name_or_list': 'delete_element.html',
            'title': 'Удаление книги',
            'text': f'Подтвердите удаление книги id{book.id} "{book.name}" '
                    f'({book.author.name}, {book.genre.name}) [by {book.user.nickname}].',
            'form': form,
            'to_redirect': request.args.get('from', default='/my', type=str)
        }

        if not form.validate_on_submit():
            return render_template(**template_params)
        session.delete(book)
        session.commit()
    return redirect(request.args.get('from', default='/my', type=str))


@blueprint.route('/download/<int:book_id>')
def downloader(book_id):
    session = db_session.create_session()
    book = session.query(Book).get(book_id)

    if not book or (not current_user.is_moderator and book.status != 1):
        return redirect('/books')

    return send_file(os.path.abspath(os.path.join(__name__, '..' + get_text_by_book(book))),
                     as_attachment=True)


def wiki_description(description, book_name, author_name, genre_name):
    if description == '':
        wikipedia.set_lang('ru')

        search_text = f'{author_name} {book_name} {genre_name}'
        results = wikipedia.search(search_text)
        if not results:
            description = "Описание отсутствует"
        else:
            page = wikipedia.page(results[0])
            description = page.content[:500] + "..."

    return description


def handle_image(form, book, template_params):
    if not form.edit_image.data:
        return True

    filename = form.image.data.filename
    if filename and filename.split('.')[-1] != 'jpg':
        template_params['message'] = 'Принимаются только картинки с расширением .jpg'
        return False

    if filename:
        local_filename = generate_random_filename(extension='.jpg')
        abspath = os.path.abspath(
            os.path.join(__file__, f'../../static/img/books/{local_filename}'))
        form.image.data.save(abspath)

        im = Image.open(abspath)
        width, height = im.size
        if not (300 <= width <= 900 and 300 <= height <= 900):
            template_params['message'] = 'Размеры картинок должны быть от 300 до 900 пикселей'
            return False
    else:
        local_filename = 'no_image.jpg'

    set_image_by_book(book, local_filename)
    return True


def handle_text(form, book, template_params):
    if template_params['show_edit_booleans'] and not form.edit_text.data:
        return True

    filename = form.text.data.filename
    if not filename:
        template_params['message'] = 'Нельзя создать книгу без текста'
        return False
    if filename.split('.')[-1] not in '.txt':
        template_params['message'] = 'Принимаются только тексты с расширением .txt'
        return False

    local_filename = f"ieb-book_{book.name}_{generate_random_filename(extension='.txt')}"
    abspath = os.path.abspath(
        os.path.join(__file__, f'../../static/txt/books/{local_filename}'))
    form.text.data.save(abspath)

    set_text_by_book(book, local_filename)
    return True
