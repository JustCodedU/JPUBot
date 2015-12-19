from src.bot.model.user import User
from src.bot.command.motd import Motd
from src.bot.command.song import Song
from src.bot.messaging.messenger import SocketHandler, IRCListener, IRCMessenger
from time import sleep

if __name__ == "__main__":
    me = User("Justpwnedu", True)
    irc = SocketHandler()
    messenger = IRCMessenger()
    irc.connect()
    sleep(1)

    irc.login()
    sleep(1)

    irc.joinChannel()
    sleep(1)

    m = Motd(messenger)
    m.execute(me)
    sleep(1)

    m = Song(messenger)
    m.execute(me)
    sleep(1)

    irc.logout()

