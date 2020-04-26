import bots_infrastructure.__all_commands
from bots_infrastructure.command_engine import bot_commands


def is_command(message_text):
    if len(message_text) < 2 or message_text[0] != '-' or message_text[1:].split()[0] not in bot_commands:
        return False
    else:
        return True


def get_answer(message_text, platform):
    command = message_text[1:]
    # if message_text == "" or message_text[0] != '-':
    #     return None, None
    #
    # command = message_text[1:]
    # if command in bot_commands:
    #     if platform in bot_commands[command].platforms:
    #         answer_text, answer_attachment = bot_commands[command].action()
    #     else:
    #         answer_text, answer_attachment = "Команда недоступна на данной платформе", None
    # else:
    #     answer_text, answer_attachment = "Такая команда мне не известна", None

    # if platform == 'vk':
    #     return answer_text, answer_attachment
    # else:
    #     return answer_text, None
    pass
