from os import getcwd
from prettyconf import Configuration
from prettyconf.loaders import EnvFile, Environment


env_file = f"{getcwd()}/.env"
config = Configuration(loaders=[Environment(), EnvFile(filename=env_file)])

DEV_USERS = [int(i) for i in config("DEV_USERS", default="1198820588").split()]
SUDO_USERS = [int(i) for i in config("SUDO_USERS", default="1198820588").split()]
OWNER_ID = int(config("OWNER_ID", default=1198820588))
