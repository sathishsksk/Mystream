import os
import time
import datetime
import logging
import asyncio
import aiohttp
from config import Config
from database import Database
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, Message, CallbackQuery
from pyrogram.errors import FloodWait, UserIsBlocked, InputUserDeactivated
from utils.stream import generate_stream_links, get_media_info

# Koyeb compatibility
PORT = int(os.environ.get("PORT", 8000))

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

app = Client(
    "FileToLinkBot",
    api_id=Config.API_ID,
    api_hash=Config.API_HASH,
    bot_token=Config.BOT_TOKEN,
    in_memory=True,
    workers=4
)

db = Database(Config.DATABASE_URL, Config.BOT_USERNAME)

@app.on_message(filters.command("start") & filters.private)
async def start_command(client, message: Message):
    user_id = message.from_user.id
    if not await db.is_user_exist(user_id):
        await db.add_user(user_id)
        logger.info(f"New user added: {user_id}")
    
    await message.reply_text(
        text=Config.START_TEXT.format(message.from_user.mention),
        disable_web_page_preview=True,
        reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton("📢 Updates Channel", url="https://t.me/viperadnan"),
             InlineKeyboardButton("💬 Support Group", url="https://t.me/viperadnan_chat")],
            [InlineKeyboardButton("🤖 About", callback_data="about"),
             InlineKeyboardButton("🔧 Help", callback_data="help")]
        ])
    )

@app.on_message(filters.command("stats") & filters.user(Config.BOT_OWNER))
async def stats_command(client, message: Message):
    total_users = await db.total_users_count()
    await message.reply_text(f"📊 Bot Statistics:\n\n👥 Total Users: {total_users}")

@app.on_message(filters.private & (
    filters.document | 
    filters.video | 
    filters.audio | 
    filters.photo
))
async def file_handler(client, message: Message):
    try:
        user_id = message.from_user.id
        if not await db.is_user_exist(user_id):
            await db.add_user(user_id)
        
        media = message.document or message.video or message.audio or message.photo
        file_name = getattr(media, 'file_name', None) or f"file_{message.id}"
        file_size = media.file_size
        
        if file_size > Config.MAX_FILE_SIZE:
            await message.reply_text(
                f"❌ File size exceeds maximum limit!\n"
                f"📦 Your file: {humanbytes(file_size)}\n"
                f"⚡ Maximum allowed: {humanbytes(Config.MAX_FILE_SIZE)}"
            )
            return
        
        # Check if media is streamable
        is_streamable = any([
            message.video,
            message.audio,
            message.document and any(x in message.document.mime_type for x in ['video', 'audio', 'pdf'])
        ])
        
        msg = await message.reply_text("📥 Downloading your file...")
        file_path = await message.download()
        
        await msg.edit_text("🔗 Generating download links...")
        
        # Generate streaming links for streamable media
        if is_streamable and Config.STREAMING_ENABLED:
            stream_links = await generate_stream_links(file_path, file_name)
            await db.add_file_record(
                file_id=media.file_id,
                file_name=file_name,
                file_size=file_size,
                download_link=stream_links['direct'],
                stream_links=stream_links,
                user_id=user_id
            )
            
            # Create streaming keyboard
            keyboard = []
            if stream_links.get('direct'):
                keyboard.append([InlineKeyboardButton("📥 Direct Download", url=stream_links['direct'])])
            if stream_links.get('stream'):
                keyboard.append([InlineKeyboardButton("🎥 Stream Online", url=stream_links['stream'])])
            if stream_links.get('preview'):
                keyboard.append([InlineKeyboardButton("👀 Preview", url=stream_links['preview'])])
            
            keyboard.append([InlineKeyboardButton("🔗 Share", url=f"https://t.me/share/url?url={stream_links['direct']}")])
            
            await msg.edit_text(
                text=f"**✅ File Ready!**\n\n"
                     f"**📁 File Name:** `{file_name}`\n"
                     f"**📦 File Size:** {humanbytes(file_size)}\n"
                     f"**🎬 Streamable:** {'Yes' if is_streamable else 'No'}\n\n"
                     f"**Choose an option below:**",
                reply_markup=InlineKeyboardMarkup(keyboard)
            )
        else:
            # Non-streamable files
            download_link = f"{Config.DOWNLOAD_URL}/files/{os.path.basename(file_path)}"
            await db.add_file_record(
                file_id=media.file_id,
                file_name=file_name,
                file_size=file_size,
                download_link=download_link,
                user_id=user_id
            )
            
            await msg.edit_text(
                text=f"**✅ File Ready!**\n\n"
                     f"**📁 File Name:** `{file_name}`\n"
                     f"**📦 File Size:** {humanbytes(file_size)}\n\n"
                     f"**🔗 Download Link:**\n`{download_link}`",
                reply_markup=InlineKeyboardMarkup([
                    [InlineKeyboardButton("📥 Download", url=download_link)],
                    [InlineKeyboardButton("🔗 Share", url=f"https://t.me/share/url?url={download_link}")]
                ])
            )
            
    except Exception as e:
        logger.error(f"File handling error: {e}")
        await message.reply_text("❌ Error processing your file. Please try again.")

@app.on_callback_query(filters.regex("^about$"))
async def about_callback(client, callback_query: CallbackQuery):
    await callback_query.answer()
    await callback_query.message.edit_text(
        text=Config.ABOUT_TEXT,
        disable_web_page_preview=True,
        reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton("🏠 Home", callback_data="home"),
             InlineKeyboardButton("🔒 Close", callback_data="close")]
        ])
    )

@app.on_callback_query(filters.regex("^help$"))
async def help_callback(client, callback_query: CallbackQuery):
    await callback_query.answer()
    await callback_query.message.edit_text(
        text=Config.HELP_TEXT,
        disable_web_page_preview=True,
        reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton("🏠 Home", callback_data="home"),
             InlineKeyboardButton("🔒 Close", callback_data="close")]
        ])
    )

@app.on_callback_query(filters.regex("^home$"))
async def home_callback(client, callback_query: CallbackQuery):
    await callback_query.answer()
    await callback_query.message.edit_text(
        text=Config.START_TEXT.format(callback_query.from_user.mention),
        disable_web_page_preview=True,
        reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton("📢 Updates Channel", url="https://t.me/viperadnan"),
             InlineKeyboardButton("💬 Support Group", url="https://t.me/viperadnan_chat")],
            [InlineKeyboardButton("🤖 About", callback_data="about"),
             InlineKeyboardButton("🔧 Help", callback_data="help")]
        ])
    )

@app.on_callback_query(filters.regex("^close$"))
async def close_callback(client, callback_query: CallbackQuery):
    await callback_query.message.delete()

@app.on_message(filters.command("broadcast") & filters.user(Config.BOT_OWNER) & filters.reply)
async def broadcast_handler(client, message: Message):
    all_users = await db.get_all_users()
    broadcast_msg = message.reply_to_message
    total_users = len(all_users)
    success = 0
    
    progress_msg = await message.reply_text(f"📤 Broadcasting to {total_users} users...")
    
    for user_id in all_users:
        try:
            await broadcast_msg.copy(user_id)
            success += 1
            if success % 100 == 0:
                await progress_msg.edit_text(f"📤 Broadcast progress: {success}/{total_users}")
        except FloodWait as e:
            await asyncio.sleep(e.value)
        except (UserIsBlocked, InputUserDeactivated):
            await db.delete_user(user_id)
        except Exception as e:
            logger.error(f"Broadcast error for {user_id}: {e}")
    
    await progress_msg.edit_text(f"✅ Broadcast completed!\nSuccess: {success}\nFailed: {total_users - success}")

def humanbytes(size):
    if not size:
        return "0 B"
    power = 2**10
    n = 0
    units = {0: 'B', 1: 'KB', 2: 'MB', 3: 'GB', 4: 'TB'}
    while size > power:
        size /= power
        n += 1
    return f"{round(size, 2)} {units[n]}"

# Koyeb health check
@app.on_message(filters.command("ping"))
async def ping_command(client, message: Message):
    start_time = time.time()
    msg = await message.reply_text("🏓 Pong!")
    end_time = time.time()
    await msg.edit_text(f"🏓 Pong! `{round((end_time - start_time) * 1000, 2)}ms`")

if __name__ == "__main__":
    print("🚀 Starting File to Link Bot with Streaming on Koyeb...")
    logger.info("Bot is starting...")
    app.run()
