from bots_infrastructure.command_engine import BotCommand
from search import search


def action(params):
    author = ' '.join(params)
    return search(author=author)


command = BotCommand('find-author', action)
command.platforms = {'vk', 'discord'}
command.description = '''Поиск книг по автору.
Использование: -find-author [АВТОР_КНИГИ]'''
