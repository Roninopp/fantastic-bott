class Config(object):
    LOGGER = True

  # Get this value from my.telegram.org/apps
    API_ID = 14980683
    API_HASH = "5bc2e9cd58092119e741c1f2b545c1bf"

    CASH_API_KEY = "VQ45LFKYPMJ2LKIU"  # Get this value for currency converter from https://www.alphavantage.co/support/#api-key

    DATABASE_URL = "postgres://afgncjpn:GfV4VDYU9dNtNfZ5Pzqs_nK1QxLXC5IJ@lallah.db.elephantsql.com/afgncjpn"  # A sql database url from elephantsql.com

    EVENT_LOGS = (-1001739283144)  # Event logs channel to note down important bot level events
    
    MONGO_DB = "Shikimori"

    ERROR_LOGS = -1001164614215

    AI_API_KEY = "SOME1HING_privet_990022"

    MONGO_DB_URI = "mongodb+srv://eren:eren@cluster0.yxuwg4r.mongodb.net/?retryWrites=true&w=majority"  # Get ths value from cloud.mongodb.com

  # Telegraph link of the image which will be shown at start command.
    START_IMG = "https://graph.org/file/aa18cfd060aa74f1b7634.jpg"

    SUPPORT_CHAT = "WoFBotsSupport"  # Your Telegram support group chat username where your users will go and bother you

    TOKEN = "5714818526:AAF0Jdauk9Mrb44bEypi0LzQiNIza-ojb68"  # Get bot token from @BotFather on Telegram

    TIME_API_KEY = "65G8ZKE6050P"  # Get this value from https://timezonedb.com/api

    OWNER_ID = 5667156680  # User id of your telegram account (Must be integer)

  # Optional fields
    BL_CHATS = []  # List of groups that you want blacklisted.
    DRAGONS = []  # User id of sudo users
    DEV_USERS = []  # User id of dev users
    DEMONS = []  # User id of support users
    TIGERS = []  # User id of tiger users
    WOLVES = []  # User id of whitelist users

    ALLOW_CHATS = True
    ALLOW_EXCL = True
    DEL_CMDS = True
    INFOPIC = True
    LOAD = []
    NO_LOAD = []
    STRICT_GBAN = True
    TEMP_DOWNLOAD_DIRECTORY = "./"
    WORKERS = (8)

class Production(Config):
    LOGGER = True

class Development(Config):
    LOGGER = True
