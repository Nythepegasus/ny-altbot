import json
import asyncio
import discord
from discord.ext.commands import Bot, Cog, command, ExtensionAlreadyLoaded, ExtensionNotFound

class AdminCog(Cog, name="Admin"):
    def __init__(self, client):
        self.client = client
        self.description = "This module is only for the developer"

    async def cog_before_invoke(self, ctx):
        await ctx.message.delete()

    async def cog_check(self, ctx):
        return await self.client.is_owner(ctx.author)

    async def cog_command_error(self, ctx, error):
        print(ctx)
        print(error)

    @command(name="load", hidden=True, help="Loads a cog.")
    async def load_cog(self, ctx, *, cog: str):
        try:
            await self.client.load_extension(f"modules.{cog}")
        except Exception as e:
            await ctx.author.send(f"**`ERROR:`**\n {type(e).__name__} - {e}")
        else:
            await ctx.send(f"`{cog}` has been loaded!", delete_after=5)

    @command(name="unload", hidden=True, help="Unloads a cog.")
    async def unload_mod(self, ctx, *, cog: str):
        if cog == "modules.admin":
            return await ctx.send("Cowardly refusing to unload admin cog.", delete_after=5)
        try:
            await self.client.unload_extension(f"modules.{cog}")
            return await ctx.send(f"`{cog}` has been unloaded!", delete_after=5)
        except Exception as e:
            await ctx.author.send(f"**`ERROR:`**\n {type(e).__name__} - {e}")

    @command(name="reload", hidden=True, help="Reloads a cog.")
    async def unload_cog(self, ctx, *, cog: str):
        try:
            await self.client.reload_extension(f"modules.{cog}")
            return await ctx.send(f"`{cog}` has been reloaded!", delete_after=5)
        except Exception as e:
            await ctx.author.send(f"**`ERROR:`**\n {type(e).__name__} - {e}")

    @command(name="sync", hidden=True, help="Sync application commands.")
    async def sync(self, ctx):
        c = await self.client.tree.sync()
        await ctx.send(f"Synced {len(c)} global commands.")

    @command(name="sync_dev", hidden=True, help="Sync development application commands.")
    async def sync_dev(self, ctx):
        c = await self.client.tree.sync(guild=discord.Object(537887803774730270))
        await interaction.response.send_message(f"Synced {len(c)} dev commands.")

    @command(name="update", hidden=True, help="Update the bot.")
    async def update_bot(self, ctx):
        """We should git pull, and reload all the modules"""
        proc = await asyncio.create_subprocess_exec(
                "git", "pull", stdout=asyncio.subprocess.PIPE
               )
        data = await proc.stdout.readline()
        line = data.decode('ascii').rstrip()
        await proc.wait()
        print(line)

        for cog in self.client.conf_data["modules"]:
            await self.client.reload_extension(cog)

        await ctx.send("Updated the bot!", delete_after=5)

    @command(name="add_cog", hidden=True, help="Add cog to bot.")
    async def add_mod(self, ctx, *, cog: str):
        conf = json.load(open("conf.json"))
        try:
            await self.client.load_extension(f"modules.{cog}")
        except (ExtensionNotFound, ExtensionAlreadyLoaded) as e:
            if isinstance(e, ExtensionNotFound):
                return await ctx.send(f"Couldn't find `{cog}` to add to startup.", delete_after=5)
            elif isinstance(e, ExtensionAlreadyLoaded):
                pass

        if f"modules.{cog}" in conf["modules"]:
            return await ctx.send(f"`{cog}` is already in startup.", delete_after=5)
        conf["modules"].append(f"modules.{cog}")
        json.dump(conf, open("conf.json", "w"), indent=4)
        return await ctx.send(f"`{cog}` has been added to bot startup!", delete_after=5)

async def setup(client: Bot):
    await client.add_cog(AdminCog(client))

