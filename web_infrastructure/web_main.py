from flask import Blueprint, render_template, request, make_response, jsonify

from data import db_session
from data.db_session import User, Book


blueprint = Blueprint(__name__, 'web_main', template_folder='templates')


@blueprint.app_errorhandler(404)
def not_found(error):
    if request.path.startswith('/api/'):
        return make_response(jsonify({'error': 'Not found'}), 404)
    return error


@blueprint.route('/')
def main():
    session = db_session.create_session()
    template_params = {
        'template_name_or_list': 'greeting.html',
        'title': 'ИЭБ',
        'books_count': len(session.query(Book).filter(Book.status == 1).all()),
        'users_count': len(session.query(User).all())
    }
    return render_template('greeting.html', title='Электронная библиотека')
