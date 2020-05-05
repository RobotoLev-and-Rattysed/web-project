from bots_infrastructure.command_engine import BotCommand
from search import search


def action(params):
    genre = ' '.join(params)
    return search(genre=genre)


command = BotCommand('find-genre', action)
command.platforms = {'vk', 'discord'}
command.description = '''Поиск книг по жанру.
Использование: -find-genre [ЖАНР]'''
