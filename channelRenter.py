from redbot.core import commands
import discord
from channelRenter.rent import Rent

rooms = []


class ChannelRenter(commands.Cog):
    """My custom cog"""

    @commands.command()
    async def watcher(self, ctx, *args):

        owner = False
        locatedroom = None
        for room in rooms:
            if room.owner == ctx.message.author or room.role in ctx.message.author.roles:
                owner = True
                locatedroom = room

        if not owner:
            ctx.message.author.send("You're not part or owner of a rent")
            return

        for participant in args:
            user = discord.utils.get(ctx.guild.members, mention=participant)
            user.add_roles(locatedroom.role)
            await user.move_to(room.voice)

        if locatedroom.secret:
            ctx.message.delete()

    @commands.command()
    async def create_role(self, ctx, name: str):

        return await ctx.guild.create_role(name=name)

    @commands.command()
    async def create_voice_channel(self, ctx, name: str):

        return await ctx.guild.create_voice_channel(name, overwrites=None, category=None, reason=None)

    @commands.command()
    async def create_text_channel(self, ctx, name: str):

        return await ctx.guild.create_text_channel(name, overwrites=None, category=None, reason=None)

    @commands.command()
    async def create_room(self, ctx, name):

        guild = ctx.guild
        role = await self.create_role(ctx, name)
        voice = await self.create_voice_channel(ctx, name)
        text = await self.create_text_channel(ctx, name)
        owner = ctx.message.author

        """ Permissions to all """
        await text.set_permissions(guild.default_role, read_messages=False)
        await voice.set_permissions(guild.default_role, connect=False)

        """ Permissions to role """
        await text.set_permissions(role, read_messages=True)
        await voice.set_permissions(role, connect=True)

        room = Rent(name, voice, text, role, owner)
        return room

    @commands.command()
    async def rent(self, ctx, name):

        room = await self.create_room(ctx, name)
        rooms.append(room)

        if ctx.author.voice is not None:
            await ctx.message.author.move_to(room.voice)
        await ctx.message.author.add_roles(room.role)

    @commands.command()
    async def rent_secret(self, ctx, name):

        room = await self.create_room(ctx, name)
        await room.voice.set_permissions(ctx.guild.default_role, view_channel=False)
        rooms.append(room)

        if ctx.author.voice is not None:
            await ctx.message.author.move_to(room.voice)
        await ctx.message.author.add_roles(room.role)
        await ctx.message.delete();

    @commands.command()
    async def unrent(self, ctx):

        """ If the sender is the owner or the administrator, continue"""
        owner = False
        locatedroom = None
        for room in rooms:
            if room.owner == ctx.message.author:
                owner = True
                locatedroom = room;

        if ctx.message.author.guild_permissions.administrator:
            owner = True

        if not owner or locatedroom is None:
            await ctx.send("You didn't rent a room")
            return

        """ Start unreting the room and deleting permissions and channels"""

        await locatedroom.voice.delete()
        await locatedroom.text.delete()
        await locatedroom.role.delete()
        rooms.remove(locatedroom)

    @commands.command()
    async def unrent_all(self, ctx):

        if ctx.message.author.guild_permissions.administrator:
            for locatedroom in rooms:
                await locatedroom.voice.delete()
                await locatedroom.text.delete()
                await locatedroom.role.delete()
            rooms.clear()
            await ctx.message.author.send("Done!")
        else:
            await ctx.message.author.send("You are not an admin")
