
# Discord Bot Helper 🤖

A modern Python library for building Discord bots with slash commands and automatic configuration.

![Python Version](https://img.shields.io/badge/python-3.8+-blue)
![Discord.py Version](https://img.shields.io/badge/discord.py-2.3+-blue)

## Features ✨
- ⚙️ Automatic configuration wizard (`dbh-init`)
- 🔄 Slash command synchronization
- 🧩 Built-in cog loader
- 📝 Smart logging system
- 🔒 Permission handling
- 📦 Auto-dependency installation

## Installation 💻
```bash
pip install git+https://github.com/KeiraOMG0/discord-bot-helper.git
```
Quick Start 🚀
Initialize Configuration:

```bash
dbh-init
```
Follow prompts to set up your bot token and preferences

Create `bot.py`:

```py
from discord_bot_helper import DiscordBotHelper
import discord
bot = DiscordBotHelper()

@bot.tree.command(name="ping", description="Check bot latency")
async def ping(interaction: discord.Interaction):
    await interaction.response.send_message(f"Pong! {round(bot.latency*1000)}ms")

if __name__ == "__main__":
    bot.run_bot()
```
Run Your Bot:

`python bot.py`
Command Types 📜
Slash Commands (Recommended)

```py
from discord import app_commands

@bot.tree.command(name="hello", description="Greet a user")
@app_commands.describe(user="User to greet")
async def hello(interaction: discord.Interaction, user: discord.User):
    await interaction.response.send_message(f"Hello {user.mention}!")
```
Prefix Commands (Legacy)

```py
@bot.command()
async def ping(ctx):
    await ctx.send(f"Pong! {round(bot.latency*1000)}ms")
```
Cog System 🧩
Create cogs/moderation.py:

```py
import discord
from discord import app_commands
from discord.ext import commands

class Moderation(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @app_commands.command(name="clear", description="Clear messages")
    @app_commands.checks.has_permissions(manage_messages=True)
    async def clear(self, interaction: discord.Interaction, amount: int):
        await interaction.response.defer(ephemeral=True)
        deleted = await interaction.channel.purge(limit=amount)
        await interaction.followup.send(f"Cleared {len(deleted)} messages", ephemeral=True)

async def setup(bot: commands.Bot):
    await bot.add_cog(Moderation(bot))
```

Cogs automatically load when:

Placed in `cogs/` directory

`use_cogs` enabled in config

File follows `*.py` naming

Permissions 🔒
Slash Command Permissions
```py
@app_commands.checks.has_permissions(manage_messages=True)
@app_commands.checks.is_owner()
```
Prefix Command Permissions
```py
@commands.has_permissions(kick_members=True)
@commands.is_owner()
```
Configuration ⚙️
Your `config.json` or `.env` file will contain:

```json
{
    "token": "YOUR_BOT_TOKEN",
    "prefix": "!",
    "sync_commands": true,
    "use_cogs": true
}
```
Example Bot 🌟

```python
from discord_bot_helper import DiscordBotHelper
import discord

class MyBot(DiscordBotHelper):
    async def setup_hook(self):
        await self.load_cogs()
        await self.tree.sync()

bot = MyBot()

@bot.tree.command(name="server", description="Show server info")
async def server(interaction: discord.Interaction):
    embed = discord.Embed(title=interaction.guild.name)
    embed.add_field(name="Members", value=interaction.guild.member_count)
    await interaction.response.send_message(embed=embed)

if __name__ == "__main__":
    bot.run_bot()
```    
Troubleshooting ⚠️
Common Issues:

Missing Permissions: Ensure bot has correct permissions in server

Command Sync Issues: Use `await bot.tree.sync()` after cog loading

Token Errors: Verify token in config.json/.env

Intents Issues: Enable required intents in Discord Developer Portal

Contributing 🤝
Fork the repository

Open Pull Request

License 📄
MIT License - See LICENSE
