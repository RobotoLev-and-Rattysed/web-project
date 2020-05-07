from flask import Blueprint, render_template, redirect, request, abort
from flask_login import current_user, login_required

from data import db_session
from data.db_session import Book, Author, Genre


blueprint = Blueprint(__name__, 'requests_blueprint', template_folder='templates')


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


@blueprint.route('/request/<string:modified_class>/<int:modified_id>/<string:new_request_status>')
@login_required
def request_action(modified_class, modified_id, new_request_status):
    if not current_user.is_moderator or modified_class not in {'book', 'author', 'genre'}:
        return redirect('/my')

    session = db_session.create_session()

    if modified_class == 'book':
        element = session.query(Book).get(modified_id)
    elif modified_class == 'author':
        element = session.query(Author).get(modified_id)
    else:
        element = session.query(Genre).get(modified_id)

    if modified_class != 'book' and len(element.books) > 0:
        return redirect(request.args.get('from', default='/book_data/my', type=str))

    if (element and
            (new_request_status.isdigit() or
             (new_request_status[0] == '-' and new_request_status[1:].isdigit()))
            and -1 <= int(new_request_status) <= 1):
        element.status = int(new_request_status)
        print(int(new_request_status))
        session.commit()

    return redirect(request.args.get('from', default='/my', type=str))
