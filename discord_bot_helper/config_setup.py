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

    # Intent configuration
    config['message_content'] = input(
        "➤ Enable message content intent? (Required for prefix commands) (Y/n): "
    ).lower() in ['y', '']

    # Optional fields
    config['owner_id'] = input("➤ Enter owner ID (optional): ").strip()
    config['sync_commands'] = input("➤ Enable slash command syncing? (Y/n): ").lower() in ['y', '']
    config['use_cogs'] = input("➤ Use cog system? (Y/n): ").lower() in ['y', '']

    # File creation
    if config['type'] == 'json':
        config_data = {
            'token': config['token'],
            'prefix': config['prefix'],
            'message_content': config['message_content'],
            'owner_id': config['owner_id'],
            'sync_commands': config['sync_commands'],
            'use_cogs': config['use_cogs']
        }
        with open('config.json', 'w') as f:
            json.dump(config_data, f, indent=2)
        print("✅ Created config.json")
    else:
        with open('.env', 'w') as f:
            f.write(f"DISCORD_TOKEN={config['token']}\n")
            f.write(f"PREFIX={config['prefix']}\n")
            f.write(f"MESSAGE_CONTENT={str(config['message_content']).lower()}\n")
            if config['owner_id']:
                f.write(f"OWNER_ID={config['owner_id']}\n")
            f.write(f"SYNC_COMMANDS={str(config['sync_commands']).lower()}\n")
            f.write(f"USE_COGS={str(config['use_cogs']).lower()}\n")
        print("✅ Created .env file")
    
    generate_bot_file(config)
    
    print("\n⚙️  Configuration complete! Run your bot with:")
    print("   python bot.py")
    return config

def generate_bot_file(config):
    """Generate a starter bot.py file and cog directory"""
    if config['use_cogs']:
        os.makedirs('cogs', exist_ok=True)
        print("✅ Created cogs/ directory")
        
        example_cog = '''import discord
from discord.ext import commands

class Example(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.command()
    async def test(self, ctx):
        """Test command"""
        await ctx.send("Cog command works!")

async def setup(bot: commands.Bot):
    await bot.add_cog(Example(bot))'''
        
        with open('cogs/example.py', 'w') as f:
            f.write(example_cog)
        print("✅ Created example cog: cogs/example.py")

    bot_content = f'''import discord
from discord_bot_helper import DiscordBotHelper

bot = DiscordBotHelper()

@bot.event
async def on_ready():
    print(f'Logged in as {{bot.user.name}} ({{bot.user.id}})')
    print('------')'''
    
    if config['sync_commands']:
        bot_content += "\n    await bot.tree.sync()"
    
    bot_content += "\n\n"
    
    if config['sync_commands']:
        bot_content += '''@bot.tree.command(name="ping", description="Check bot latency")
async def ping(interaction: discord.Interaction):
    await interaction.response.send_message(f"Pong! {{round(bot.latency*1000)}}ms")

'''

    bot_content += '''@bot.command()
async def hello(ctx):
    await ctx.send(f"Hello {ctx.author.mention}!")

'''

    if config['use_cogs']:
        bot_content += "# Cogs loaded automatically from cogs directory\n"

    bot_content += '''if __name__ == "__main__":
    bot.run_bot()'''

    with open('bot.py', 'w') as f:
        f.write(bot_content)
    print("✅ Created starter bot.py")