from src.bot.command.abstractcommand import AbstractCommand

class Song(AbstractCommand):

    def __init__(self):
        super(Song, self).__init__()

        # This command does not require mod privileges
        self.modOnlyAccess = False
        self.command = "!song"

    def execute(self):
        pass
