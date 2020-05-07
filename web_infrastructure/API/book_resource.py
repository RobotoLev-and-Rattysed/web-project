from flask import jsonify
from flask_restful import abort, Resource

from data import db_session
from data.db_session import User, Book


class BookResource(Resource):
    def get(self, book_id):
        session = db_session.create_session()
        book = session.query(Book).get(book_id)

        if not book:
            abort(404, message=f'Book {book_id} not found')
        if book.status != 1:
            abort(403, message=f'Book {book_id} is private')

        data = book.to_dict(only=('id', 'name', 'author_id', 'genre_id',
                                  'description', 'image_name', 'text_name'))
        data['image_name'] = '/static/img/books/' + data['image_name']
        data['text_name'] = '/static/txt/books/' + data['text_name']

        return jsonify({'book': data})


class BookListResource(Resource):
    def get(self):
        session = db_session.create_session()
        books = session.query(Book).filter(Book.status == 1).all()
        if not books:
            abort(404, message=f'Books not found')

        books_data = []
        for book in books:
            data = book.to_dict(only=('id', 'name', 'author_id', 'genre_id',
                                      'description', 'image_name', 'text_name'))
            data['image_name'] = '/static/img/books/' + data['image_name']
            data['text_name'] = '/static/txt/books/' + data['text_name']

            books_data.append(data)

        return jsonify({'books': books_data})
