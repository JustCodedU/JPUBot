"""
    Class for executing the !song command.

    Command reads file at given location in config file and gives the last line
    in the file which should be the song playing.

    @Author N McCallum
"""

from src.bot.command.abstractcommand import AbstractCommand

class Song(AbstractCommand):

    def __init__(self):
        super(Song, self).__init__()

        # This command does not require mod privileges
        self.modOnlyAccess = False
        self.command = "!song"

    def execute(self):
        pass
