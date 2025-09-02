# File to Link Bot with Streaming

A Telegram bot that converts files to direct download links with streaming capabilities, deployed on Koyeb.

## Features

- ✅ File to direct link conversion
- ✅ Video & audio streaming
- ✅ Support for files up to 4GB
- ✅ MongoDB database
- ✅ User management
- ✅ Broadcast messages
- ✅ Koyeb deployment optimized

## Koyeb Deployment

1. **Fork this repository**
2. **Create secrets in Koyeb dashboard:**
   - `api-id`: Your Telegram API_ID
   - `api-hash`: Your Telegram API_HASH  
   - `bot-token`: Your bot token from @BotFather
   - `database-url`: MongoDB connection string

3. **Connect GitHub repository to Koyeb**
4. **Deploy automatically**

## Environment Variables

| Variable | Description | Required |
|----------|-------------|----------|
| `API_ID` | Telegram API ID | Yes |
| `API_HASH` | Telegram API Hash | Yes |
| `BOT_TOKEN` | Bot token from @BotFather | Yes |
| `DATABASE_URL` | MongoDB connection string | Yes |
| `DOWNLOAD_URL` | Your Koyeb app URL | Yes |
| `MAX_FILE_SIZE` | Maximum file size (bytes) | No |
| `STREAMING_ENABLED` | Enable streaming | No |

## Commands

- `/start` - Start the bot
- `/stats` - Bot statistics (admin only)
- `/broadcast` - Broadcast message (admin only)
- `/ping` - Check bot latency

## Support

For support, contact [@viperadnan](https://t.me/viperadnan) or create an issue on GitHub.
