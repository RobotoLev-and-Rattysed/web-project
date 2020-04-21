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
