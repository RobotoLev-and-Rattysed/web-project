bot_commands = {}


class BotCommand:
    def __init__(self, keyword, action):
        self.keyword = keyword
        self.action = action
        bot_commands[self.keyword] = self

        self.platforms = set()
        self.description = ''

    def action(self):
        pass


class BotAnswer:
    def __init__(self, text=None, attachments=None):
        self.text = text
        self.attachments = attachments


class WrongParams(Exception):
    pass