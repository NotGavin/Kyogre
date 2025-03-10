import discord
from discord.ext import commands

import peewee

from kyogre import utils, checks
from kyogre.exts.db.kyogredb import *

class Badge:
    def __init__(self, id, name, description, emoji, active):
        self.id=id
        self.name=name
        self.description=description
        self.emoji=emoji
        self.active=active
    

class BadgeCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.group(name='badge', aliases=['bg'])
    @commands.has_permissions(manage_roles=True)
    async def _badge(self, ctx):
        if ctx.invoked_subcommand == None:
            raise commands.BadArgument()

    @_badge.command(name='add', aliases=['create', 'cr', 'new'])
    @commands.has_permissions(manage_roles=True)
    async def _add(self, ctx, *, info):
        info = re.split(r',\s+', info)
        if len(info) < 2:
            await ctx.message.add_reaction(self.bot.failed_react)
            self.bot.help_logger(f"User: {ctx.author.name}, channel: {ctx.channel}, error: Insufficient badge info: {info}.")
            return await ctx.send("Must provide at least an emoji and badge name, and optionally badge description.", delete_after=10)
        converter = commands.PartialEmojiConverter()
        try:
            badge_emoji = await converter.convert(ctx, info[0])
        except:
            badge_emoji = None
        if not badge_emoji:
            await ctx.message.add_reaction(self.bot.failed_react)
            self.bot.help_logger(f"User: {ctx.author.name}, channel: {ctx.channel}, error: No emoji found: {info[0]}.")
            return await ctx.send("Could not find that emoji.", delete_after=10)
        badge_name = info[1]
        badge_desc = ''
        if len(info) > 2:
            badge_desc = info[2]
        try:
            new_badge, __ = BadgeTable.get_or_create(name=badge_name, description=badge_desc, emoji=badge_emoji.id, active=True)
            if new_badge:
                send_emoji = self.bot.get_emoji(badge_emoji.id)
                message = f"{send_emoji} {badge_name} (#{new_badge.id}) successfully created!"
                colour = discord.Colour.green()
                reaction = self.bot.success_react
            else:
                message = "Failed to create badge. Please try again."
                colour = discord.Colour.red()
                reaction = self.bot.failed_react
        except peewee.IntegrityError:
            message = f"""A badge already exists with the same name, description, and emoji."""
            colour = discord.Colour.red()
            reaction = self.bot.failed_react
        await ctx.message.add_reaction(reaction)
        response = await ctx.channel.send(embed=discord.Embed(colour=colour, description=message), delete_after=12)

    @_badge.command(name='grant', aliases=['give', 'gr'])
    @commands.has_permissions(manage_roles=True)
    async def _grant(self, ctx, id: int=0, member: discord.Member=None):
        if id == 0 or member is None:
            await ctx.message.add_reaction(self.bot.failed_react)
            self.bot.help_logger(f"User: {ctx.author.name}, channel: {ctx.channel}, error: Insufficient info.")
            return await ctx.send("Must provide a badge id and Trainer name.", delete_after=10)
        badge_to_give = BadgeTable.get(BadgeTable.id == id)
        if badge_to_give:
            try:
                guild_obj, __ = GuildTable.get_or_create(snowflake=ctx.guild.id)
                trainer_obj, __ = TrainerTable.get_or_create(snowflake=member.id, guild=ctx.guild.id)
                new_badge, __ = BadgeAssignmentTable.get_or_create(trainer=member.id, badge=id)
                if new_badge:
                    send_emoji = self.bot.get_emoji(badge_to_give.emoji)
                    message = f"{member.display_name} has been given {send_emoji} **{badge_to_give.name}**!"
                    colour = discord.Colour.green()
                    reaction = self.bot.success_react
                else:
                    message = "Failed to give badge. Please try again."
                    colour = discord.Colour.red()
                    reaction = self.bot.failed_react
            except peewee.IntegrityError:
                message = f"{member.display_name} already has the **{badge_to_give.name}** badge!"
                colour = discord.Colour.red()
                reaction = self.bot.failed_react
        await ctx.message.add_reaction(reaction)
        response = await ctx.channel.send(embed=discord.Embed(colour=colour, description=message), delete_after=12)

    @commands.command(name="available-badges", aliases=['ab'])
    async def _available(self, ctx):
        result = (BadgeTable
                    .select(BadgeTable.id,
                            BadgeTable.name,
                            BadgeTable.description,
                            BadgeTable.emoji,
                            BadgeTable.active))
        result = result.objects(Badge)
        result = [r for r in result if r.active]
        embed = discord.Embed(title="Badges currently available", colour=discord.Colour.purple())
        for r in result:
            send_emoji = self.bot.get_emoji(r.emoji)
            name = f"{send_emoji} {r.name} (#{r.id})"
            embed.add_field(name=name, value=f"     {r.description}", inline=False)
        await ctx.send(embed=embed)

def setup(bot):
    bot.add_cog(BadgeCommands(bot))
