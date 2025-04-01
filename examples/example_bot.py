from discord_bot_helper import DiscordBotHelper

bot = DiscordBotHelper()

@bot.command()
async def ping(ctx):
    """Simple ping command"""
    latency = round(bot.latency * 1000)
    await ctx.send(f"🏓 Pong! Latency: {latency}ms")

@bot.tree.command(name="hello", description="Say hello to the bot")
async def hello(interaction: discord.Interaction):
    """Say hello to the bot"""
    await interaction.response.send_message(f"👋 Hello {interaction.user.mention}!")

if __name__ == "__main__":
    bot.run_bot()