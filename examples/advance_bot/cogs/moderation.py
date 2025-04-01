import discord
from discord import app_commands
from discord.ext import commands

class Moderation(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @app_commands.command(name="clear", description="Clear a number of messages from this channel.")
    @app_commands.checks.has_permissions(manage_messages=True)
    async def clear(self, interaction: discord.Interaction, amount: int):
        """Clears messages using a slash command."""
        await interaction.response.defer(ephemeral=True)  # Defer response to avoid timeouts
        deleted = await interaction.channel.purge(limit=amount)
        await interaction.followup.send(f"🗑️ Cleared {len(deleted)} messages", ephemeral=True, delete_after=5)

    @app_commands.command(name="shutdown", description="Shuts down the bot (owner only).")
    @app_commands.checks.is_owner()
    async def shutdown(self, interaction: discord.Interaction):
        """Bot owner shutdown command."""
        await interaction.response.send_message("🛑 Shutting down...", ephemeral=True)
        await self.bot.close()

async def setup(bot: commands.Bot):
    await bot.add_cog(Moderation(bot))
