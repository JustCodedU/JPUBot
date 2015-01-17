"""
Config file for settings for IRC Bot.
"""

global config

config = {

    # Basic bot configurations needed to log into irc server
    'server': 'irc.twitch.tv',
    'port': 6667,
    'username': 'username',
    'password': 'oauth password',

    # Customized settings for bot
    'channel': '#channelname',
    'joinmessage': 'JPUBot has joined the channel',
    'leavemessage': 'JPUBot Disconnecting from channel',

    # Commands that bot can use
    'commands': {
        '!disconnect': 'disconnect',
        '!addcom': 'addcom',
        '!remcom': 'remcom',
        '!motd': 'Message of the day.',
        '!test': 'Test command received.'
        
        # Custom commands added below
    }
}

