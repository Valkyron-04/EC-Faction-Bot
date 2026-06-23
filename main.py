import os
import discord
from discord.ext import commands
from discord import app_commands
from dotenv import load_dotenv

# ==========================
# LOAD TOKEN
# ==========================
load_dotenv()

TOKEN = os.getenv("YOUR_BOT_TOKEN")

if TOKEN is None:
    print("ERROR: Could not find YOUR_BOT_TOKEN in .env file.")
    exit()

# ==========================
# INTENTS
# ==========================
intents = discord.Intents.default()
intents.message_content = True
intents.members = True

# ==========================
# BOT SETUP
# ==========================
bot = commands.Bot(
    command_prefix="!",
    intents=intents
)

# ==========================
# READY EVENT
# ==========================
@bot.event
async def on_ready():
    try:
        synced = await bot.tree.sync()
        print(f"Synced {len(synced)} command(s).")
        print(f"{bot.user} is online!")
    except Exception as e:
        print(e)

# ==========================
# PING COMMAND
# ==========================
@bot.tree.command(
    name="ping",
    description="Check bot latency."
)
async def ping(interaction: discord.Interaction):
    await interaction.response.send_message(
        f"🏓 Pong! {round(bot.latency * 1000)}ms"
    )

# ==========================
# EMBED GENERATOR
# ==========================
@bot.tree.command(
    name="embed",
    description="Create an announcement embed."
)
@app_commands.describe(
    title="Embed title",
    description="Embed description"
)
async def embed(
    interaction: discord.Interaction,
    title: str,
    description: str
):

    embed = discord.Embed(
        title=title,
        description=description,
        color=discord.Color.blue()
    )

    embed.set_footer(
        text="Faction Ethics Committee"
    )

    await interaction.response.send_message(
        embed=embed
    )

# ==========================
# DEPLOYMENT COMMAND
# ==========================
@bot.tree.command(
    name="deploy",
    description="Send a deployment call."
)
@app_commands.describe(
    host="Deployment host",
    cohost="Deployment co-host",
    members_required="Members required",
    notes="Additional notes"
)
async def deploy(
    interaction: discord.Interaction,
    host: str,
    cohost: str,
    members_required: str,
    notes: str
):

    embed = discord.Embed(
        title="📢 Deployment Call",
        color=discord.Color.orange()
    )

    embed.add_field(
        name="Host",
        value=host,
        inline=False
    )

    embed.add_field(
        name="Co-host",
        value=cohost,
        inline=False
    )

    embed.add_field(
        name="Members Required",
        value=members_required,
        inline=False
    )

    embed.add_field(
        name="Notes",
        value=notes,
        inline=False
    )

    embed.set_footer(
        text="Faction Ethics Committee"
    )

    await interaction.response.send_message(
        embed=embed
    )

# ==========================
# RUN BOT
# ==========================
bot.run(TOKEN)