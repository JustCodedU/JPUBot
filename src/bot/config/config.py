"""
Config file for settings for IRC Bot.
"""

global config

config = {

    # Basic bot configurations needed to log into irc server
    'server': 'irc.twitch.tv',
    'port': 6667,
    'username': 'justbottedyou',
    'oauthcode': 'oauth:4v9o783glqpf5kqjjyz8h347fxea04',

    # Customized settings for bot
    'channel': '#justpwnedu',
    'joinmessage': 'JPUBot has joined the channel.',
    'leavemessage': 'JPUBot Disconnecting from channel.',

    # Console output settings
    'debug': False,

    # Commands that bot can use
    # To enable set the value to True, to disable set the value to False
    'commands': {
        '!disconnect': True,
        '!addcom': True,
        '!remcom': True,
        '!motd': True,
        '!test': True,
        '!song': True,
        '!lastsong': True,
    },

    # File properties
    'properties': {
        'songpath': 'C:\\Users\\Admin\\Desktop\\Stream\\np.txt',
    },

    # Command values
    'values': {
        'motdvalue': 'Welcome to the channel!',
    }
}

