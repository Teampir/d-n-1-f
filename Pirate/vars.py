from os import getcwd

from prettyconf import Configuration
from prettyconf.loaders import EnvFile, Environment

env_file = f"{getcwd()}/.env"
config = Configuration(loaders=[Environment(), EnvFile(filename=env_file)])


class Config:
    """Config class for variables."""

    LOGGER = True
    BOT_TOKEN = config("BOT_TOKEN", default="5333465495:AAFE01xmdiiwlxbOdmfaXvMEUdpa3MEUEvI")
    APP_ID = int(config("APP_ID", default=11861664))
    API_HASH = config("API_HASH", default="f1467da97808a3546f35cad95db72fd2")
    OWNER_ID = int(config("OWNER_ID", default=1158680997))
    MESSAGE_DUMP = int(config("MESSAGE_DUMP", default=-100))
    DEV_USERS = [int(i) for i in config("DEV_USERS", default="1158680997").split()]
    SUDO_USERS = [int(i) for i in config("SUDO_USERS", default="1158680997").split()]
    WHITELIST_USERS = [int(i) for i in config("WHITELIST_USERS", default="1158680997").split()]
    DB_URI = config("DB_URI", default="mongodb+srv://Minnal:minnal@cluster0.gdq2z.mongodb.net/?retryWrites=true&w=majority")
    DB_NAME = config("DB_NAME", default="alita_robot")
    NO_LOAD = config("NO_LOAD", default="").split()
    PREFIX_HANDLER = config("PREFIX_HANDLER", default="/").split()
    SUPPORT_GROUP = config("SUPPORT_GROUP", default="DivideProjectsDiscussion")
    SUPPORT_CHANNEL = config("SUPPORT_CHANNEL", default="DivideProjects")
    ENABLED_LOCALES = [str(i) for i in config("ENABLED_LOCALES", default="en").split()]
    VERSION = config("VERSION", default="v2.0")
    WORKERS = int(config("WORKERS", default=16))
    BOT_USERNAME = ""
    BOT_ID = ""
    BOT_NAME = ""


class Development:
    """Development class for variables."""

    # Fill in these vars if you want to use Traditional method of deploying
    LOGGER = True
    BOT_TOKEN = "5333465495:AAFE01xmdiiwlxbOdmfaXvMEUdpa3MEUEvI"
    APP_ID = 11861664  # Your APP_ID from Telegram
    API_HASH = "f1467da97808a3546f35cad95db72fd2"  # Your APP_HASH from Telegram
    OWNER_ID = 1158680997  # Your telegram user id
    MESSAGE_DUMP = -100  # Your Private Group ID for logs
    DEV_USERS = []
    SUDO_USERS = []
    WHITELIST_USERS = []
    DB_URI = "mongodb+srv://Minnal:minnal@cluster0.gdq2z.mongodb.net/?retryWrites=true&w=majority"
    DB_NAME = "alita_robot"
    NO_LOAD = []
    PREFIX_HANDLER = ["!", "/"]
    SUPPORT_GROUP = "SUPPORT_GROUP"
    SUPPORT_CHANNEL = "SUPPORT_CHANNEL"
    ENABLED_LOCALES = ["ENABLED_LOCALES"]
    VERSION = "VERSION"
    WORKERS = 8
