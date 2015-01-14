"""
Config file for settings for IRC Bot.
"""

global config

config = {

    # Basic bot configurations needed to log into irc server
    'server': 'irc.twitch.tv',
    'port': 6667,
    'username': 'username',
    'password': 'oauth pass',

    # Customized settings for bot
    'channel': '#channelname',
    'joinmessage': 'JPUBot has joined the channel',

    # Commands that bot can use
    'commands': {
        '!addcom': 'addcom',
        '!motd': 'Message of the day.',
        '!test': 'Test command received.'
        
        # Custom commands added below
    }

    #FIXME: Add more settings to config
}

