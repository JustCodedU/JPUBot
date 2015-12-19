import logging
from _socket import socket
import socket as Socket
from _socket import gaierror
from _socket import error
from src.bot.config.config import config as BotSettings
from time import sleep
from src.bot.exception.exceptions import *

class _MessageConstants(object):
    """
    Helper class that holds constants for messaging through the IRC.

    Holds static methods that retrieve the information from the configuration
    file and returns the resulting value.

    Holding them in static methods does not allow editing of the values.

    @Author N McCallum
    """

    @staticmethod
    def CHANNEL():
        return BotSettings["channel"]

    @staticmethod
    def LEAVE_MESSAGE():
        return BotSettings["leavemessage"]

    @staticmethod
    def MESSAGE():
        return "PRIVMSG %s :" % BotSettings["channel"]

    @staticmethod
    def USERNAME():
        return BotSettings["username"]

    @staticmethod
    def OAUTH():
        return BotSettings["oauthcode"]

    @staticmethod
    def IRC_ADDRESS():
        return BotSettings["server"]

    @staticmethod
    def IRC_PORT():
        return BotSettings["port"]

class SocketHandler(object):
    """
    Class holds the socket instance and handles the connection to the IRC server and channel.

    Methods can be used to connect to the IRC server provided in the configuration file, login using
    the properties in the configuration file, connect to the channel, and logout/close the application.

    Attributes:
        socket (socket): socket that will be used to communicate with IRC server

    @Author N McCallum
    """

    socket = Socket.socket(Socket.AF_INET, Socket.SOCK_STREAM)

    def __init__(self):
        # Load logger instance
        self.logger = logging.getLogger("LOG")

    def resetSocket(self):
        """
        resetSocket()

        Resets the current instance of the socket. This will close the socket and the socket will need to be
        reconnected to the channel before sending messages/commands.
        """

        self.socket = socket()

    def connect(self):
        """
        connect()

        Attempts to connect to the hostname and port given in the configuration file. If connection fails,
        exceptions are printed as logging errors.
        """

        self.logger.info("Attempting to connect to IRC server...")
        try:
            self.socket.connect((_MessageConstants.IRC_ADDRESS(), _MessageConstants.IRC_PORT()))
            self.logger.info("Connection successful!")

        except gaierror:
            self.logger.error("Could not lookup address {}".format(_MessageConstants.IRC_ADDRESS()))

        except OverflowError:
            self.logger.error("Port {} invalid! Must be 0-65535".format(_MessageConstants.IRC_PORT()))

        except TimeoutError:
            self.logger.error("Connection to server timed out. Could not establish connection")

        except error as e:
            self.logger.error("Connection failed: {}".format(e))

    def login(self):
        """
        login()

        Attempts to login to the IRC server with the given username and oauth password in the configuration file.
        If the login fails, exceptions are printed as logging errors.
        """

        self.logger.info("Attempting to login to IRC server...")
        try:
            self.socket.send(("PASS %s\r\n" % _MessageConstants.OAUTH()).encode())
            self.socket.send(("NICK %s\r\n" % _MessageConstants.USERNAME()).encode())
            self.socket.send(("USER %s %s BOT :%s\r\n" % (_MessageConstants.USERNAME(),
                                                          _MessageConstants.IRC_ADDRESS(),
                                                          _MessageConstants.OAUTH())).encode())
            self.logger.info("Login Successful!")

        except TimeoutError:
            self.logger.error("Connection to server timed out.")

        except error as e:
            self.logger.error("Login failed: {}".format(e))

    def joinChannel(self):
        """
        joinChannel()

        Attempts to join the channel name given in the configuration file. Upon failure, prints exceptions
        as logging errors.
        """

        self.logger.info("Attempting to join channel {}...".format(_MessageConstants.CHANNEL()))
        try:
            self.socket.send(("JOIN %s\r\n" % _MessageConstants.CHANNEL()).encode())
            message = IRCMessenger(BotSettings["joinmessage"])
            message.sendMessage()

            # TODO this needs to get implemented
            # self.socketHandler.socket.send(("CAP REQ :twitch.tv/membership").encode())
            self.logger.info("Joined channel {} !".format(_MessageConstants.CHANNEL()))

        except TimeoutError:
            self.logger.error("Connection to server timed out.")

        except error as e:
            self.logger.error("Could not join channel: {}".format(e))

    def logout(self):
        """
        logout()

        Attempts to logout of the IRC server and close the application gracefully. Upon failure, prints exceptions
        as logging errors and force closes the socket and application exits with code 1.
        """

        self.logger.info("Attempting to logout of IRC server...")
        error_code = 0

        try:
            mes = IRCMessenger(BotSettings['leavemessage'])
            mes.sendMessage()
            self.logger.info("Closing socket...")
            sleep(5)
            self.socket.send("QUIT \r\n".encode())
            self.socket.close()
            self.logger.info("Exiting application...")

        except TimeoutError:
            self.logger.error("Connection to server timed out.")
            error_code = 1

        except error as e:
            self.logger.error("Unable to disconnect gracefully: {}".format(e))
            error_code = 2

        finally:
            self.logger.error("Exiting application...")
            self.socket.close()
            exit(error_code)


class IRCMessenger(object):
    """
    Messaging implementation for twitch API.

    Allows creation of messages and sending to the irc channel through the API. Can send regular messages or coloured
    "me" messages. Checks the data buffer after sending the message to see if the message was sent successfully. On
    failure, the exception is logged.

    Uses socketHandler() instance to send the messages through the connected socket.

    @Author N McCallum
    """

    def __init__(self, message=""):
        self.message = message
        self.socketHandler = SocketHandler()

        # Load logger instance
        self.logger = logging.getLogger("LOG")

    def setMessage(self, message):
        """
        setMessage(str)

        Sets the message instance variable to the string provided in the method call.
        """

        if type(message) == str:
            self.message = message
        else:
            self.logger.error("Can't set message because not string")

    def sendMessage(self):
        """
        sendMessage()

        Attempts to send the message in the message instance variable as a private message to the IRC server channel
        using the socketHandler() instance.
        """

        try:
            self.socketHandler.socket.send(("%s %s\r\n" % (_MessageConstants.MESSAGE(), self.message)).encode())
            # reader = IRCListener()
            # data = reader.readChat()

            # if self.message not in data:
            #     raise MessageError("Message could not be sent to server: " + self.message)

            self.logger.info("Message Sent: {}".format(self.message))

        except MessageError as e:
            self.logger.error("Error trying to send message: {}".format(e))

        except OSError as e:
            self.logger.error("OS Error occurred trying to send message \"{}\": {}".format(self.message, e))

    def sendMeMessage(self):
        """
        sendMeMessage()

        Attempts to send the message in the message instance variable as a private message to the IRC server channel
        using the socketHandler() instance. Text will appear coloured on the twitch chat channel.
        """
        try:
            self.socketHandler.socket.send(("%s/me %s\r\n" % (_MessageConstants.MESSAGE(), self.message)).encode())
            # reader = IRCListener()
            # data = reader.readChat()

            # if self.message not in data:
            #     raise MessageError("Me message could not be send to server: " + self.message)

            self.logger.info("Me Message Sent: {}".format(self.message))

        except MessageError as e:
            self.logger.error("Error trying to send me message: {}".format(e))

        except OSError as e:
            self.logger.error("OS Error occurred trying to send me message \"{}\": {}".format(self.message, e))


class IRCListener(object):
    """
    Chat reader for the IRC channel.

    Used to read the chat and hold onto the read elements in the buffer so the chat log can be accessed.
    Buffer can be reset to allow for certain size.

    Uses socketHandler() instance to receive the messages through the connected socket.

    @Author N McCallum
    """

    buffer = ""

    def __init__(self, bufferSize=1024):
        self.bufferSize = bufferSize
        self.socketHandler = SocketHandler()

        # Load logger instance
        self.logger = logging.getLogger("LOG")

    def resetBuffer(self):
        """
        resetBuffer()

        Resets the current buffer and erases the chat log.
        """

        self.buffer = ""

    def readChat(self):
        """
        readChat() -> str

        Reads the chat to the given buffer size in the instance variable and decodes it.
        Returns the string of the read buffer size and adds to the total buffer variable.
        """

        try:
            # Receive data and add to the buffer
            data = self.socketHandler.socket.recv(1024).decode()
            data = data.rstrip()

            self.buffer += data + "\n"
            return data

        except OSError as exception:
            self.logger.error("OS error trying to read from IRC: {}".format(exception))

        except ReadIRCError as exception:
            self.logger.error("Error reading buffer: {}".format(exception))
