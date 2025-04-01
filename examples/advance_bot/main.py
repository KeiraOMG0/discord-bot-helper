from discord_bot_helper import DiscordBotHelper

class AdvancedBot(DiscordBotHelper):
    async def setup_hook(self):
        await self.load_cogs('cogs')
        await super().setup_hook()

bot = AdvancedBot()

@bot.event
async def on_ready():
    print(f"Logged in as {bot.user} (ID: {bot.user.id})")
    print("------")

if __name__ == "__main__":
    bot.run_bot()