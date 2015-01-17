"""
    Command file used to store bot commands and search the commands for the appropriate response.
        @author: N. McCallum
        @version: 2
        @date: 17/01/2015
"""

# Imports
import config as settings
import importlib
import re


class Command(object):

    #=======================================================
    # Constructor for command object.
    #     Input:
    #         data - Buffer to search for commands in.
    #     Output:
    #         None.
    #=======================================================
    def __init__(self, data):
        self.data = data
        self.matches = settings.config['commands']

    #==========================================================
    # Checks for match in buffer to an existing command stored
    # in the config file commands.
    #     Input:
    #         None.
    #     Output:
    #         boolean - Returns True if match is found.
    #                 - Returns False if match not found.
    #===========================================================
    def checkForMatch(self):
        # Check for a match in the array and return true if it is there
        for k in self.matches:
            if k in self.data:
                return True

        return False

    #==========================================================
    # Isolates command from buffer and searches for the
    # matching return message in the commands dictionary.
    #     Input:
    #         None.
    #     Output:
    #         string - value from commands dictionary for
    #                  command.
    #===========================================================
    def findCommand(self):
        # Reload the command file to check for new commands
        importlib.reload(settings)
        self.matches = settings.config['commands']

        # Debug information
        print("[DEBUG] Commands: %s" % self.matches)

        # Check for the match and if it is there return the value that goes with the command
        if self.checkForMatch():
            # Isolate the command from the buffer
            self.data = re.sub('^.*%s' % settings.config['channel'], '', self.data).strip().strip(":").split(" ")[0]

            # Debug information
            print("[DEBUG] Isolated command: %s" % self.data)

            for k in self.matches:
                if k == self.data:
                    return self.matches.get(k)
        else:
            return None

    #==========================================================
    # Searches data for a command that exists in data.
    #     Input:
    #         data - Data to search for command in (string).
    #         com - Command to search for in data (string).
    #     Output:
    #         boolean - Returns True if match is found.
    #                 - Returns False if match not found.
    #===========================================================
    def inFile(self, data, com):
        # Search the data for the command
        for i in data:
            if com in i:
                # Command is there
                return True
        # Command is not there
        return False

    #==========================================================
    # Attempts to add the command into the commands dictionary
    # inside the config file with the value passed in val.
    #     Input:
    #         com - Command to add in dictionary.
    #         val - Value to store with command.
    #     Output:
    #         boolean - Returns True command was added.
    #                 - Returns False if command was not added.
    #===========================================================
    def addCom(self, com, val):
        # Open the config file and find line with commands
        with open('config.py', 'r') as file:
            data = file.readlines()

        # Debug information
        print("[DEBUG] Printing data contents:")
        print(data)
        print("Attempting to add command...")

        # Check if the command already exists
        if self.inFile(data, com):
            print("[CONSOLE] Command has not been added because it already exists.")
            return False

        # Create new com string with correct format
        com = "        , '%s': '%s'" % (com, val)

        # Find the correct spot to add the command and add it there
        for i in range(0, len(data) - 1):
            if "# Custom commands added below" in data[i]:
                data.insert(i + 1, com + "\n")

        # Debug information
        print("[DEBUG] Printing data contents after command insertion:")
        print(data)

        # Write changes to file
        with open('config.py', 'w') as file:
            file.write("".join(data))

        # Print result
        print("[CONSOLE] Command has been added.")

        return True

    #===========================================================
    # Attempts to remove the command from the commands
    # dictionary inside the config file.
    #     Input:
    #         com - Command to remove from dictionary.
    #     Output:
    #         boolean - Returns True command was deleted.
    #                 - Returns False if command was not deleted.
    #============================================================
    def remCom(self, com):
        # Open the config file and find line with commands
        with open('config.py', 'r') as file:
            data = file.readlines()

        # Debug information
        print("[DEBUG] Printing data contents:")
        print(data)
        print("[CONSOLE] Attempting to remove command...")

        # Check if command exists in file
        if not self.inFile(data,com):
            print("[CONSOLE] Command does not exist.")
            return False

        # Find the line containing the command and delete it
        for i in range(0, len(data) - 1):
            if com in data[i]:
                del data[i]

        # Debug information
        print("[DEBUG] Printing data contents after command insertion:")
        print(data)

        # Write the new data back into the file
        with open('config.py', 'w') as file:
            file.write("".join(data))

        # Print the result to the console
        print("[CONSOLE] Command has been removed.")

        return True