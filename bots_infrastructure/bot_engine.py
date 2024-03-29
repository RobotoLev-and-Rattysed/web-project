import bots_infrastructure.__all_commands
from bots_infrastructure.command_engine import bot_commands, BotAnswer, WrongParams


def is_command(message_text):
    if len(message_text) == 0 or message_text[0] != '-':
        return False
    return True


def get_answer(message_text, platform) -> BotAnswer:
    if not is_command(message_text):
        return BotAnswer()

    words = message_text[1:].split()
    command, params = words[0], words[1:]
    if command in bot_commands:
        if platform in bot_commands[command].platforms:
            try:
                answer = bot_commands[command].action(params)
            except WrongParams:
                answer = bot_commands['help'].action([command])
        else:
            answer = BotAnswer("Команда недоступна на данной платформе")
    else:
        answer = BotAnswer("Такая команда мне не известна")
    if platform == 'discord':
        strings = answer.text.split('\n')
        strings[0] = '> ```' + strings[0] + '```'
        answer.text = '\n'.join(strings)

    return answer
    # if platform == 'vk':
    #     return answer_text, answer_attachment
    # else:
    #     return answer_text, None
