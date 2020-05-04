from bots_infrastructure.command_engine import BotCommand, BotAnswer, WrongParams
from data import db_session
from data.db_session import Book, Author, Genre


def action(params):
    if len(params) != 1:
        raise WrongParams
    try:
        id = int(params[0])
    except Exception:
        raise WrongParams
    sesion = db_session.create_session()
    book = sesion.query(Book).join(Author).join(Genre).filter(Book.id == id,
                                                              Book.status == 1).first()
    if book is None:
        return BotAnswer(f'''Книга с данным ID не найдена на сервере''')
    return BotAnswer(f'''Книга найдена!

Название: {book.name}
Автор: {book.author.name}
Жанр: {book.genre.name}
Описание: {book.description}''')


command = BotCommand('get-book', action)
command.platforms = {'vk', 'discord'}
command.description = '''Получение книги по её уникальному ID
Использование: -get-book [ID]'''
