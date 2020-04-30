from bots_infrastructure.command_engine import bot_commands, BotCommand, BotAnswer, WrongParams


def action(params):
    if len(params) == 0:
        text = "Список команд, доступных для выполнения\n\n"
        for bot_command in sorted(list(bot_commands.keys())):
            text += f'{bot_command} - {bot_commands[bot_command].description} ' \
                    f'({", ".join(list(bot_commands[bot_command].platforms))})\n'
    elif len(params != 1):
        raise WrongParams
    else:
        text = 'В процессе создания'
    return BotAnswer(text)


command = BotCommand('help', action)
command.platforms = {'vk', 'discord'}
command.description = 'Информация о доступных командах'
