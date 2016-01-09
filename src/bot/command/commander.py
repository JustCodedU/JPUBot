from abc import abstractmethod, ABCMeta
import re
import src.bot.config.config as BotSettings
import importlib
import os
import logging
from src.bot.messaging.messenger import MessageConstants

class CommandRunner:

    def __init__(self, messenger, user_tracker):
        self.logger = logging.getLogger("LOG")
        self.user_tracker = user_tracker
        self.messenger = messenger

    def findAndExecute(self, buffer):
        importlib.reload(BotSettings)
        commands = BotSettings.config['commands']
        mappings = BotSettings.config['mappings']
        lines = str.split(buffer, "\n")

        for line in lines:
            if MessageConstants.PRIV_MSG() in line:
                command = self.findCommand(line)
                user = self.user_tracker.returnUser(line)

                if command not in commands:
                    return
                module = __import__("src.bot.command." + mappings[command].lower())
                module = getattr(module, "bot")
                module = getattr(module, "command")
                module = getattr(module, mappings[command].lower())
                module = getattr(module, mappings[command])
                instance = module(self.messenger)

                if instance is not None and issubclass(type(instance), AbstractCommand):
                    instance.execute(user)

    def findCommand(self, line):
        lines = str.split(line, " ")
        return re.sub(':', '', lines[3]).strip()



class AbstractCommand:
    """
    Abstract class for the commands classes to extend that gives
    basic functionality for the command. Provides methods that check if the command is enabled
    and if the user has the required permissions to execute the command.

    @author N McCallum
    """

    __metaclass__ = ABCMeta
    modOnlyAccess = False
    command = ""

    def __init__(self, messenger):
        # For the new instance reload the config file
        importlib.reload(BotSettings)

        # Load the configs
        self.commandList = BotSettings.config['commands']
        self.propertyList = BotSettings.config['properties']
        self.valueList = BotSettings.config['values']
        self.messenger = messenger

        # Load logger instance
        self.logger = logging.getLogger("LOG")

    @abstractmethod
    def execute(self, user):
        """
        execute(User)

        Execute method for the command. Executes what should happen during the command.
        """
        pass

    def checkIfAllowed(self, user):
        """
        checkIfAllowed(User) -> boolean

        Method to check if the user has the required access privileges to run the command.
        """

        # Default case if mod access is not needed everyone has access
        if not self.modOnlyAccess:
            return True

        # Otherwise check the user's access level
        if user.modAccess == self.modOnlyAccess:
            return True
        else:
            return False

    def checkIfEnabled(self):
        """
        checkIfEnabled() -> boolean

        Method to check if the command is enabled in the config file.
        """

        # Reload the command file to check for new commands
        importlib.reload(BotSettings)
        matches = BotSettings.config['commands']

        # Check for the match and if it is there return the value that goes with the command
        for key in matches:
            key.strip("!")
            if key == self.command:
                return matches.get(key)

        # If reached the command does not exist
        return False

    def getTextLine(self, index, path):
        """
        getTextLine(int, str) -> str

        Searches the path provided for a readable file and returns the line number relative to the bottom given by
        the index.

        Examples:
            Index of -1 returns latest line in the file.
        """

        # Set data to none by default
        data = None

        # Check if the file is accessible
        if not os.path.exists(path):
            self.logger.error("Cannot find file at path provided in config file: ".format(path))
            return None

        # Try to read text file and return the value of the last line in the file
        try:
            with open(path, 'r') as file:
                data = file.readline(index)
        except IOError:
            self.logger.error("Error when opening file, check if file is readable: ".format(path))
        finally:
            return data
