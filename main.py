import os
print("VERSION 26 JUNE FIX")
import discord
from discord.ext import commands
from discord import app_commands
from dotenv import load_dotenv

# ============================================
# LOAD TOKEN
# ============================================

load_dotenv()

TOKEN = os.getenv("YOUR_BOT_TOKEN")

if TOKEN is None:
    print("ERROR: Could not find YOUR_BOT_TOKEN in .env file.")
    exit()

# ============================================
# CONFIGURATION
# ============================================

# Replace this with YOUR role ID
PING_ROLE_ID = 1480231883383111881

# Thumbnail (leave blank if you don't want one)
THUMBNAIL_URL = ""

# ============================================
# INTENTS
# ============================================

intents = discord.Intents.default()
intents.message_content = True
intents.members = True

# ============================================
# BOT SETUP
# ============================================

bot = commands.Bot(
    command_prefix="!",
    intents=intents
)

# ============================================
# READY EVENT
# ============================================

@bot.event
async def on_ready():

    if not hasattr(bot, "synced"):
        try:
            synced = await bot.tree.sync()
            print(f"Synced {len(synced)} command(s).")
            bot.synced = True
        except Exception as e:
            print(f"Sync Error: {e}")

    print(f"{bot.user} is online!")

# ============================================
# /PING
# ============================================

@bot.tree.command(
    name="ping",
    description="Check the bot latency."
)
async def ping(interaction: discord.Interaction):

    await interaction.response.send_message(
        f"Pong! {round(bot.latency * 1000)}ms"
    )


# ============================================
# /EMBED
# ============================================

@bot.tree.command(
    name="embed",
    description="Create a professional announcement."
)
@app_commands.describe(
    title="Announcement title",
    description="Announcement description"
)
async def embed(
    interaction: discord.Interaction,
    title: str,
    description: str
):

    role = interaction.guild.get_role(PING_ROLE_ID)

    print(f"PING_ROLE_ID: {PING_ROLE_ID}")
    print(f"ROLE OBJECT: {role}")

    ping_text = role.mention if role else "ROLE NOT FOUND"

    embed = discord.Embed(
        title=title,
        description=description,
        color=discord.Color.green()
    )

    embed.set_footer(text=f"Posted by {interaction.user.display_name}")
    embed.timestamp = discord.utils.utcnow()

    await interaction.response.send_message(
        content=ping_text,
        embed=embed,
        allowed_mentions=discord.AllowedMentions(roles=True)
    )

# ============================================
# /DEPLOY
# ============================================

@bot.tree.command(
    name="deploy",
    description="Create a deployment announcement."
)
@app_commands.describe(
    cohost="Co-Host",
    members_required="Members required",
    notes="Additional notes"
)
async def deploy(
    interaction: discord.Interaction,
    cohost: str,
    members_required: str,
    notes: str
):

    host = interaction.user
    role = interaction.guild.get_role(1480231883383111881)

    # Create role + host ping
    ping_text = host.mention

    if role:
        ping_text += f" {role.mention}"

    # Create embed
    embed = discord.Embed(
        title="DEPLOYMENT CALL",
        color=discord.Color.green()
    )

    embed.description = (
        "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n\n"

        f"**HOST**\n"
        f"{host.mention}\n\n"

        f"**CO-HOST**\n"
        f"{cohost}\n\n"

        f"**MEMBERS REQUIRED**\n"
        f"{members_required}\n\n"

        f"**NOTES**\n"
        f"{notes}\n\n"

        "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    )

    if THUMBNAIL_URL:
        embed.set_thumbnail(url=THUMBNAIL_URL)

    embed.set_footer(
        text="Faction Ethics Committee"
    )

    embed.timestamp = discord.utils.utcnow()

    await interaction.response.send_message(
        content=ping_text,
        embed=embed,
        allowed_mentions=discord.AllowedMentions(
            users=True,
            roles=True
        )
    )

# ============================================
# RUN BOT
# ============================================

if __name__ == "__main__":
    try:
        bot.run(TOKEN)

    except discord.LoginFailure:
        print("ERROR: Invalid bot token.")

    except Exception as e:
        print(f"Unexpected error: {e}")