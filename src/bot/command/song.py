from src.bot.command.abstractcommand import AbstractCommand

class Song(AbstractCommand):
    """
    Class for executing the !song command.

    Command reads file at given location in config file and gives the last line
    in the file which should be the song playing.

    @Author N McCallum
    """

    def __init__(self, messenger):
        super(Song, self).__init__(messenger)

        # This command does not require mod privileges
        self.modOnlyAccess = False
        self.command = "!song"

    def execute(self, user):
        """
        execute(User)

        Checks if the command is enabled and the user has the permissions to execute it, then
        reads the last line in the file stored under 'songpath' in the configuration file and sends
        a message to the IRC server of what is stored inside.
        """

        self.logger.info("Command detected: {}, sending message...".format(self.command))

        if self.checkIfEnabled():
            if self.checkIfAllowed(user):
                if self.readSongPath() is not None:
                    self.messenger.setMessage(self.getTextLine(-1, self.readSongPath()))
                    self.messenger.sendMeMessage()
                    self.logger.info("User {} executed {} command.".format(user.userName, self.command))
                else:
                    self.logger.error("Could not find value for {} command".format(self.command))
            else:
                self.logger.info("User {} does not have permission to run command.".format(user.userName))
        else:
            self.logger.info("Command not enabled")

    def readSongPath(self):
        """
        readSongPath() -> str

        Looks in the configuration file for the string saved under the tag 'songpath' and returns it.
        If it does not exist it returns None.
        """

        for key in self.propertyList:
            if key == "songpath":
                return self.propertyList.get(key)

        return None
