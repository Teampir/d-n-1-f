from os import getcwd
from prettyconf import Configuration
from prettyconf.loaders import EnvFile, Environment


env_file = f"{getcwd()}/.env"
config = Configuration(loaders=[Environment(), EnvFile(filename=env_file)])

class Config:
    """Config class for variables."""
    
ENABLED_LOCALES = [str(i) for i in config("ENABLED_LOCALES", default="en").split()]
DEV_USERS = [int(i) for i in config("DEV_USERS", default="1198820588").split()]
SUDO_USERS = [int(i) for i in config("SUDO_USERS", default="1198820588").split()]
OWNER_ID = int(config("OWNER_ID", default=1198820588))
SUPPORT_STAFF = int(config("SUPPORT_STAFF", default=1198820588))

class Development:
    """Development class for variables."""
    
ENABLED_LOCALES = ["ENABLED_LOCALES"]
OWNER_ID = 12345  # Your telegram user id
DEV_USERS = []
SUDO_USERS = []
