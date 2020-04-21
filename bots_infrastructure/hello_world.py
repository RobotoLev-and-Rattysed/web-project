from .command_engine import BotCommand


def action():
    return 'Hello World!', 'photo-194404073_457239017'


command = BotCommand('hello_world', action)
command.platforms = {'vk', 'discord'}
command.description = 'Поздороваюсь с миром'
