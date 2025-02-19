from environs import Env

env = Env()
env.read_env()

BOT_TOKEN = env.str("BOT_TOKEN")
ADMINS = env.list("ADMINS")
CHANNEL_ID = env.str("CHANNEL_ID")

# CHANNEL_USERNAME = env.str("CHANNEL_USERNAME")
IP = env.str("ip")
