from redbot.core import commands
import discord

rooms = []
class ChannelRenter(commands.Cog):
    """My custom cog"""

    @commands.command()
    async def mycom(self, ctx, member: discord.Member):
        """This does stuff!"""
        # Your code will go here

        await member.edit(voice_channel=None)

    @commands.command()
    async def channelId(self, ctx, member: discord.Member):
        """This does stuff!"""
        # Your code will go here
        member.voice.mo
        await ctx.send(member.voice.channel.id)

    @commands.command()
    async def registerchannel(self, ctx):

        if ctx.author.voice.channel == None:
            await ctx.send("Você precisa estar cadastrado numa sala para registra-la")
            return

        currentvc: int = ctx.author.voice.channel.id

        if currentvc in rooms:
            await ctx.send("Sala já cadastrada")
        else:
            rooms.append(currentvc)
            await ctx.send("Sala " + " cadastrada")

    @commands.command()
    async def watcher(self, ctx, *args):

        await ctx.send(args)
        if ctx.author.voice.channel is None:
            await ctx.send("Você não está em nenhuma sala")
            return

        currentvc: int = ctx.author.voice.channel
        if currentvc.id not in rooms:
            await ctx.send("Sala não cadastrada")
        else:
            for participant in args:
                print('participant = ' + participant)
                print(ctx.message.guild.members)
                tmp = discord.utils.get(ctx.message.guild.members, mention=participant)
                print(tmp)
                await ctx.send(tmp)
                await tmp.move_to(currentvc)
