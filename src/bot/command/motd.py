from src.bot.command.abstractcommand import AbstractCommand

class Motd(AbstractCommand):
    """
    Class for executing the !motd command.

    Command send the message of the day defined in the config file to the
    irc channel as a message.

    @Author N McCallum
    """

    def __init__(self, messenger):
        super(Motd, self).__init__(messenger)

        # Command does not require mod access
        self.modOnlyAccess = False
        self.command = "!motd"

    def execute(self, user):
        """
        execute(User)

        Checks if the command is enabled and the user has the permissions to execute it, then
        sends the message stored under 'motdvalue' in values to the IRC server as a message.
        """

        self.logger.info("Command detected: {}, sending message...".format(self.command))

        if self.checkIfEnabled():
            if self.checkIfAllowed(user):
                if self.readMotdValue() is not None:
                    self.messenger.setMessage(self.readMotdValue())
                    self.messenger.sendMessage()
                    self.logger.info("User {} executed {} command.".format(user.userName, self.command))
                else:
                    self.logger.error("Could not find value for {} command".format(self.command))
            else:
                self.logger.info("User {} does not have permission to run command.".format(user.userName))
        else:
            self.logger.info("Command not enabled")

    def readMotdValue(self):
        """
        readMotdValue() -> str

        Looks in the configuration file for the string saved under the tag 'motdvalue' and returns it.
        If it does not exist it returns None.
        """

        for key in self.valueList:
            if key == "motdvalue":
                return self.valueList.get(key)

        return None
