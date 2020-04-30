from bots_infrastructure.command_engine import BotCommand, BotAnswer
from search import search


def action(params):
    name = ' '.join(params)
    books = search(name=name)
    if len(books.all()) == 0:
        return 'Книг с таким именем не найдено.'
    answer = f'Результаты по запросу "{name}"\n'
    for book in books:
        answer += f'''Название книги: {book.name}
Автор: {book.author.name}
Жанр: {book.genre.name}
ID в библиотеке: {book.id}

'''
    return BotAnswer(answer)


command = BotCommand('find_book', action)
command.platforms = {'vk', 'discord'}
command.description = 'Поиск книги по названию'
