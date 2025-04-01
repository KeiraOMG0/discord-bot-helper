import json
import os
from getpass import getpass

def setup_config():
    """Interactive configuration setup wizard"""
    print("╭──────────────────────────────────────╮")
    print("│   Discord Bot Helper Setup Wizard    │")
    print("╰──────────────────────────────────────╯")
    
    config = {}
    
    # Configuration type selection
    while True:
        config_type = input("➤ Use [J]SON or [E]NV configuration? (J/E): ").lower()
        if config_type in ['j', 'e']:
            config['type'] = 'json' if config_type == 'j' else 'env'
            break
        print("⚠️  Please enter J or E")

    # Required fields
    config['token'] = getpass("➤ Enter bot token: ").strip()
    while not config['token']:
        print("⚠️  Token is required!")
        config['token'] = getpass("➤ Enter bot token: ").strip()

    config['prefix'] = input("➤ Enter command prefix (default: !): ").strip() or '!'

    # Optional fields
    config['owner_id'] = input("➤ Enter owner ID (optional): ").strip()
    config['sync_commands'] = input("➤ Enable slash command syncing? (Y/n): ").lower() in ['y', '']
    config['use_cogs'] = input("➤ Use cog system? (Y/n): ").lower() in ['y', '']

    # File creation
    if config['type'] == 'json':
        with open('config.json', 'w') as f:
            json.dump({k:v for k,v in config.items() if k != 'type'}, f, indent=2)
        print("✅ Created config.json")
    else:
        with open('.env', 'w') as f:
            f.write(f"DISCORD_TOKEN={config['token']}\n")
            f.write(f"PREFIX={config['prefix']}\n")
            if config['owner_id']:
                f.write(f"OWNER_ID={config['owner_id']}\n")
            f.write(f"SYNC_COMMANDS={str(config['sync_commands']).lower()}\n")
            f.write(f"USE_COGS={str(config['use_cogs']).lower()}\n")
        print("✅ Created .env file")
    
    # Generate bot.py
    generate_bot_file(config)
    
    print("\n⚙️  Configuration complete! Run your bot with:")
    print("   python bot.py")
    return config

def generate_bot_file(config):
    """Generate a starter bot.py file and cog directory"""
    # Create cogs directory if enabled
    if config['use_cogs']:
        os.makedirs('cogs', exist_ok=True)
        print("✅ Created cogs/ directory")

        # Add example cog file
        example_cog = """import discord
from discord.ext import commands

class Example(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.command()
    async def test(self, ctx):
        \"\"\"Test command\"\"\"
        await ctx.send("Cog command works!")

async def setup(bot: commands.Bot):
    await bot.add_cog(Example(bot))
"""
        with open('cogs/example.py', 'w') as f:
            f.write(example_cog)
        print("✅ Created example cog: cogs/example.py")

    # Generate bot.py content
    bot_content = """import discord
from discord_bot_helper import DiscordBotHelper

# Initialize bot with configured settings
bot = DiscordBotHelper(command_prefix='{prefix}')

@bot.event
async def on_ready():
    print(f'Logged in as {{bot.user.name}} ({{bot.user.id}})')
    print('------')
    {sync_command}

# Example slash command
{slash_command}

# Example prefix command
@bot.command()
async def hello(ctx):
    await ctx.send(f"Hello {{ctx.author.mention}}!")

{cog_comment}

if __name__ == "__main__":
    bot.run_bot()
""".format(
        prefix=config["prefix"],
        sync_command="await bot.tree.sync()" if config["sync_commands"] else "",
        slash_command=(
            '''@bot.tree.command(name="ping", description="Check bot latency")
async def ping(interaction: discord.Interaction):
    await interaction.response.send_message(f"Pong! {{round(bot.latency*1000)}}ms")'''
            if config["sync_commands"]
            else ""
        ),
        cog_comment="# Example cog loaded from cogs/example.py" if config["use_cogs"] else "",
    )

    with open('bot.py', 'w') as f:
        f.write(bot_content)
    print("✅ Created starter bot.py")
