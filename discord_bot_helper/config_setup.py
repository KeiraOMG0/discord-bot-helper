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
    
    print("\n⚙️  Configuration complete! Run your bot with:")
    print("   from discord_bot_helper import DiscordBotHelper")
    return config