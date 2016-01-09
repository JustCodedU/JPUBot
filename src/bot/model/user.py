from functools import reduce
import logging
from time import clock

class User:

    """
    Class to register users that are connected to the channel.
    Class holds the values to give connected time and access level.

    @Author N McCallum
    """

    def __init__(self, userName, modAccess=False):
        self.userName = userName
        self.modAccess = modAccess

        # Initialize join time at creation
        self.joinTime = clock()

        # Load logger instance
        self.logger = logging.getLogger("LOG")

    def getConnectedTime(self):
        """
        getConnectedTime() -> floating point

        Returns floating point number of connected time in seconds.
        """

        return clock() - self.joinTime

    def getConnectedTimeString(self):
        """
        getConnectedTimeString() -> string

        Returns formatted string of user time connected to channel.
        Format: hh:mm:ss
        """

        connectedTime = self.getConnectedTime()

        return "%02d:%02d:%02d" % \
            reduce(lambda a, b: divmod(a[0], b) + a[1:], [(round(connectedTime),), 60, 60])

    def setModAccess(self, modAccess):
        """
        setModAccess(boolean)

        Sets the access level of the user to the boolean passed. Represents if user
        has access to moderator.
        """

        self.logger.info("User [%s] mod access set to: " + str(modAccess), self.userName)
        self.modAccess = modAccess

