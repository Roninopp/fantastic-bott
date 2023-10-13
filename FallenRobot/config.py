class Config(object):
    LOGGER = True

  # Get this value from my.telegram.org/apps
    API_ID = "7217645"
    API_HASH = "78ba6352dd5cdc166fdef5aa84ba7c67"
    VIRUS_API_KEY = "rffr"
    CASH_API_KEY = ""  # Get this value for currency converter from https://www.alphavantage.co/support/#api-key
    BOT_ID = 2291
    DATABASE_URL = "postgres://ncttyari:DvjEut7QzjPAaTC59QkgBGyO8361YmiU@trumpet.db.elephantsql.com/ncttyari"  # A sql database url from elephantsql.com
    SQLALCHEMY_DATABASE_URI = "postgres://ncttyari:DvjEut7QzjPAaTC59QkgBGyO8361YmiU@trumpet.db.elephantsql.com/ncttyari"
    EVENT_LOGS = (-1001966188512)  # Event logs channel to note down important bot level events
    JOIN_LOGGER = (-1001966188512)
    OPENWEATHERMAP_ID = 1212
    MONGO_DB = "mongodb+srv://gabimaru:gabi123@cluster0.p8qlfbe.mongodb.net/?retryWrites=true&w=majority"
    REDIS_URL = "redis://:dplEdSkGkGs0WCs7J2XdGRSLgQL0HHGT@redis-10625.c99.us-east-1-4.ec2.cloud.redislabs.com:10625"
    DONATION_LINK = "ewfewfe"
    ERROR_LOGS = (-1001709251588)
  
    AI_API_KEY = ""
    ARQ_API_KEY = ""
    ARQ_API_URL = "gay"

    MONGO_DB_URI = "mongodb+srv://gabimaru:gabi123@cluster0.p8qlfbe.mongodb.net/?retryWrites=true&w=majority"  # Get ths value from cloud.mongodb.com

  # Telegraph link of the image which will be shown at start command.
    START_IMG = "https://telegra.ph/file/065b18d37a25206190fab.jpg"

    SUPPORT_CHAT = "SpiralTechDivision"  # Your Telegram support group chat username where your users will go and bother you

    TOKEN = "2100096282:AAFYKUba5wJWPvu4zJfAWkMWy6xcI66wFQM"  # Get bot token from @BotFather on Telegram

    TIME_API_KEY = ""  # Get this value from https://timezonedb.com/api
    SPAMWATCH_SUPPORT_CHAT = "effr"
    SPAMWATCH_API = "wdwd"
    OWNER_ID = 5965096598  # User id of your telegram account (Must be integer)
    OWNER_USERNAME = "DUSHMANxRONIN"
    WEBHOOK = False
    URL = "api.telegram.org"
    PORT = 5000
    WALL_API = "qrew"
    
  # Optional fields
    BL_CHATS = []  # List of groups that you want blacklisted.
    DRAGONS = [1737646273,5654523936,]  # User id of sudo users
    DEV_USERS = [6040984893]  # User id of dev users
    DEMONS = []  # User id of support users
    TIGERS = []  # User id of tiger users
    WOLVES = []  # User id of whitelist users

    ALLOW_CHATS = True
    ALLOW_EXCL = True
    DEL_CMDS = True
    INFOPIC = True
    CERT_PATH = "sasa"
    LOAD = []
    NO_LOAD = []
    STRICT_GBAN = True
    TEMP_DOWNLOAD_DIRECTORY = "./"
    WORKERS = (8)
    BAN_STICKER = "fee"

class Production(Config):
    LOGGER = True

class Development(Config):
    LOGGER = True

class configClass:
    host = 'gcp.connect.psdb.cloud'  # host name from planetscale.com for sql database
    user = 'i4lmpe9j2lsgw0oc9fcq'  # username from planetscale.com for sql database
    password = 'pscale_pw_5aiifymoD3wZIkq3b36V7da3w60FTPiRfWKWFjuin8R'
    database = 'fantastic_bot'
    url = f"mysql://{user}:{password}@{host}/{database}"
    ssl_ca = r"FallenRobot/cacert.pem"
    mongoURL = "mongodb+srv://samurai557:samurai0000@cluster0.su1rrtd.mongodb.net/?retryWrites=true&w=majority"
