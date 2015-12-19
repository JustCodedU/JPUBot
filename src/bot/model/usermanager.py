import logging
import re
from src.bot.config.config import config as BotSettings
from src.bot.model.user import User

class UserTracker(object):
    """
    Tracks users that are joined and leaving the channel.
    Also searches for moderators and updates privileges.

    @Author N McCallum
    """

    userList = {}

    def __init__(self):
        self.logger = logging.getLogger("LOG")

    def resetUserList(self):
        """
        resetUserList()

        Clears the list of users back to an empty list.
        """

        self.userList = {}

    def registerUser(self, user):
        """
        registerUser(User)

        Adds user given to the user list under key username from User object
        with value of the User object passed.
        """

        # Do not register null user
        if not user:
            self.logger.error("Cannot register null user!")
            return

        # Else add user to tracking list
        self.userList[user.userName] = user
        self.logger.info("User: {} added to connected users.".format(user.userName))

    def deRegisterUser(self, user):
        """
        deRegisterUser(User)

        Removes user from the user list if they exist in it already.
        Deletes the entry from the user list under key username from User object
        """

        # Do not look for null
        if not user:
            self.logger.error("Cannot de-register null user!")
            return

        # If the user exists remove it from the list
        for listedUser in self.userList.keys():
            if user.userName == listedUser:
                del self.userList[listedUser]
                self.logger.info("User: {} removed from connected users.".format(user.userName))
                return

        # Else send error log
        self.logger.error("Cannot de-register user because they are not registered!")

    def isolateUserName(self, line):
        """
        isolateUserName(string) -> string

        Takes a line from the IRC buffer and isolates the username from join
        and leaving messages and returns it.
        """

        # Remove all special characters from the line
        line = re.sub('[^A-Za-z0-9]+', ' ', line)
        line.strip()

        # Return the first set of characters
        return line.split(" ")[0]

    def findUser(self, buffer):
        """
        findUser(string)

        Takes the buffer read from the IRC and looks for join/leave messages
        and updates the user list accordingly.
        """

        # Split the buffer into a list by line
        data = buffer.split("\n")

        # Loop through the lines in the buffer
        for line in data:
            # Check if a user has joined
            if "has joined {}".format(BotSettings['channel']) in line:
                # Find username and create new user
                username = self.isolateUserName(line)
                user = User(username)

                # Add user to the list
                self.registerUser(user)

            # Check if user has left channel
            elif "has left {}".format(BotSettings['channel']) in line:
                # Find username and create new user
                username = self.isolateUserName(line)
                user = User(username)

                # Remove user from the list
                self.deRegisterUser(user)

    def __updatePrivileges(self, privilege, line):
        """
        __updatePrivileges(boolean, string)

        Helper method that isolates for the username then retrieves
        the user object mapped under that key and updates the access
        privilege given in boolean.
        """

        # Isolate for the username
        username = line.strip("+o ").strip("\r")    # \r is sometimes added for unknown reason

        # Update user's mod access
        user = self.userList.get(username)
        user.setModAccess(privilege)
        self.userList[user.userName] = user

    def findMods(self, buffer):
        """
        findMods(string)

        Looks for IRC mod access update lines in IRC buffer and
        updates those user's privileges.
        """

        # Split the buffer into a list by line
        data = buffer.split("\n")

        # Loop through the lines in the buffer
        for line in data:
            if (":jtv MODE %s" % BotSettings['channel']) in line:
                # Isolate the user name
                line = re.sub('^.*%s ' % BotSettings['channel'], '', line)

                # Check for the +o or -o modifier and add/remove from mod list
                if "+o" in line:
                    # Set the mod access for the user to true
                    self.__updatePrivileges(True, line)

                elif "-o" in line:
                    # Set the mod access for the user to false
                    self.__updatePrivileges(False, line)
