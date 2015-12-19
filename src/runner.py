import logging
from src.bot.command.commander import CommandRunner
from src.bot.messaging.messenger import SocketHandler, IRCListener, IRCMessenger
from time import sleep
from src.bot.model.usermanager import UserTracker
from sys import stdout

class Runner:
    irc = SocketHandler()

    def __init__(self):
        # Configure the logger
        logger = logging.getLogger("LOG")
        logger.setLevel(logging.INFO)
        handler = logging.StreamHandler(stdout)
        formatter = logging.Formatter('(%(asctime)s) [%(levelname)s]: %(message)s')
        handler.setFormatter(formatter)
        logger.addHandler(handler)

    def run(self):
        user_tracker = UserTracker()
        messenger = IRCMessenger(self.irc)
        listener = IRCListener(self.irc)
        commander = CommandRunner(messenger, user_tracker)

        self.irc.connect()
        self.irc.login()
        self.irc.joinChannel()

        while True:
            buffer = listener.readChat()
            print("Buffer: " + buffer)

            user_tracker.findUser(buffer)
            user_tracker.findMods(buffer)

            commander.findAndExecute(buffer)
            sleep(0.1)

        self.irc.logout()

    @classmethod
    def stop(cls):
        Runner.irc.logout()
        exit(0)


if __name__ == "__main__":
    runner = Runner()
    runner.run()


