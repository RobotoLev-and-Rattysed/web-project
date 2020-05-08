from bots_infrastructure.command_engine import BotCommand
from search import search


def action(params):
    name = ' '.join(params)
    return search(name=name)


command = BotCommand('find-book', action)
command.platforms = {'vk', 'discord'}
command.description = '''Поиск книги по названию.
Использование: -find-book [НАЗВАНИЕ КНИГИ]'''
