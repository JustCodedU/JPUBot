"""
    Abstract class for the commands classes to extend that gives
    basic functionality for the command.

    @author N McCallum
"""

from abc import abstractmethod, ABCMeta
import src.bot.config.config as BotSettings
import importlib

class AbstractCommand:
    __metaclass__ = ABCMeta
    modOnlyAccess = False
    command = ""

    def __init__(self):
        pass

    """
        Execute method for the command. Executes what should happen during the command.
    """
    @abstractmethod
    def execute(self):
        pass

    """
        Method to check if the user has the required access privileges to run the command.

        @param user - User object for the user trying to execute command.
        @return boolean value if user is allowed to execute command.
    """
    def checkIfAllowed(self, user):
        # Default case if mod access is not needed everyone has access
        if not self.modOnlyAccess:
            return True

        # Otherwise check the user's access level
        if user.getModAccess == self.modOnlyAccess:
            return True
        else:
            return False

    """
        Method to check if the command is enabled in the config file.

        @return boolean value if the command has been enabled in the settings
    """
    def checkIfEnabled(self):
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
