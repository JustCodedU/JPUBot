"""
    Bot file to set-up and run bot in chat. Scans chat for commands and replies with
    the value set in the config file.
        @author: N. McCallum
        @version: 2
        @date: 14/01/2015
"""

import _socket
import config as settings   #Change folder location to config.config
import commands
import re


class Bot(object):

    #=======================================================
    # Constructor for bot.
    #     Input:
    #         channel - channel name to connect to in irc.
    #     Output:
    #         None.
    #=======================================================
    def __init__(self):
        # Set the channel to the user input
        self.channel = settings.config['channel']

        # Create new socket to connect to irc
        self.s = _socket.socket()

        # Define constants for class
        self.nick = settings.config['username']
        self.realid = settings.config['username']
        self.irc = settings.config['server']
        self.port = settings.config['port']
        self.passw = settings.config['password']
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
        self.readBuffer += data + "\n"

        # Print the buffer to the screen
        print("[DEBUG] Cat'ing Buffer to StdOut:")  # FIXME: Not sure if printing buffer to screen each time is needed
        print(self.readBuffer)

        return data

    #===========================================================================================
    # Main function with loop to run the bot continuously on irc server.
    #     Input:
    #         None.
    #     Output:
    #         None.
    #===========================================================================================
    def run(self):
        # Loop while connected to chat
        while True:
            buffer = self.readChat(1024)

            # Check if bot has disconnected
            if len(buffer) == 0:
                print("Bot has been disconnected. Attempting to reconnect...")
                self.s.send("QUIT \r\n".encode())
                self.s.close()
                self.connect()

            # Check for ping and reply with pong
            if buffer[:4] == "PING":
                print("[DEBUG] Ping command detected. Sending pong...")
                self.s.send("PONG".encode())

            # Check if streamer gave disconnect command and disconnect from chat
            if "justpwnedu!justpwnedu@justpwnedu.tmi.twitch.tv PRIVMSG #justpwnedu :!disconnect" in buffer:
                self.s.send(("PRIVMSG %s :JPUBot Disconnecting from channel.\r\n" % self.channel).encode())
                self.s.send("QUIT \r\n".encode())
                exit(0)

            # Check for a command in the buffer and print the appropriate response
            c = commands.Command(buffer)
            com = c.findCommand()
            if com is not None:
                print("[DEBUG] Printing Command: %s" % com)
                # Check if com requires a function call
                if com == 'addcom':
                    # Debug information
                    print("[DEBUG] ADDCOM DETECTED")
                    print("[DEBUG] Printing buffer: %s" % buffer)

                    # Isolate the command to add into the file
                    words = re.sub('^.*:!addcom', '', buffer).strip()

                    # Split the words into the command and the value
                    words = words.split(" ")
                    newCommand = words[0]
                    newValue = words[1:len(words)]
                    newValue = " ".join(newValue)

                    # FIXME: Add default ! to command
                    # Send the string to add to function
                    c.addCom("        , '%s': '%s'" % (newCommand, newValue))
                else:   # Doesn't require function call so print command
                    self.s.send(("PRIVMSG %s :%s\r\n" % (self.channel, com)).encode())

            data = buffer.split("\n")
            if data[0] == "PING":
                self.s.send("PONG".encode())

    #===========================================================================================
    # Function to isolate user from buffer in order to find who put command into chat on
    # irc server.
    #     Input:
    #         data - Buffer that the function should isolate user on.
    #     Output:
    #         None.
    #===========================================================================================
    def determineUser(self, data):
        # Print for debug info and return the value of the user
        print(re.sub('!.*$', '', data.strip().split(" ")[0].strip(":")))
        return re.sub('!.*$', '', data.strip().split(" ")[0].strip(":"))

    #def say(self, msg):
        # FIXME: implement function to write to channel


def main():
    ircBot = Bot()
    ircBot.connect()
    ircBot.run()


if __name__ == "__main__":
    main()
