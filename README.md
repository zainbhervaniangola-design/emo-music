# 🎵 Emo Music Bot

A sleek Discord bot that integrates with Spotify to search and manage music. Now with **slash commands (/)** for a modern Discord experience!

## ✨ Features

- 🎵 **Play Songs** - Search and play tracks from Spotify
- 🔍 **Search** - Find songs with multiple results
- 🎧 **Playlists** - Browse and search Spotify playlists
- 🎤 **Artist Info** - Get detailed artist information
- ⚡ **Slash Commands** - Modern `/` command interface
- 📊 **Rich Embeds** - Beautiful formatted responses
- 🔒 **Secure** - Environment variables for credentials

## 📋 Commands

| Command | Description | Example |
|---------|-------------|----------|
| `/play` | Play a song from Spotify | `/play query:Blinding Lights` |
| `/search` | Search for songs | `/search query:Sad limit:5` |
| `/playlist` | Search playlists | `/playlist query:Sad Songs` |
| `/artist` | Get artist info | `/artist query:The Weeknd` |
| `/ping` | Check latency | `/ping` |
| `/help` | Show all commands | `/help` |

## 🚀 Setup

### 1. Create Discord Bot

1. Go to [Discord Developer Portal](https://discord.com/developers/applications)
2. Click "New Application"
3. Go to "Bot" → "Add Bot"
4. Copy the **Token**
5. Go to "OAuth2" → "URL Generator"
6. Select scopes: `bot`
7. Select permissions:
   - Send Messages
   - Embed Links
   - Read Message History
8. Copy the generated URL and invite the bot to your server

### 2. Create Spotify App

1. Go to [Spotify Developer Dashboard](https://developer.spotify.com/dashboard)
2. Log in or create an account
3. Click "Create an App"
4. Accept terms and create
5. Copy **Client ID** and **Client Secret**

### 3. Setup Environment

```bash
# Clone the repository
git clone https://github.com/zainbhervaniangola-design/emo-music.git
cd emo-music

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Create .env file
cp .env.example .env
```

### 4. Configure .env

Edit `.env` and add your credentials:

```
DISCORD_TOKEN=your_discord_bot_token_here
SPOTIFY_CLIENT_ID=your_spotify_client_id_here
SPOTIFY_CLIENT_SECRET=your_spotify_client_secret_here
```

### 5. Run the Bot

```bash
python bot.py
```

You should see: `✅ [BotName] is online and synced X command(s)!`

## 💻 Usage Examples

### Search and Play a Song
```
/play query:Blinding Lights
```

### Search Multiple Results
```
/search query:Sad Songs limit:5
```

### Find a Playlist
```
/playlist query:Workout Music
```

### Get Artist Information
```
/artist query:The Weeknd
```

## 📁 Project Structure

```
emo-music/
├── bot.py              # Main bot file with all commands
├── requirements.txt    # Python dependencies
├── .env.example        # Environment variables template
└── README.md          # This file
```

## ⚙️ Technologies

- **discord.py** - Discord bot framework
- **Spotipy** - Spotify API client
- **python-dotenv** - Environment variable management

## 🔒 Security Notes

- **Never** commit your `.env` file
- **Never** share your bot token
- Keep your Spotify credentials private
- Use environment variables for all sensitive data

## 🐛 Troubleshooting

### Commands not showing up?
- Restart the bot: `python bot.py`
- Commands sync on startup automatically
- May take a few seconds to appear in Discord

### "No tracks found"?
- Check your spelling
- Try a simpler query
- Make sure Spotify has the track

### Bot is offline?
- Check your Discord token in `.env`
- Make sure the bot has correct permissions
- Check console for error messages

## 📝 License

MIT License - Feel free to use and modify!

## 🤝 Contributing

Feel free to fork and submit pull requests!

## 📧 Support

If you encounter issues, please open a GitHub issue.

---

**COPYRIGHT ARE NOT ALLOWED**
**Made by zainbhervaniangola-design**
