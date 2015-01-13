"""
    Bot file to set-up and run bot in chat. Scans chat for commands and replies with
    the value set in the config file.
        @author: N. McCallum
        @version: 1
        @date: 13/01/2015
"""

import _socket
import config as settings   #Change folder location to config.config
import commands


class Bot(object):

    #=======================================================
    # Constructor for bot.
    #     Input:
    #         channel - channel name to connect to in irc.
    #     Output:
    #         None.
    #=======================================================
    def __init__(self, channel):
        # Set the channel to the user input
        self.channel = channel

        # Create new socket to connect to irc
        self.s = _socket.socket()

        # Define constants for class
        self.nick = "justbottedyou"
        self.realid = "justbottedyou"
        self.irc = "irc.twitch.tv"
        self.port = 6667
        self.passw = "oauth:dzp8ts6z6t1c5ezf1wkjmky5gsf3qc"
        self.readBuffer = ""

    #=======================================================
    # Function to connect to irc server and log in as bot
    #   Input:
    #       None.
    #   Output:
    #       None.
    #=======================================================
    def connect(self):
        # Connect to the irc server
        print("Attempting to connect...")
        self.s.connect((self.irc, self.port))

        # Log into the irc server using twitch info
        print("Connected. Attempting to log in...")
        self.s.send(("PASS %s\r\n" % self.passw).encode())
        self.s.send(("NICK %s\r\n" % self.nick).encode())
        self.s.send(("USER %s %s BOT :%s\r\n" % (self.realid, self.irc, self.nick)).encode())

        # Connect to user channel
        print("Logged in. Attempting to join channel " + self.channel + "...")
        self.s.send(("JOIN %s\r\n" % self.channel).encode())
        self.s.send(("PRIVMSG %s :JPUBot Connected to Channel.\r\n" % self.channel).encode())

        return

    #===========================================================================================
    # Function to read chat and return buffer.
    #     Input:
    #         bufferSize - Size to use for buffer, should be multiple of 2 (ie: 1024 - 4096).
    #     Output:
    #         None.
    #===========================================================================================
    def readChat(self, bufferSize):

        # Receive data and add to the buffer
        data = self.s.recv(bufferSize).decode()
        data = data.rstrip()
        self.readBuffer += data

        # Print the buffer to the screen
        print("[DEBUG] Cat'ing Buffer to StdOut:")
        print(self.readBuffer)

        return data

    def run(self):
        # Loop while connected to chat
        while True:
            buffer = self.readChat(1024)

            # Check if bot has disconnected
            if len(buffer) == 0:
                print("Bot has been disconnected. Attempting to reconnect...")
                self.s.send("QUIT \r\n".encode())
                self.connect()

            # Check for ping and reply with pong
            if buffer[:4] == "PING":
                self.s.send("PONG".encode())

            # Check for a message
            if "!test" in buffer:
                self.s.send(("PRIVMSG %s :Test command received.\r\n" % self.channel).encode())

            if "justpwnedu!justpwnedu@justpwnedu.tmi.twitch.tv PRIVMSG #justpwnedu :!disconnect" in buffer:
                self.s.send(("PRIVMSG %s :JPUBot Disconnecting from channel.\r\n" % self.channel).encode())
                self.s.send("QUIT \r\n".encode())
                exit(0)

            data = buffer.split("\n")
            if data[0] == "PING":
                self.s.send("PONG".encode())


    #def checkForCommand(self, data):
        #FIXME: delegate later to commands.py

def main():
    ircBot = Bot("#justpwnedu")
    ircBot.connect()
    ircBot.run()


if __name__ == "__main__":
    main()
