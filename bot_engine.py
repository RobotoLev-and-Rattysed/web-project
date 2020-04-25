import bots_infrastructure.__all_commands
from bots_infrastructure.command_engine import bot_commands


def get_answer(message_text, platform):
    if message_text == "" or message_text[0] != '-':
        return None, None

    command = message_text[1:]
    if command in bot_commands:
        if platform in bot_commands[command].platforms:
            answer_text, answer_attachment = bot_commands[command].action()
        else:
            answer_text, answer_attachment = "Команда недоступна на данной платформе", None
    else:
        answer_text, answer_attachment = "Такая команда мне не известна", None

    if platform == 'vk':
        return answer_text, answer_attachment
    else:
        return answer_text, None
