"""
    Bot file to set-up and run bot in chat. Scans chat for commands and replies with
    the value set in the config file.
        @author: N. McCallum
        @version: 2
        @date: 17/01/2015
"""

import _socket
import config as settings   #Change folder location to config.config
import commands
import re


class Bot(object):

    #=======================================================
    # Constructor for bot.
    #     Input:
    #         None.
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

        # Add the channel owner to the moderators list
        self.moderators = [settings.config['channel'].strip("#")]

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

    #==================================================================
    # Function to disconnect from the irc server and close application.
    #   Input:
    #       None.
    #   Output:
    #       None.
    #===================================================================
    def disconnect(self):
        # FIXME: If left idle for extended period of time disconnect message is not printed
        self.s.send(("PRIVMSG %s :%s.\r\n" % (self.channel, settings.config['leavemessage'])).encode())
        self.s.send("QUIT \r\n".encode())
        exit(0)

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

        # Debug information
        if settings.config['debug']:
            print("[DEBUG] Cat'ing Buffer to StdOut:")
            print(self.readBuffer)

        return data

    #===========================================================================================
    # Function to isolate user from buffer in order to find who put command into chat on
    # irc server. Only works for times when user sends message to irc chat.
    #     Input:
    #         data - Buffer that the function should isolate user on.
    #     Output:
    #         None.
    #===========================================================================================
    def determineUser(self, data):
        # Return the value of the user
        return re.sub('!.*$', '', data.strip().split(" ")[0].strip(":"))

    #===========================================================================================
    # Function to search buffer for moderators and add them if they do not exist in the mod list
    #     Input:
    #         None.
    #     Output:
    #         None.
    #===========================================================================================
    def findMods(self, data):
        # Only search buffer if it contains connected users in it
        if (":jtv MODE %s" % settings.config['channel']) in data:
            # Split the buffer into multiple lines to isolate lines with user in them
            data = data.split("\n")

            # Search for lines with users in it
            for i in data:
                if (":jtv MODE %s" % settings.config['channel']) in i:
                    # Isolate the user name
                    user = re.sub('^.*%s ' % settings.config['channel'], '', i)

                    # Check for the +o or -o modifier and add/remove from mod list
                    if "+o" in user:
                        # Add to the mod list if not already added
                        user = user.strip("+o ").strip("\r")    # \r is sometimes added for unknown reason
                        if user not in self.moderators:
                            self.moderators.append(user)
                    elif "-o" in user:
                        # Remove from mod list
                        user = user.strip("-o ").strip("\r")    # \r is sometimes added for unknown reason
                        if user in self.moderators:
                            self.moderators.remove(user)

                    # If neither is in user do nothing

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

            # Print the buffer to console
            print(buffer)

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

            # Find mods to add/remove from mod list
            self.findMods(buffer)

            # Debug information
            print("[DEBUG] Modded users: %s" % self.moderators)

            # Check for a command in the buffer and print the appropriate response
            c = commands.Command(buffer)
            com = c.findCommand()
            if com is not None:
                print("[DEBUG] Printing Command: %s" % com)

                # Check if com requires a function call
                if com == 'addcom':    # Check if user wants to add command
                    # Debug information
                    print("[DEBUG] Add command detected.")

                    # Check if user is a moderator
                    if self.determineUser(buffer) in self.moderators:
                        print("[DEBUG] Printing buffer: %s" % buffer)

                        # Isolate the command to add into the file
                        words = re.sub('^.*:!addcom', '', buffer).strip()

                        # Split the words into the command and the value
                        words = words.split(" ")
                        newCommand = words[0]
                        newValue = words[1:len(words)]

                        # Check if the user has entered a blank value or command
                        if len(newCommand) == 0 or len(newValue) == 0:
                            print("[CONSOLE] Command field is empty. Command not added.")
                            self.s.send(("PRIVMSG %s :Command not added because field cannot be left empty (Format: !addcom !commandname message to print).\r\n" % self.channel).encode())
                        else:
                            newValue = " ".join(newValue)

                            # Send the string to add function
                            result = c.addCom(newCommand, newValue)

                            # Print the result of the command to the console and server
                            if result:
                                self.s.send(("PRIVMSG %s :Command %s added.\r\n" % (self.channel, newCommand)).encode())
                            else:
                                self.s.send(("PRIVMSG %s :Command %s already exists.\r\n" % (self.channel, newCommand)).encode())

                    else:   # User is not a moderator
                        # Debug information
                        print("[CONSOLE] User is not moderator. Command not executed")
                        self.s.send(("PRIVMSG %s :User is not moderator.\r\n" % self.channel).encode())

                elif com == 'remcom':    # Check if user wants to remove command
                    # Debug information
                    print("[DEBUG] Remove command detected.")

                    # Check if user is a moderator
                    if self.determineUser(buffer) in self.moderators:
                        print("[DEBUG] Printing buffer: %s" % buffer)

                        # Isolate the command to add into the file
                        words = re.sub('^.*:!remcom', '', buffer).strip()

                        # Split the words to find command to remove
                        words = words.split(" ")
                        delCommand = words[0]

                        # Check for empty command
                        if len(delCommand) == 0:
                            print("[CONSOLE] Command field is empty. Command not deleted.")
                            self.s.send(("PRIVMSG %s :Command not removed because field cannot be left empty (Format: !remcom !commandname).\r\n" % self.channel).encode())
                        else:
                            # Send the string to remove function
                            result = c.remCom(delCommand)

                            # Print the result to the console and the server
                            if result:
                                self.s.send(("PRIVMSG %s :Command %s removed.\r\n" % (self.channel, delCommand)).encode())
                            else:
                                self.s.send(("PRIVMSG %s :Command %s does not exist.\r\n" % (self.channel, delCommand)).encode())

                    else:   # User is not a moderator
                        # Debug information
                        print("[CONSOLE] User is not moderator. Command not executed")
                        self.s.send(("PRIVMSG %s :User is not moderator.\r\n" % self.channel).encode())

                elif com == 'disconnect':    # Check for disconnect command
                    # Check if channel owner was the one to use it
                    if self.determineUser(buffer) == settings.config['channel'].strip("#"):
                        # Disconnect from irc server
                        self.disconnect()

                else:   # Doesn't require function call so print command
                    self.s.send(("PRIVMSG %s :%s\r\n" % (self.channel, com)).encode())

            data = buffer.split("\n")
            if data[0] == "PING":
                self.s.send("PONG".encode())


def main():
    ircBot = Bot()
    ircBot.connect()
    ircBot.run()


if __name__ == "__main__":
    main()
