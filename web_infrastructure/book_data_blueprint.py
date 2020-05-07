from flask import Blueprint, render_template, redirect, request
from flask_login import current_user, login_required

from data import db_session
from data.db_session import Author, Genre

from web_infrastructure.forms_models import GenreForm, AuthorForm, DeleteForm


blueprint = Blueprint(__name__, 'book_data_blueprint', template_folder='templates')


@blueprint.route('/book_data/<string:type_of_sorting>')
@login_required
def all_genres(type_of_sorting):
    if type_of_sorting not in {'all', 'my', 'requests'}:
        return redirect('/book_data/all')
    if type_of_sorting == 'requests' and not current_user.is_moderator:
        return redirect('/book/all')

    session = db_session.create_session()
    template_params = {
        'template_name_or_list': 'book_data.html'
    }

    if type_of_sorting == 'all':
        template_params['title'] = 'Общедоступные данные для книг'
        template_params['authors'] = session.query(Author).filter(
            Author.status == 1
        ).order_by(Author.id).all()
        template_params['genres'] = session.query(Genre).filter(
            Genre.status == 1
        ).order_by(Genre.id).all()
        template_params['current_address'] = '/book_data/all'
    elif type_of_sorting == 'my':
        template_params['title'] = 'Добавленные мной данные для книг'
        template_params['authors'] = session.query(Author).filter(
            Author.user == current_user
        ).order_by(Author.id).all()
        template_params['genres'] = session.query(Genre).filter(
            Genre.user == current_user
        ).order_by(Genre.id).all()
        template_params['current_address'] = '/book_data/my'
        template_params['my_book_data'] = True
    else:
        template_params['title'] = 'Заявки данных для книг'
        template_params['authors'] = session.query(Author).filter(
            Author.status < 1
        ).order_by(Author.id).all()
        template_params['genres'] = session.query(Genre).filter(
            Genre.status < 1
        ).order_by(Genre.id).all()
        template_params['current_address'] = '/book_data/requests'

    return render_template(**template_params)


@blueprint.route('/new_author', methods=['GET', 'POST'])
@login_required
def new_author():
    form = AuthorForm()

    template_params = {
        'template_name_or_list': 'author_or_genre.html',
        'form': form,
        'title': 'Добавление автора'
    }

    if form.validate_on_submit():
        session = db_session.create_session()

        author = Author(
            user_id=current_user.id,
            name=form.name.data
        )

        session.add(author)
        session.commit()

        return redirect('/book_data/my')
    return render_template(**template_params)


@blueprint.route('/edit_author/<int:author_id>', methods=['GET', 'POST'])
@login_required
def edit_author(author_id):
    session = db_session.create_session()
    author = session.query(Author).get(author_id)

    if not author:
        return redirect('/book_data/all')

    form = AuthorForm()
    template_params = {
        'template_name_or_list': 'author_or_genre.html',
        'title': f'Редактирование автора id{author_id} ({author.name})',
        'form': form,
    }

    if (author.user == current_user and author.status == -1) or current_user.is_moderator:
        if not form.validate_on_submit():
            form.name.data = author.name
            return render_template(**template_params)

        author.name = form.name.data
        if not current_user.is_moderator:
            author.status = 0
        session.commit()
    return redirect(request.args.get('from', default='/book_data/my', type=str))


@blueprint.route('/delete_author/<int:author_id>', methods=['GET', 'POST'])
@login_required
def delete_author(author_id):
    session = db_session.create_session()
    author = session.query(Author).get(author_id)

    if not author or len(author.books) > 0:
        return redirect('/book_data/my')

    if (author.user == current_user and author.status == -1) or current_user.is_moderator:
        form = DeleteForm()

        template_params = {
            'template_name_or_list': 'delete_element.html',
            'title': 'Удаление автора',
            'text': f'Подтвердите удаление автора id{author.id} "{author.name}".',
            'form': form,
            'to_redirect': request.args.get('from', default='/book_data/my', type=str)
        }

        if not form.validate_on_submit():
            return render_template(**template_params)
        session.delete(author)
        session.commit()
    return redirect(request.args.get('from', default='/book_data/my', type=str))


@blueprint.route('/new_genre', methods=['GET', 'POST'])
@login_required
def new_genre():
    form = GenreForm()

    template_params = {
        'template_name_or_list': 'author_or_genre.html',
        'form': form,
        'title': 'Добавление жанра'
    }

    if form.validate_on_submit():
        session = db_session.create_session()

        genre = Genre(
            user_id=current_user.id,
            name=form.name.data
        )

        session.add(genre)
        session.commit()

        return redirect('/book_data/my')
    return render_template(**template_params)


@blueprint.route('/edit_genre/<int:genre_id>', methods=['GET', 'POST'])
@login_required
def edit_genre(genre_id):
    session = db_session.create_session()
    genre = session.query(Genre).get(genre_id)

    if not genre:
        return redirect('/book_data/all')

    form = GenreForm()
    template_params = {
        'template_name_or_list': 'author_or_genre.html',
        'title': f'Редактирование жанра id{genre_id} ({genre.name})',
        'form': form,
    }

    if (genre.user == current_user and genre.status == -1) or current_user.is_moderator:
        if not form.validate_on_submit():
            form.name.data = genre.name
            return render_template(**template_params)

        genre.name = form.name.data
        if not current_user.is_moderator:
            genre.status = 0
        session.commit()

    return redirect(request.args.get('from', default='/book_data/my', type=str))


@blueprint.route('/delete_genre/<int:genre_id>', methods=['GET', 'POST'])
@login_required
def delete_genre(genre_id):
    session = db_session.create_session()
    genre = session.query(Genre).get(genre_id)

    if not genre or len(genre.books) > 0:
        return redirect('/book_data/my')

    if (genre.user == current_user and genre.status == -1) or current_user.is_moderator:
        form = DeleteForm()

        template_params = {
            'template_name_or_list': 'delete_element.html',
            'title': 'Удаление жанра',
            'text': f'Подтвердите удаление жанра id{genre.id} "{genre.name}".',
            'form': form,
            'to_redirect': request.args.get('from', default='/book_data/my', type=str)
        }

        if not form.validate_on_submit():
            return render_template(**template_params)
        session.delete(genre)
        session.commit()
    return redirect(request.args.get('from', default='/book_data/my', type=str))
