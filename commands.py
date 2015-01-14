"""
    Command file used to store bot commands and search the commands for the appropriate response.
        @author: N. McCallum
        @version: 2
        @date: 14/01/2015
"""

# Imports
import config as settings
import importlib


class Command(object):

    def __init__(self, data):
        self.data = data
        self.matches = settings.config['commands']

    def checkForMatch(self):
        # Check for a match in the array and return true if it is there
        for k in self.matches:
            if k in self.data:
                return True

        return False

    def findCommand(self):
        # Reload the command file to check for new commands
        importlib.reload(settings)
        self.matches = settings.config['commands']

        # Debug information
        print("[DEBUG] Commands:")
        print(self.matches)

        # Check for the match and if it is there return the value that goes with the command
        if self.checkForMatch():
            for k in self.matches:
                if k in self.data:
                    return self.matches.get(k)
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
            if "# Custom commands added below" in data[i]:
                data.insert(i + 1, com + "\n")

        # Debug information
        print("[DEBUG] Printing data contents after command insertion:")
        print(data)

        print("Attempting to add command...")
        with open('config.py', 'w') as file:
            file.write("".join(data))

        print("Command has been added.")