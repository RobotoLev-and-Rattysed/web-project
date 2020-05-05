from data import db_session
from data.db_session import Book, Author, Genre
from bots_infrastructure.command_engine import BotAnswer


def search(name='', author='', genre=''):
    sesion = db_session.create_session()
    books = sesion.query(Book).join(Author).join(Genre).filter((Book.name.like('%' + name + '%') |
                                                                Book.name.like('%' + name.capitalize() + '%') |
                                                                Book.name.like('%' + name.lower() + '%')),
                                                               (Author.name.like('%' + author + '%') |
                                                                Author.name.like('%' + author.capitalize() + '%') |
                                                                Author.name.like('%' + author.lower() + '%')),
                                                               (Genre.name.like('%' + genre + '%') |
                                                                Genre.name.like('%' + genre.capitalize() + '%') |
                                                                Genre.name.like('%' + genre.lower() + '%')),
                                                               Book.status == 1)
    if len(books.all()) == 0:
        return BotAnswer('Книг с таким именем не найдено.')
    answer = f'Результаты по запросу "{name + author + genre}"\n'
    for book in books:
        answer += f'''Название книги: {book.name}
    Автор: {book.author.name}
    Жанр: {book.genre.name}
    ID в библиотеке: {book.id}

    '''
    return BotAnswer(answer)
