from pyrogram.client import Client
from bot.config import Config

from inspect import signature

def wztgClient(*args, **kwargs):
    if "max_concurrent_transmissions" in signature(Client.__init__).parameters:
        kwargs["max_concurrent_transmissions"] = 1000
    return Client(*args, **kwargs)

app = wztgClient(
    "bot_session",
    api_id=Config.API_ID,
    api_hash=Config.API_HASH,
    bot_token=Config.BOT_TOKEN,
    workdir=".",
    workers=1000
)

user_client = None
if Config.SESSION_STRING:
    user_client = Client(
        "user_session",
        api_id=Config.API_ID,
        api_hash=Config.API_HASH,
        session_string=Config.SESSION_STRING,
        workdir="."
    )
