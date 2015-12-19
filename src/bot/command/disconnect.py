from src.bot.command.commander import AbstractCommand
from src.runner import Runner


class Disconnect(AbstractCommand):
    """
    Class for executing the !motd command.

    Command send the message of the day defined in the config file to the
    irc channel as a message.

    @Author N McCallum
    """

    def __init__(self, messenger):
        super(Disconnect, self).__init__(messenger)

        # Command does not require mod access
        self.modOnlyAccess = True
        self.command = "!disconnect"

    def execute(self, user):
        """
        execute(User)

        Checks if the command is enabled and the user has the permissions to execute it, then
        sends the message stored under 'motdvalue' in values to the IRC server as a message.
        """
        Runner.stop()

