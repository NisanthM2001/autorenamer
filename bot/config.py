import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    # Read-only from env (API credentials)
    API_ID = 25713073
    API_HASH = "65a23aaa7a97f42475de52ed240af2f3"
    BOT_TOKEN = "8442496037:AAG6NX4eqPFVhI8THn9d5FhRBUeO5bg7BUw"
    SESSION_STRING = ""
    LOG_CHANNEL_ID = ""
    OWNER_ID = 6927710017
    DATABASE_URL = "mongodb+srv://autorenamer:autorenamer@autorenamer.nlb6zve.mongodb.net/?appName=Autorenamer"
    
    # Dynamic Admin IDs (loaded from MongoDB)
    ADMIN_IDS = []
    
    # Persistent settings (loaded from storage, not env)
    SOURCE_CHANNEL_IDS = []
    DESTINATION_CHANNEL_IDS = []
    WHITELIST_WORDS = []
    BLACKLIST_WORDS = []
    REMOVED_WORDS = []  # Words to remove from filename (case-sensitive exact match)
    FILE_PREFIX = ""
    FILE_SUFFIX = ""
    REMOVE_USERNAME = False
    CUSTOM_CAPTION = ""
    START_LINK = None
    END_LINK = None
    PROCESS_ABOVE_2GB = False  # Telegram Premium restriction
    
    DOWNLOAD_DIR = "downloads"
    THUMBNAIL_DIR = "thumbnails"
    
    @classmethod
    def is_configured(cls):
        return all([cls.API_ID, cls.API_HASH, cls.BOT_TOKEN, cls.OWNER_ID])
    
    @classmethod
    def get_info(cls):
        return {
            "api_configured": bool(cls.API_ID and cls.API_HASH),
            "bot_token_set": bool(cls.BOT_TOKEN),
            "source_channels": len(cls.SOURCE_CHANNEL_IDS),
            "destination_channels": len(cls.DESTINATION_CHANNEL_IDS),
            "log_channel_set": bool(cls.LOG_CHANNEL_ID),
            "whitelist_words": cls.WHITELIST_WORDS,
            "blacklist_words": cls.BLACKLIST_WORDS,
        }
