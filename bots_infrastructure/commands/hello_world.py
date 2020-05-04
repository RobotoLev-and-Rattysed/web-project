from bots_infrastructure.command_engine import BotCommand, BotAnswer


def action(params):
    return BotAnswer('Hello World!', {'photo': ['static/img/hello_world.jpg']})


command = BotCommand('hello-world', action)
command.platforms = {'vk', 'discord'}
command.description = 'Поздороваюсь с миром'
