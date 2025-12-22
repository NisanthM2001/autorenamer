import os
try:
    from PIL import Image
    PIL_AVAILABLE = True
except ImportError:
    PIL_AVAILABLE = False
    print("⚠️ Pillow not installed. Thumbnail support disabled.")
from bot.config import Config
from bot.database import save_thumbnail_image, delete_thumbnail_image, load_thumbnail_image_sync

THUMBNAIL_PATH = os.path.join(Config.THUMBNAIL_DIR, "default_thumb.jpg")

async def save_thumbnail(photo_path: str) -> bool:
    if not PIL_AVAILABLE:
        return False
        
    try:
        os.makedirs(Config.THUMBNAIL_DIR, exist_ok=True)
        
        # 1. Process and save to local disk
        with Image.open(photo_path) as img:
            img = img.convert("RGB")
            img.thumbnail((320, 320))
            img.save(THUMBNAIL_PATH, "JPEG", quality=85)
            
        # 2. Read bytes and save to DB
        with open(THUMBNAIL_PATH, 'rb') as f:
            image_data = f.read()
            await save_thumbnail_image(image_data)
        
        return True
    except Exception as e:
        print(f"Error saving thumbnail: {e}")
        return False

def get_thumbnail() -> str | None:
    if os.path.exists(THUMBNAIL_PATH):
        return THUMBNAIL_PATH
    return None

async def delete_thumbnail() -> bool:
    try:
        # 1. Delete from local disk
        if os.path.exists(THUMBNAIL_PATH):
            os.remove(THUMBNAIL_PATH)
            
        # 2. Delete from DB
        await delete_thumbnail_image()
        return True
    except Exception as e:
        print(f"Error deleting thumbnail: {e}")
        return False

def has_thumbnail() -> bool:
    return os.path.exists(THUMBNAIL_PATH)

def init_thumbnail():
    """Restore thumbnail from DB on startup"""
    try:
        os.makedirs(Config.THUMBNAIL_DIR, exist_ok=True)
        if not os.path.exists(THUMBNAIL_PATH):
            print("Checking DB for saved thumbnail...")
            data = load_thumbnail_image_sync()
            if data:
                with open(THUMBNAIL_PATH, 'wb') as f:
                    f.write(data)
                print("✅ Restored thumbnail from DB")
    except Exception as e:
        print(f"Error restoring thumbnail: {e}")

# Run restoration on import/startup
init_thumbnail()
