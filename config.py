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
    'motd': 'Message of the day.',
    'joinmessage': 'JPUBot has joined the channel',

    # Commands that bot can use
    'commands': {
        '!addcom': 'addcom',
        '!minik': 'tfw no turbo T-T',
        '!test': 'Test command received.'
    }
    # End of commands


    #FIXME: Add more settings to config
}

