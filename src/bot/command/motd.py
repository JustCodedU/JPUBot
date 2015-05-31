"""
    Class for executing the !motd command.

    Command send the message of the day defined in the config file to the
    irc channel as a message.

    @Author N McCallum
"""

from src.bot.command.abstractcommand import AbstractCommand
from logging import Logger

class Motd(AbstractCommand):

    def __init__(self):
        super(Motd, self).__init__()

        # Command does not require mod access
        self.modOnlyAccess = False
        self.command = "!motd"

    def execute(self):
        # TODO create messaging wrapper to get executes started to be defined
        pass

    def readMotdValue(self):
        # Look for the value in config
        for key in self.valueList:
            if key == "motdvalue":
                return self.valueList.get(key)

        return None
