"""
    Command file used to store bot commands and search the commands for the appropriate response.
        @author: N. McCallum
        @version: 1
        @date: 12/01/2015
"""

# Imports
import config as settings


class Command(object):

    def __init__(self, data):
        self.data = data
        self.matches = settings.config['commands']

    def checkForMatch(self):
        # Check for a match in the array and return true if it is there
        for k, v in self.matches:
            if k in self.data:
                return True

        return False

    def findCommand(self):
        # Check for the match and if it is there return the value that goes with the command
        if self.checkForMatch():
            for k, v in self.matches:
                if k in self.data:
                    return v
        else:
            return None

    def addCom(self, com):
        # Open the config file and find line with commands
        with open('config.py', 'r') as file:
            data = file.readlines()

        # Debug information
        print("[DEBUG] Printing data contents:")
        print(data)

        for i in range(0, len(data)):
            if "# End of commands" in data[i]:
                data.insert(i - 2, com)

        # Debug information
        print("[DEBUG] Printing data contents after command insertion:")
        print(data)

        print("Attempting to add command...")
        with open('config.py', 'w') as file:
            file.write(data)

        print("Command has been added.")