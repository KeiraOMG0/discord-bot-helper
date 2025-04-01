import discord
from discord.ext import commands
import os
import json
import logging
from dotenv import load_dotenv
from typing import Optional

class DiscordBotHelper(commands.Bot):
    """Enhanced Discord bot with helper functionality"""
    
    def __init__(
        self,
<<<<<<< HEAD
        command_prefix: str = "!",
        intents: discord.Intents = discord.Intents.default(),
        *args, **kwargs
    ):
=======
        command_prefix: Optional[str] = None,
        intents: Optional[discord.Intents] = None,
        *args, **kwargs
    ):
        # Load early config for critical settings
        self._pre_config = self._load_pre_config()
        
        # Set up intents from config if not provided
        if intents is None:
            intents = discord.Intents.default()
            intents.message_content = self._pre_config.get('message_content', False)
            
        # Use config prefix if not provided
        command_prefix = command_prefix or self._pre_config.get('prefix', '!')
        
>>>>>>> 60c585b (Pushing changes!)
        super().__init__(
            command_prefix=command_prefix,
            intents=intents,
            *args, **kwargs
        )
<<<<<<< HEAD
        self.config = self._load_config()
        self.logger = self._setup_logging()
        self._validate_config()

    def _load_config(self) -> dict:
        """Load configuration from available sources"""
        if os.path.exists('config.json'):
            with open('config.json') as f:
                return json.load(f)
            
        load_dotenv()
        return {
            'token': os.getenv('DISCORD_TOKEN'),
            'prefix': os.getenv('PREFIX'),
            'owner_id': os.getenv('OWNER_ID'),
            'sync_commands': os.getenv('SYNC_COMMANDS', 'false').lower() == 'true',
            'use_cogs': os.getenv('USE_COGS', 'false').lower() == 'true'
        }
=======
        
        # Complete initialization
        self.config = self._validate_config()
        self.logger = self._setup_logging()

    def _load_pre_config(self) -> dict:
        """Load config values needed before bot initialization"""
        if os.path.exists('config.json'):
            with open('config.json') as f:
                return json.load(f)
        
        load_dotenv()
        return {
            'prefix': os.getenv('PREFIX', '!'),
            'message_content': os.getenv('MESSAGE_CONTENT', 'false').lower() == 'true'
        }

    def _validate_config(self) -> dict:
        """Load and validate full configuration"""
        full_config = self._load_pre_config()
        full_config.update({
            'token': os.getenv('DISCORD_TOKEN') or self._pre_config.get('token'),
            'owner_id': os.getenv('OWNER_ID'),
            'sync_commands': os.getenv('SYNC_COMMANDS', 'false').lower() == 'true',
            'use_cogs': os.getenv('USE_COGS', 'false').lower() == 'true'
        })
        
        if not full_config.get('token'):
            raise ValueError("No bot token found in configuration!")
        return full_config
>>>>>>> 60c585b (Pushing changes!)

    def _setup_logging(self) -> logging.Logger:
        """Configure logging system"""
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s | %(levelname)-8s | %(name)s: %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S',
            handlers=[
                logging.StreamHandler(),
                logging.FileHandler('bot.log')
            ]
        )
        return logging.getLogger('DBH')

<<<<<<< HEAD
    def _validate_config(self):
        """Validate essential configuration"""
        if not self.config.get('token'):
            raise ValueError("No bot token found in configuration!")

=======
>>>>>>> 60c585b (Pushing changes!)
    async def setup_hook(self) -> None:
        """Post-initialization setup"""
        self.logger.info("Starting bot initialization...")
        
        if self.config.get('use_cogs'):
            await self.load_cogs()
            
        if self.config.get('sync_commands'):
            self.logger.info("Syncing application commands...")
<<<<<<< HEAD
            await self.tree.sync()
=======
            try:
                synced = await self.tree.sync()
                self.logger.info(f"Synced {len(synced)} commands")
            except Exception as e:
                self.logger.error(f"Command sync failed: {str(e)}")
>>>>>>> 60c585b (Pushing changes!)

    async def load_cogs(self, cog_dir: str = 'cogs') -> None:
        """Load all cogs from directory"""
        self.logger.info(f"Loading cogs from {cog_dir}/")
        
        if not os.path.exists(cog_dir):
            os.makedirs(cog_dir)
            self.logger.warning(f"Created missing cog directory: {cog_dir}/")
            return

        for filename in os.listdir(cog_dir):
            if filename.endswith('.py') and not filename.startswith('_'):
                cog_name = f"{cog_dir}.{filename[:-3]}"
                try:
                    await self.load_extension(cog_name)
                    self.logger.info(f"Loaded cog: {cog_name}")
                except Exception as e:
                    self.logger.error(f"Failed to load {cog_name}: {str(e)}")

    def run_bot(self) -> None:
        """Start the bot with proper error handling"""
        try:
            self.logger.info("Starting bot...")
            super().run(self.config['token'])
        except discord.LoginError:
            self.logger.critical("Invalid bot token!")
        except KeyboardInterrupt:
            self.logger.info("Bot shutdown requested")
        finally:
            self.logger.info("Bot has shut down")