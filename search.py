from data import db_session
from data.db_session import Book, Author, Genre


def search(name='', author='', genre=''):
    sesion = db_session.create_session()
    books = sesion.query(Book).join(Author).join(Genre).filter(Book.name.like('%' + name + '%'),
                                                               Author.name.like('%' + author + '%'),
                                                               Genre.name.like('%' + genre + '%'),
                                                               Book.status == 1)
    return books
    # for book in books:
    #     print(book.name)
    #     print(book.author.name)
    #     print(book.id)
    #     print()
