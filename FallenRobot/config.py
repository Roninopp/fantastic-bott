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
    EVENT_LOGS = (-1001709251588)  # Event logs channel to note down important bot level events
    JOIN_LOGGER = (-1001709251588)
    OPENWEATHERMAP_ID = 1212
    MONGO_DB = "mongodb+srv://gabimaru:gabi123@cluster0.p8qlfbe.mongodb.net/?retryWrites=true&w=majority"
    REDIS_URL = "redis://:dplEdSkGkGs0WCs7J2XdGRSLgQL0HHGT@redis-10625.c99.us-east-1-4.ec2.cloud.redislabs.com:10625"
    OPENAI_API_KEY = "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"
    DONATION_LINK = "ewfewfe"
    ERROR_LOGS = (-1001709251588)
  
    AI_API_KEY = ""
    ARQ_API_KEY = ""
    ARQ_API_URL = "gay"

    MONGO_DB_URI = "mongodb+srv://gabimaru:gabi123@cluster0.p8qlfbe.mongodb.net/?retryWrites=true&w=majority"  # Get ths value from cloud.mongodb.com

  # Telegraph link of the image which will be shown at start command.
    START_IMG = "https://telegra.ph/file/9cb02986d9999d2fecf82.jpg"

    SUPPORT_CHAT = "samurai_botsupport"  # Your Telegram support group chat username where your users will go and bother you

    TOKEN = "2100096282:AAF02uGaMkBtBS9vGMm0E0ltKNsdpYi7des"  # Get bot token from @BotFather on Telegram

    TIME_API_KEY = ""  # Get this value from https://timezonedb.com/api
    SPAMWATCH_SUPPORT_CHAT = "effr"
    SPAMWATCH_API = "wdwd"
    OWNER_ID = 1793699293  # User id of your telegram account (Must be integer)
    OWNER_USERNAME = "DUSHMANxRONIN"
    WEBHOOK = False
    URL = "api.telegram.org"
    PORT = 5000
    WALL_API = "qrew"
    
  # Optional fields
    BL_CHATS = []  # List of groups that you want blacklisted.
    DRAGONS = [5274479443,5916768852]  # User id of sudo users
    DEV_USERS = []  # User id of dev users
    DEMONS = [1737646273,1669062342,1811267624]  # User id of support users
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
