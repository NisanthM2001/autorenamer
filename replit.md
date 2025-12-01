# Channel File Processor Bot - PRODUCTION READY
## 🏷️ Version 01.01.01 (STABLE RELEASE)

## Overview

A professional Telegram bot that downloads files from source channels, applies dynamic filtering, intelligently renames files, and uploads to multiple destinations with real-time progress tracking. Features sequential file processing with an attractive, responsive UI showing detailed queue information and processing statistics.

## Project Structure

```
.
├── main.py              # Bot entry point
├── bot/
│   ├── __init__.py
│   ├── client.py        # Pyrogram client setup
│   ├── config.py        # Environment config
│   ├── filters.py       # File filtering logic
│   ├── handlers.py      # Bot command handlers
│   ├── processor.py     # Core file processing (sequential with real-time updates)
│   ├── database.py      # PostgreSQL storage
│   └── thumbnail.py     # Thumbnail management
├── downloads/           # Temporary downloads
├── thumbnails/          # Stored thumbnails
└── README.md
```

## ✨ Key Features

✅ **Real-Time Progress Updates** - Updates every 3 seconds with live speed, percentage, file name
✅ **Dynamic Language & Subtitles** - Auto-extracts language (English, Hindi, Telugu, Tamil, etc) and subtitles from filenames
✅ **Smart Captions** - Template-based captions with variables: {filename}, {filesize}, {language}, {subtitle}
✅ **Queue Display** - Shows minimum 5+ pending files with skip indicators and premium marks
✅ **Skip Indicators** - Files marked as: ✗ Skip, ⭐ Premium, ✓ Process
✅ **Processing Statistics** - Shows total processed + skipped counts in real-time
✅ **Whitelist/Blacklist Filtering** - Intelligent file filtering by keywords
✅ **Smart Renaming** - Replace underscores, remove @usernames, remove www patterns, case-sensitive word removal
✅ **Prefix/Suffix Support** - Add custom text to start/end of filenames
✅ **Multi-Channel Upload** - Upload to multiple destination channels simultaneously
✅ **Custom Thumbnails** - Set and manage custom thumbnails for all uploads
✅ **Message Range Processing** - Define start/end message links to process
✅ **Telegram Premium Support** - Handle files >2GB (requires premium user account)
✅ **Cancel All Button** - Instant cancellation stops downloads, uploads, and file handling
✅ **Persistent Settings** - All configurations saved to PostgreSQL database
✅ **Export/Import** - Backup and restore all settings as JSON
✅ **Clean Sequential Processing** - One file at a time, automatic queue advancement

## 🎨 Progress UI Layout

```
📥 DOWNLOADING 2/10

📄 current_file_2024.mkv

████████░░░░ 65%
💾 450MB / 680MB
🚀 2.3MB/s

━━━━━━━━━━━━━━━━━━
📊 STATS:
  📝 Total Processed: 2
  ⏳ Currently: Downloading

📋 QUEUE (8+):
  1. ✓ regular_file.mkv
  2. ⭐ premium_file.mkv (Premium)
  3. ✗ video.mkv (Skip - Blacklist)
  4. ✓ series.mkv
  5. ⭐ hd_movie.mkv (Premium)
  +3 more...

━━━━━━━━━━━━━━━━━━
✅ Processed: 2 | ⏭️ Skipped: 1
```

## 🔧 Environment Variables

| Variable | Description |
|----------|-------------|
| API_ID | Telegram API ID from my.telegram.org |
| API_HASH | Telegram API Hash |
| BOT_TOKEN | Bot token from @BotFather |
| OWNER_ID | Your Telegram user ID |
| DATABASE_URL | PostgreSQL connection string |

## 📱 Bot Commands

### Main Menu
- `/start` - Open main menu with interactive buttons
- `/help` - Detailed help text
- `/status` - Show current configuration

### Settings (via buttons)
- **Source Channels** - Set which channels to download from
- **Dest Channels** - Set upload destination channels
- **Whitelist/Blacklist** - Filter files by keywords
- **Remove Words** - Case-sensitive word removal from filenames
- **Prefix/Suffix** - Add to start/end of filenames
- **Remove Username** - Strip @username patterns from files
- **Set Caption** - Custom caption template with dynamic variables
- **Premium Mode** - Handle files >2GB (Telegram Premium users only)
- **Set Thumbnail** - Custom thumbnail for all uploads

### Processing
- `/setrange <start_link> <end_link>` - Define message range to process
- `/process` - Start sequential file processing
- **Cancel All Button** - Stop all downloads/uploads immediately

### File Management
- `/setthumb` - Reply to photo to set thumbnail
- `/delthumb` - Delete current thumbnail

## 📝 Filename Processing Pipeline

Automatic cleanup in this order:
1. Replace underscores with spaces
2. Remove @username patterns (if enabled)
3. Remove www.1tamilmv.* patterns
4. Remove specified words (case-sensitive)
5. Clean extra spaces
6. Add prefix/suffix
7. Preserve file extension

Example: `@user_old_file_2024.mkv` → `old file 2024.mkv`

## 🎬 Language & Subtitle Extraction

Automatically detects and extracts from filenames:
- **Languages**: English, Hindi, Telugu, Kannada, Tamil, Malayalam, Punjabi
- **Subtitles**: English, Hindi, Telugu, Kannada, Tamil, Malayalam, Punjabi

Used in dynamic captions: `{language}` and `{subtitle}` variables

## ⚙️ Processing Flow

1. **Fetch Phase** - Retrieves all messages in defined range
2. **Queue Phase** - Builds queue with skip reasons, premium indicators
3. **Download Phase** - Downloads file with real-time speed tracking
4. **Extract Phase** - Detects language/subtitle from filename
5. **Upload Phase** - Uploads to all destination channels with progress
6. **Cleanup Phase** - Removes temporary files
7. **Auto-Advance** - Next queued file automatically starts

## 📊 Processing Statistics

Real-time display of:
- `Total Processed` - Files successfully downloaded and uploaded
- `Skipped` - Files filtered or rejected
- `Currently` - Current operation (Downloading/Uploading)
- `Download Speed` - Current download speed
- `Upload Speed` - Current upload speed
- `Queue Count` - Number of pending files

## 💾 Database

- **PostgreSQL** - All settings persisted automatically
- **Auto-backup** - Use Export/Import for manual backups
- **Auto-restore** - Settings loaded on bot restart
- **Status** - Connected and fully operational

## 🚀 Deployment

### Development (Currently Running)
- Bot is running in development mode
- Settings persist across restarts
- Real-time progress updates working
- All features fully operational

### Production Deployment
1. Click **"Publish"** button (top-right in Replit)
2. Get public bot URL for 24/7 operation
3. Bot runs on dedicated VM instance
4. All settings persist automatically
5. Ready for immediate use in Telegram

## 📋 Latest Changes (Version 01.01.01 - STABLE)

✅ **File Count Tracking** - Total Found, To Process, Premium, Skipped counts
✅ **Reorganized UI** - Queue display first, then Progress + File Counts below
✅ **Current File Index** - Shows 1/10 (which file being processed vs total to process)
✅ **Completed Counter** - Only increments after successful download + upload
✅ **Dynamic Calculations** - Remaining = total - processed - skipped
✅ **Remove Words Append** - Send new words to ADD them, not replace. Clear All button to empty
✅ **Real-Time Queue** - Updates during both download and upload phases
✅ **Language Extraction** - Auto-detects English, Hindi, Telugu, Kannada, Tamil, Malayalam, Punjabi
✅ **Production Deployment** - VM deployment ready for 24/7 operation
✅ **All Features Stable** - Ready for immediate use

## ✨ Status

🟢 **VERSION 01.01.01 - STABLE RELEASE**

**See VERSION_HISTORY.md for checkpoint documentation**

This is a STABLE version that all future changes will build upon.
If any errors occur in future versions, reference this version.

- ✅ Sequential file processing working perfectly
- ✅ Real-time UI updates every 3 seconds  
- ✅ File counting displays all necessary metrics
- ✅ Queue display shows 5+ files with skip indicators
- ✅ Current file index correct (1/10 when processing first file)
- ✅ Completed count only increments after success
- ✅ Cancel button stops all operations instantly
- ✅ All settings persistent via PostgreSQL
- ✅ Production VM deployment configured
- ✅ Bot running and ready to use

**🎯 CHECKPOINT SAVED: VERSION 01.01.01**
**Ready to use! Send `/start` in Telegram to begin.**

---

## 🎯 Quick Start Guide

1. **Set Source Channel**: Click "Source Channels" and provide channel ID
2. **Set Destination**: Click "Dest Channels" and provide destination channel ID
3. **Set Range**: Send `/setrange <start_link> <end_link>` with message links
4. **Configure Filters** (Optional):
   - Add whitelist/blacklist keywords
   - Set prefix/suffix for filenames
   - Enable premium mode if needed
5. **Start Processing**: Click `/process` button
6. **Monitor Progress**: Watch real-time updates with speed, %, file name
7. **Cancel if Needed**: Click "Cancel All" to stop immediately

That's it! Your bot is ready to process files automatically.
