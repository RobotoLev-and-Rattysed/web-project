from bots_infrastructure.command_engine import bot_commands, BotCommand, BotAnswer, WrongParams


def action(params):
    if len(params) == 0:
        text = "Список команд, доступных для выполнения\n\n"
        for bot_command in sorted(list(bot_commands.keys())):
            text += f'{bot_command} - {bot_commands[bot_command].description} ' \
                    f'({", ".join(list(bot_commands[bot_command].platforms))})\n\n'
    elif len(params) == 1:
        text = params[0]
        if text not in bot_commands.keys():
            return  BotAnswer(text='Данной команды не существует')
        text = bot_commands[text].description
    else:
        raise WrongParams
    return BotAnswer(text)


command = BotCommand('help', action)
command.platforms = {'vk', 'discord'}
command.description = '''Выводит информацию о доступных командах
Использование: -help {КОМАНДА}'''
