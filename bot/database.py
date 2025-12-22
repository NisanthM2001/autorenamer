import os
import json
from datetime import datetime
try:
    from pymongo import MongoClient
    from pymongo.errors import ConnectionFailure
    MONGO_AVAILABLE = True
except ImportError:
    MONGO_AVAILABLE = False
    print("[WARNING] pymongo not installed. Using in-memory settings only.")

from bot.config import Config
import certifi

ca = certifi.where()

# Database connection
DATABASE_URL = Config.DATABASE_URL
db_client = None
db = None
settings_collection = None
thumbnails_collection = None
admins_collection = None

# In-memory fallback
in_memory_settings = {
    "source_channels": [],
    "destination_channels": [],
    "whitelist_words": [],
    "blacklist_words": [],
    "removed_words": [],
    "file_prefix": "",
    "file_suffix": "",
    "remove_username": False,
    "custom_caption": "",
    "start_link": None,
    "end_link": None,
    "process_above_2gb": False,
    "parallel_downloads": 1
}

def init_db():
    """Initialize MongoDB connection"""
    global db_client, db, settings_collection
    
    if not MONGO_AVAILABLE:
        return False
    
    if not DATABASE_URL:
        print("[WARNING] No DATABASE_URL found. Using in-memory settings.")
        return False
        
    try:
        # Use certifi for SSL/TLS certificates
        db_client = MongoClient(
            DATABASE_URL, 
            tlsCAFile=ca,
            tlsAllowInvalidCertificates=True, 
            serverSelectionTimeoutMS=5000
        )
        # Test connection
        db_client.admin.command('ping')
        
        db = db_client.get_database("telegram_bot_db")
        settings_collection = db.get_collection("settings")
        thumbnails_collection = db.get_collection("thumbnails")
        admins_collection = db.get_collection("admins")
        
        print("[SUCCESS] Connected to MongoDB")
        return True
    except Exception as e:
        print(f"[ERROR] MongoDB connection error: {e}")
        return False

# Initialize on startup
init_db()

def load_settings_sync():
    """Synchronously load settings from MongoDB or memory at startup"""
    global in_memory_settings
    
    if settings_collection is not None:
        try:
            doc = settings_collection.find_one({"_id": "main_settings"})
            if doc:
                # Merge with defaults to ensure all keys exist
                loaded = {**in_memory_settings, **doc}
                # Remove internal mongo id
                if "_id" in loaded:
                    # Keep _id as "main_settings", but we update our in-memory dict
                    pass
                
                in_memory_settings = {
                    "source_channels": loaded.get("source_channels", []),
                    "destination_channels": loaded.get("destination_channels", []),
                    "whitelist_words": loaded.get("whitelist_words", []),
                    "blacklist_words": loaded.get("blacklist_words", []),
                    "removed_words": loaded.get("removed_words", []),
                    "file_prefix": loaded.get("file_prefix", ""),
                    "file_suffix": loaded.get("file_suffix", ""),
                    "remove_username": loaded.get("remove_username", False),
                    "custom_caption": loaded.get("custom_caption", ""),
                    "start_link": loaded.get("start_link"),
                    "end_link": loaded.get("end_link"),
                    "process_above_2gb": loaded.get("process_above_2gb", False),
                    "parallel_downloads": loaded.get("parallel_downloads", 1)
                }
                print(f"[SUCCESS] Settings loaded from MongoDB")
                return in_memory_settings
        except Exception as e:
            print(f"[ERROR] Error loading from MongoDB: {e}")
            
    print(f"[SUCCESS] Using in-memory settings")
    return in_memory_settings

async def load_settings():
    """Load all settings (wrapper for sync since pymongo is sync)"""
    return load_settings_sync()

async def save_settings(settings_dict):
    """Save settings to MongoDB or memory"""
    global in_memory_settings
    
    in_memory_settings = settings_dict
    
    if settings_collection is not None:
        try:
            # Prepare document
            doc = settings_dict.copy()
            doc["_id"] = "main_settings"
            doc["updated_at"] = datetime.utcnow()
            
            settings_collection.replace_one(
                {"_id": "main_settings"},
                doc,
                upsert=True
            )
        except Exception as e:
            print(f"[ERROR] Error saving settings to MongoDB: {e}")

async def update_setting(key, value):
    """Update a single setting"""
    global in_memory_settings
    
    in_memory_settings[key] = value
    
    if settings_collection is not None:
        try:
            settings_collection.update_one(
                {"_id": "main_settings"},
                {"$set": {key: value, "updated_at": datetime.utcnow()}},
                upsert=True
            )
        except Exception as e:
            print(f"[ERROR] Error updating setting in MongoDB: {e}")

async def delete_setting(key):
    """Delete a specific setting (reset to default)"""
    global in_memory_settings
    
    defaults = {
        "source_channels": [],
        "destination_channels": [],
        "whitelist_words": [],
        "blacklist_words": [],
        "removed_words": [],
        "file_prefix": "",
        "file_suffix": "",
        "remove_username": False,
        "custom_caption": "",
        "start_link": None,
        "end_link": None,
        "process_above_2gb": False,
        "parallel_downloads": 1
    }
    
    if key in defaults:
        val = defaults[key]
        in_memory_settings[key] = val
        await update_setting(key, val)

async def save_backup(settings_dict):
    """Save settings to backup in MongoDB"""
    if settings_collection is not None:
        try:
            doc = settings_dict.copy()
            doc["_id"] = "backup_settings"
            doc["updated_at"] = datetime.utcnow()
            
            settings_collection.replace_one(
                {"_id": "backup_settings"},
                doc,
                upsert=True
            )
            print("[SUCCESS] Backup saved successfully to MongoDB")
            return True
        except Exception as e:
            print(f"[ERROR] Error saving backup: {e}")
            return False
    return False

async def load_backup():
    """Load settings from MongoDB backup"""
    if settings_collection is not None:
        try:
            doc = settings_collection.find_one({"_id": "backup_settings"})
            if doc:
                return {
                    "source_channels": doc.get("source_channels", []),
                    "destination_channels": doc.get("destination_channels", []),
                    "whitelist_words": doc.get("whitelist_words", []),
                    "blacklist_words": doc.get("blacklist_words", []),
                    "removed_words": doc.get("removed_words", []),
                    "file_prefix": doc.get("file_prefix", ""),
                    "file_suffix": doc.get("file_suffix", ""),
                    "remove_username": doc.get("remove_username", False),
                    "custom_caption": doc.get("custom_caption", ""),
                    "start_link": doc.get("start_link"),
                    "end_link": doc.get("end_link"),
                    "process_above_2gb": doc.get("process_above_2gb", False),
                    "parallel_downloads": doc.get("parallel_downloads", 1)
                }
        except Exception as e:
            print(f"[ERROR] Error loading backup: {e}")
    return None

async def save_thumbnail_image(image_data: bytes):
    """Save thumbnail binary to MongoDB"""
    if thumbnails_collection is not None:
        try:
            thumbnails_collection.replace_one(
                {"_id": "main_thumbnail"},
                {"_id": "main_thumbnail", "data": image_data, "updated_at": datetime.utcnow()},
                upsert=True
            )
            return True
        except Exception as e:
            print(f"[ERROR] Error saving thumbnail to DB: {e}")
            return False
    return False

async def load_thumbnail_image():
    """Load thumbnail binary from MongoDB"""
    if thumbnails_collection is not None:
        try:
            doc = thumbnails_collection.find_one({"_id": "main_thumbnail"})
            if doc and "data" in doc:
                return doc["data"]
        except Exception as e:
            print(f"[ERROR] Error loading thumbnail from DB: {e}")
    return None

def load_thumbnail_image_sync():
    """Sync load thumbnail (for startup)"""
    if thumbnails_collection is not None:
        try:
            doc = thumbnails_collection.find_one({"_id": "main_thumbnail"})
            if doc and "data" in doc:
                return doc["data"]
        except Exception as e:
            print(f"[ERROR] Error loading thumbnail from DB: {e}")
    return None

async def delete_thumbnail_image():
    """Delete thumbnail from MongoDB"""
    if thumbnails_collection is not None:
        try:
            thumbnails_collection.delete_one({"_id": "main_thumbnail"})
            return True
        except Exception as e:
            print(f"[ERROR] Error deleting thumbnail from DB: {e}")
            return False
    return False

# Admin Management
async def add_admin(user_id: int):
    """Add a new admin to MongoDB"""
    global admins_collection
    if admins_collection is not None:
        try:
            admins_collection.replace_one(
                {"user_id": user_id},
                {"user_id": user_id, "added_at": datetime.utcnow()},
                upsert=True
            )
            # Update local memory
            from bot.config import Config
            if user_id not in Config.ADMIN_IDS:
                Config.ADMIN_IDS.append(user_id)
            return True
        except Exception as e:
            print(f"[ERROR] Error adding admin: {e}")
    return False

async def remove_admin(user_id: int):
    """Remove an admin from MongoDB"""
    global admins_collection
    if admins_collection is not None:
        try:
            admins_collection.delete_one({"user_id": user_id})
            # Update local memory
            from bot.config import Config
            if user_id in Config.ADMIN_IDS:
                Config.ADMIN_IDS.remove(user_id)
            return True
        except Exception as e:
            print(f"[ERROR] Error removing admin: {e}")
    return False

def load_admins_sync():
    """Load all admins from MongoDB into memory"""
    global admins_collection
    admin_ids = []
    if admins_collection is not None:
        try:
            cursor = admins_collection.find({})
            for doc in cursor:
                admin_ids.append(doc["user_id"])
        except Exception as e:
            print(f"[ERROR] Error loading admins: {e}")
    return admin_ids
