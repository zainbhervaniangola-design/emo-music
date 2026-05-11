import discord
from discord.ext import commands
from discord import app_commands
import os
from dotenv import load_dotenv
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import logging

# Load environment variables
load_dotenv()

# Logging setup
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Discord Bot Setup
intents = discord.Intents.default()
intents.message_content = True
intents.guilds = True

bot = commands.Bot(command_prefix="!", intents=intents)

# Spotify Setup
DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")
SPOTIFY_CLIENT_ID = os.getenv("SPOTIFY_CLIENT_ID")
SPOTIFY_CLIENT_SECRET = os.getenv("SPOTIFY_CLIENT_SECRET")

if not all([DISCORD_TOKEN, SPOTIFY_CLIENT_ID, SPOTIFY_CLIENT_SECRET]):
    logger.error("Missing required environment variables. Check your .env file.")
    exit()

# Initialize Spotify client
auth_manager = SpotifyClientCredentials(
    client_id=SPOTIFY_CLIENT_ID,
    client_secret=SPOTIFY_CLIENT_SECRET
)
sp = spotipy.Spotify(auth_manager=auth_manager)


@bot.event
async def on_ready():
    try:
        synced = await bot.tree.sync()
        print(f"✅ {bot.user} is online and synced {len(synced)} command(s)!")
    except Exception as e:
        print(f"❌ Error syncing commands: {e}")


@bot.tree.command(name="play", description="Play a song from Spotify")
@app_commands.describe(query="Song name or artist name")
async def play(interaction: discord.Interaction, query: str):
    """Search and play a song from Spotify"""
    await interaction.response.defer()
    
    try:
        results = sp.search(q=query, type="track", limit=1)
        
        if not results["tracks"]["items"]:
            await interaction.followup.send("❌ No tracks found!")
            return
        
        track = results["tracks"]["items"][0]
        track_name = track["name"]
        artist_name = track["artists"][0]["name"]
        album_name = track["album"]["name"]
        track_url = track["external_urls"]["spotify"]
        image_url = track["album"]["images"][0]["url"]
        
        # Create embed
        embed = discord.Embed(
            title="🎵 Now Playing",
            description=f"[{track_name}]({track_url})",
            color=discord.Color.green()
        )
        embed.add_field(name="Artist", value=artist_name, inline=False)
        embed.add_field(name="Album", value=album_name, inline=False)
        embed.set_thumbnail(url=image_url)
        
        await interaction.followup.send(embed=embed)
        logger.info(f"Playing: {track_name} by {artist_name}")
        
    except Exception as e:
        logger.error(f"Error in play command: {e}")
        await interaction.followup.send(f"❌ Error: {str(e)}")


@bot.tree.command(name="search", description="Search for a song on Spotify")
@app_commands.describe(query="Song name or artist name", limit="Number of results (1-10)")
async def search(interaction: discord.Interaction, query: str, limit: int = 5):
    """Search for songs on Spotify"""
    await interaction.response.defer()
    
    try:
        if limit < 1 or limit > 10:
            await interaction.followup.send("❌ Limit must be between 1 and 10")
            return
        
        results = sp.search(q=query, type="track", limit=limit)
        tracks = results["tracks"]["items"]
        
        if not tracks:
            await interaction.followup.send("❌ No tracks found!")
            return
        
        embed = discord.Embed(
            title=f"🔍 Search Results for '{query}'",
            color=discord.Color.blue(),
            description=""
        )
        
        for idx, track in enumerate(tracks, 1):
            track_name = track["name"]
            artist_name = track["artists"][0]["name"]
            track_url = track["external_urls"]["spotify"]
            embed.description += f"{idx}. [{track_name}]({track_url}) - {artist_name}\n"
        
        await interaction.followup.send(embed=embed)
        logger.info(f"Searched: {query}")
        
    except Exception as e:
        logger.error(f"Error in search command: {e}")
        await interaction.followup.send(f"❌ Error: {str(e)}")


@bot.tree.command(name="playlist", description="Search for a Spotify playlist")
@app_commands.describe(query="Playlist name")
async def playlist(interaction: discord.Interaction, query: str):
    """Search for playlists on Spotify"""
    await interaction.response.defer()
    
    try:
        results = sp.search(q=query, type="playlist", limit=5)
        playlists = results["playlists"]["items"]
        
        if not playlists:
            await interaction.followup.send("❌ No playlists found!")
            return
        
        embed = discord.Embed(
            title=f"🎧 Playlist Results for '{query}'",
            color=discord.Color.purple(),
            description=""
        )
        
        for idx, pl in enumerate(playlists, 1):
            pl_name = pl["name"]
            pl_owner = pl["owner"]["display_name"]
            pl_url = pl["external_urls"]["spotify"]
            pl_tracks = pl["tracks"]["total"]
            embed.description += f"{idx}. [{pl_name}]({pl_url}) - by {pl_owner} ({pl_tracks} songs)\n"
        
        await interaction.followup.send(embed=embed)
        logger.info(f"Searched playlists: {query}")
        
    except Exception as e:
        logger.error(f"Error in playlist command: {e}")
        await interaction.followup.send(f"❌ Error: {str(e)}")


@bot.tree.command(name="artist", description="Get information about an artist")
@app_commands.describe(query="Artist name")
async def artist(interaction: discord.Interaction, query: str):
    """Get artist information from Spotify"""
    await interaction.response.defer()
    
    try:
        results = sp.search(q=query, type="artist", limit=1)
        
        if not results["artists"]["items"]:
            await interaction.followup.send("❌ Artist not found!")
            return
        
        artist_info = results["artists"]["items"][0]
        artist_name = artist_info["name"]
        popularity = artist_info["popularity"]
        followers = artist_info["followers"]["total"]
        genres = ", ".join(artist_info["genres"]) if artist_info["genres"] else "N/A"
        artist_url = artist_info["external_urls"]["spotify"]
        image_url = artist_info["images"][0]["url"] if artist_info["images"] else None
        
        embed = discord.Embed(
            title=f"🎤 {artist_name}",
            url=artist_url,
            color=discord.Color.orange()
        )
        embed.add_field(name="Popularity", value=f"⭐ {popularity}/100", inline=True)
        embed.add_field(name="Followers", value=f"👥 {followers:,}", inline=True)
        embed.add_field(name="Genres", value=genres, inline=False)
        if image_url:
            embed.set_thumbnail(url=image_url)
        
        await interaction.followup.send(embed=embed)
        logger.info(f"Artist lookup: {artist_name}")
        
    except Exception as e:
        logger.error(f"Error in artist command: {e}")
        await interaction.followup.send(f"❌ Error: {str(e)}")


@bot.tree.command(name="ping", description="Check bot latency")
async def ping(interaction: discord.Interaction):
    """Check the bot's latency"""
    latency = round(bot.latency * 1000)
    embed = discord.Embed(
        title="🏓 Pong!",
        description=f"Latency: {latency}ms",
        color=discord.Color.green()
    )
    await interaction.response.send_message(embed=embed)


@bot.tree.command(name="help", description="Show all available commands")
async def help_command(interaction: discord.Interaction):
    """Display all bot commands"""
    embed = discord.Embed(
        title="🎵 Emo Music Bot - Commands",
        color=discord.Color.blurple(),
        description="Here are all the available slash commands:"
    )
    
    commands_list = [
        ("/play [query]", "Search and play a song from Spotify"),
        ("/search [query] [limit]", "Search for songs (shows up to 10 results)"),
        ("/playlist [query]", "Search for Spotify playlists"),
        ("/artist [query]", "Get information about an artist"),
        ("/ping", "Check bot latency"),
        ("/help", "Show this help message")
    ]
    
    for cmd, desc in commands_list:
        embed.add_field(name=cmd, value=desc, inline=False)
    
    embed.set_footer(text="Made with ❤️ by Emo Music Bot")
    await interaction.response.send_message(embed=embed, ephemeral=True)


# Error handling
@bot.tree.error
async def on_app_command_error(interaction: discord.Interaction, error: app_commands.AppCommandError):
    logger.error(f"Command error: {error}")
    if not interaction.response.is_done():
        await interaction.response.send_message(f"❌ An error occurred: {str(error)}", ephemeral=True)
    else:
        await interaction.followup.send(f"❌ An error occurred: {str(error)}", ephemeral=True)


if __name__ == "__main__":
    try:
        bot.run(DISCORD_TOKEN)
    except Exception as e:
        logger.error(f"Failed to start bot: {e}")
