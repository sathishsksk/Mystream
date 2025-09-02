import os

class Config:
    # Koyeb Environment Variables
    API_ID = int(os.environ.get("API_ID", "1234567"))
    API_HASH = os.environ.get("API_HASH", "your_api_hash_here")
    BOT_TOKEN = os.environ.get("BOT_TOKEN", "your_bot_token_here")
    BOT_USERNAME = os.environ.get("BOT_USERNAME", "your_bot_username")
    BOT_OWNER = int(os.environ.get("BOT_OWNER", "123456789"))
    DATABASE_URL = os.environ.get("DATABASE_URL", "your_mongodb_url_here")
    DOWNLOAD_URL = os.environ.get("DOWNLOAD_URL", "https://your-domain.com")
    
    # File and Streaming Settings
    MAX_FILE_SIZE = int(os.environ.get("MAX_FILE_SIZE", "4294967296"))  # 4GB
    STREAMING_ENABLED = bool(os.environ.get("STREAMING_ENABLED", True))
    MAX_STREAM_SIZE = int(os.environ.get("MAX_STREAM_SIZE", "2147483648"))  # 2GB
    STREAM_CHUNK_SIZE = int(os.environ.get("STREAM_CHUNK_SIZE", "1048576"))  # 1MB
    STREAMING_BUFFER_SIZE = int(os.environ.get("STREAMING_BUFFER_SIZE", "65536"))  # 64KB
    
    # Text Messages
    START_TEXT = """👋 Hello {},\n\n🤖 **Welcome to File to Link Bot!**\n\nI can convert your files into direct download links with streaming support!\n\n**✨ Features:**\n✅ Files up to 4GB\n✅ Video & Audio Streaming\n✅ Fast Download Links\n✅ Secure & Private\n\n**📤 Just send me any file and I'll generate a link for you!**"""
    
    ABOUT_TEXT = """🤖 **About File to Link Bot**\n\n**Version:** 2.0\n**Developer:** @viperadnan\n**Platform:** Koyeb\n\n**🔧 Features:**\n• File to Direct Link Conversion\n• Video & Audio Streaming\n• Multi-Quality Support\n• MongoDB Database\n• Broadcast Messages\n• User Management\n\n**📊 Technical:**\n• Pyrogram Framework\n• Motor Async MongoDB\n• Koyeb Deployment\n• CDN Support\n\n**🌐 Source Code:** [GitHub](https://github.com/viperadnan-git/file-to-link-bot)"""
    
    HELP_TEXT = """📖 **How to Use:**\n\n1. **Send any file** (document, video, audio, photo)\n2. **Wait for processing** (I'll download your file)\n3. **Get download link** (direct link + streaming options)\n4. **Share the link** with anyone\n\n**📁 Supported Files:**\n• Documents (PDF, ZIP, etc.) - Up to 4GB\n• Videos (MP4, MKV, etc.) - Up to 2GB streaming\n• Audio (MP3, WAV, etc.) - Up to 2GB streaming\n• Images (JPG, PNG, etc.)\n\n**⚡ Streaming Features:**\n• Video streaming with progress\n• Audio streaming with quality options\n• Direct download links\n• Shareable links\n\n**🔧 Commands:**\n/start - Start the bot\n/stats - Bot statistics (admin only)\n/broadcast - Broadcast message (admin only)\n/ping - Check bot latency\n\n**Need help?** Contact @viperadnan"""
