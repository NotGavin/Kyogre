
import discord
from discord.ext import commands
from discord.ext.commands.errors import CommandError
from inspect import signature, getfullargspec
import asyncio

class TeamSetCheckFail(CommandError):
    'Exception raised checks.teamset fails'
    pass

class SubscriptionSetCheckFail(CommandError):
    'Exception raised checks.subscriptionset fails'
    pass

class PvpSetCheckFail(CommandError):
    'Exception raised checks.pvpset fails'
    pass

class JoinSetCheckFail(CommandError):
    'Exception raised checks.joinset fails'
    pass

class WildSetCheckFail(CommandError):
    'Exception raised checks.wildset fails'
    pass

class LureSetCheckFail(CommandError):
    'Exception raised checks.lureset fails'
    pass

class ReportCheckFail(CommandError):
    'Exception raised checks.allowreport fails'
    pass

class RaidSetCheckFail(CommandError):
    'Exception raised checks.raidset fails'
    pass

class EXRaidSetCheckFail(CommandError):
    'Exception raised checks.exraidset fails'
    pass

class ResearchSetCheckFail(CommandError):
    'Exception raised checks.researchset fails'
    pass

class InvasionSetCheckFail(CommandError):
    'Exception raised checks.invasionset fails'
    pass

class MeetupSetCheckFail(CommandError):
    'Exception raised checks.meetupset fails'
    pass

class ArchiveSetCheckFail(CommandError):
    'Exception raised checks.archiveset fails'
    pass

class RegionsSetCheckFail(CommandError):
    'Exception raised checks.regionsset fails'
    pass

class RegionChangeCheckFail(CommandError):
    'Exception raised checks.regionchange fails'
    pass

class InviteSetCheckFail(CommandError):
    'Exception raised checks.inviteset fails'
    pass

class CityChannelCheckFail(CommandError):
    'Exception raised checks.citychannel fails'
    pass

class SubscriptionChannelCheckFail(CommandError):
    'Exception raised checks.subscriptionchannel fails'
    pass

class PvpChannelCheckFail(CommandError):
    'Exception raised checks.pvpchannel fails'
    pass

class RaidChannelCheckFail(CommandError):
    'Exception raised checks.raidchannel fails'
    pass

class EggChannelCheckFail(CommandError):
    'Exception raised checks.eggchannel fails'
    pass

class NonRaidChannelCheckFail(CommandError):
    'Exception raised checks.nonraidchannel fails'
    pass

class ActiveRaidChannelCheckFail(CommandError):
    'Exception raised checks.activeraidchannel fails'
    pass

class ActiveChannelCheckFail(CommandError):
    'Exception raised checks.activechannel fails'
    pass

class CityRaidChannelCheckFail(CommandError):
    'Exception raised checks.cityraidchannel fails'
    pass

class RegionEggChannelCheckFail(CommandError):
    'Exception raised checks.cityeggchannel fails'
    pass

class RegionExRaidChannelCheckFail(CommandError):
    'Exception raised checks.allowexraidreport fails'
    pass

class ExRaidChannelCheckFail(CommandError):
    'Exception raised checks.cityeggchannel fails'
    pass

class ResearchReportChannelCheckFail(CommandError):
    'Exception raised checks.researchreport fails'
    pass

class InvasionReportChannelCheckFail(CommandError):
    'Exception raised checks.invasionreport fails'
    pass

class MeetupReportChannelCheckFail(CommandError):
    'Exception raised checks.meetupreport fails'
    pass

class WildReportChannelCheckFail(CommandError):
    'Exception raised checks.wildreport fails'
    pass

class LureReportChannelCheckFail(CommandError):
    'Exception raised checks.lurereport fails'
    pass

class TradeChannelCheckFail(CommandError):
    'Exception raised checks.tradereport fails'
    pass

class TradeSetCheckFail(CommandError):
    'Exception raised checks.tradeset fails'
    pass

class UserBanned(CommandError):
    'Exception raised checks.is_good_standing fails'
    pass

async def delete_error(message, error, delay):
    await asyncio.sleep(delay)
    try:
        await message.delete()
    except (discord.errors.Forbidden, discord.errors.HTTPException):
        pass
    try:
        await error.delete()
    except (discord.errors.Forbidden, discord.errors.HTTPException):
        pass

def missing_arg_msg(ctx):
    prefix = ctx.prefix.replace(ctx.bot.user.mention, '@' + ctx.bot.user.name)
    command = ctx.invoked_with
    callback = ctx.command.callback
    sig = list(signature(callback).parameters.keys())
    (args, varargs, varkw, defaults, kwonlyargs, kwonlydefaults, annotations) = getfullargspec(callback)
    rq_args = []
    nr_args = []
    if defaults:
        rqargs = args[:(- len(defaults))]
    else:
        rqargs = args
    if varargs:
        if varargs != 'args':
            rqargs.append(varargs)
    arg_num = len(ctx.args) - 1
    sig.remove('ctx')
    args_missing = sig[arg_num:]
    msg = "I'm missing some details! Usage: {prefix}{command}".format(prefix=prefix, command=command)
    for a in sig:
        if kwonlydefaults:
            if a in kwonlydefaults.keys():
                msg += ' [{0}]'.format(a)
                continue
        if a in args_missing:
            msg += ' **<{0}>**'.format(a)
        else:
            msg += ' <{0}>'.format(a)
    return msg

def custom_error_handling(bot, logger):

    @bot.event
    async def on_command_error(ctx, error):
        if ctx.resolved:
            return
        channel = ctx.channel
        prefix = ctx.prefix.replace(ctx.bot.user.mention, '@' + ctx.bot.user.name)
        bot.help_logger.info(f"User: {ctx.author.name}, channel: {channel}, error: {error.__class__.__name__}")
        try:
            bot.help_logger.info(f"Original error: {error.original}")
        except AttributeError:
            pass
        if isinstance(error, commands.MissingRequiredArgument):
            error = await channel.send(embed=discord.Embed(colour=discord.Colour.red(), description=missing_arg_msg(ctx)))
            await delete_error(ctx.message, error, 10)
        elif isinstance(error, commands.BadArgument):
            error = await channel.send(f"The **{prefix}{ctx.command}** command doesn't take a subcommand of **{ctx.subcommand_passed}**")
            await delete_error(ctx.message, error, 20)
        elif isinstance(error, commands.CommandNotFound):
            pass
        elif isinstance(error, commands.CheckFailure):
            pass
        elif isinstance(error, TeamSetCheckFail):
            msg = 'Team Management is not enabled on this server. **{prefix}{cmd_name}** is unable to be used.'.format(cmd_name=ctx.invoked_with, prefix=prefix)
            error = await channel.send(msg)
            await delete_error(ctx.message, error, 10)
        elif isinstance(error, SubscriptionSetCheckFail):
            msg = 'Subscriptions are not enabled on this server. **{prefix}{cmd_name}** is unable to be used.'.format(cmd_name=ctx.invoked_with, prefix=prefix)
            error = await channel.send(msg)
            await delete_error(ctx.message, error, 10)
        elif isinstance(error, WildSetCheckFail):
            msg = 'Wild Reporting is not enabled on this server. **{prefix}{cmd_name}** is unable to be used.'.format(cmd_name=ctx.invoked_with, prefix=prefix)
            error = await channel.send(msg)
            await delete_error(ctx.message, error, 10)
        elif isinstance(error, LureSetCheckFail):
            msg = 'Lure Reporting is not enabled on this server. **{prefix}{cmd_name}** is unable to be used.'.format(cmd_name=ctx.invoked_with, prefix=prefix)
            error = await channel.send(msg)
            await delete_error(ctx.message, error, 10)
        elif isinstance(error, ReportCheckFail):
            msg = 'Reporting is not enabled for this channel. **{prefix}{cmd_name}** is unable to be used.'.format(cmd_name=ctx.invoked_with, prefix=prefix)
            error = await channel.send(msg)
            await delete_error(ctx.message, error, 10)
        elif isinstance(error, RaidSetCheckFail):
            msg = 'Raid Management is not enabled on this server. **{prefix}{cmd_name}** is unable to be used.'.format(cmd_name=ctx.invoked_with, prefix=prefix)
            error = await channel.send(msg)
            await delete_error(ctx.message, error, 10)
        elif isinstance(error, EXRaidSetCheckFail):
            msg = 'EX Raid Management is not enabled on this server. **{prefix}{cmd_name}** is unable to be used.'.format(cmd_name=ctx.invoked_with, prefix=prefix)
            error = await channel.send(msg)
            await delete_error(ctx.message, error, 10)
        elif isinstance(error, ResearchSetCheckFail):
            msg = 'Research Reporting is not enabled on this server. **{prefix}{cmd_name}** is unable to be used.'.format(cmd_name=ctx.invoked_with, prefix=prefix)
            error = await channel.send(msg)
            await delete_error(ctx.message, error, 10)
        elif isinstance(error, InvasionSetCheckFail):
            msg = 'Team Rocket Takeover Reporting is not enabled on this server. **{prefix}{cmd_name}** is unable to be used.'.format(cmd_name=ctx.invoked_with, prefix=prefix)
            error = await channel.send(msg)
            await delete_error(ctx.message, error, 10)
        elif isinstance(error, MeetupSetCheckFail):
            msg = 'Meetup Reporting is not enabled on this server. **{prefix}{cmd_name}** is unable to be used.'.format(cmd_name=ctx.invoked_with, prefix=prefix)
            error = await channel.send(msg)
            await delete_error(ctx.message, error, 10)
        elif isinstance(error, ArchiveSetCheckFail):
            msg = 'Channel Archiving is not enabled on this server. **{prefix}{cmd_name}** is unable to be used.'.format(cmd_name=ctx.invoked_with, prefix=prefix)
            error = await channel.send(msg)
            await delete_error(ctx.message, error, 10)
        elif isinstance(error, RegionsSetCheckFail):
            msg = 'Regions are not enabled on this server. **{prefix}{cmd_name}** is unable to be used.'.format(cmd_name=ctx.invoked_with, prefix=prefix)
            error = await channel.send(msg)
            await delete_error(ctx.message, error, 10)
        elif isinstance(error, InviteSetCheckFail):
            msg = 'EX Raid Invite is not enabled on this server. **{prefix}{cmd_name}** is unable to be used.'.format(cmd_name=ctx.invoked_with, prefix=prefix)
            error = await channel.send(msg)
            await delete_error(ctx.message, error, 10)
        elif isinstance(error, JoinSetCheckFail):
            msg = 'Invite links are not enabled on this server. **{prefix}{cmd_name}** is unable to be used.'.format(cmd_name=ctx.invoked_with, prefix=prefix)
            error = await channel.send(msg)
            await delete_error(ctx.message, error, 10)
        elif isinstance(error, CityChannelCheckFail):
            guild = ctx.guild
            msg = 'Please use **{prefix}{cmd_name}** in '.format(cmd_name=ctx.invoked_with, prefix=prefix)
            city_channels = bot.guild_dict[guild.id]['configure_dict']['raid']['report_channels']
            if len(city_channels) > 10:
                msg += 'a Region report channel.'
            else:
                msg += 'one of the following region channels:'
                for c in city_channels:
                    channel = discord.utils.get(guild.channels, id=c)
                    if channel:
                        msg += '\n' + channel.mention
                    else:
                        msg += '\n#deleted-channel'
            error = await ctx.channel.send(embed=discord.Embed(colour=discord.Colour.red(), description=msg))
            await delete_error(ctx.message, error, 10)
        elif isinstance(error, SubscriptionChannelCheckFail):
            guild = ctx.guild
            msg = 'Please use **{prefix}{cmd_name}** in the following channel'.format(cmd_name=ctx.invoked_with, prefix=prefix)
            subscription_channels = bot.guild_dict[guild.id]['configure_dict']['subscriptions']['report_channels']
            if len(subscription_channels) > 1:
                msg += 's:\n'
            else:
                msg += ': '
            counter = 0
            for c in subscription_channels:
                channel = discord.utils.get(guild.channels, id=c)
                if counter > 0:
                    msg += '\n'
                if channel:
                    msg += channel.mention
                else:
                    msg += '\n#deleted-channel'
                counter += 1
            error = await ctx.channel.send(embed=discord.Embed(colour=discord.Colour.red(), description=msg))
            await delete_error(ctx.message, error, 10)
        elif isinstance(error, PvpChannelCheckFail):
            guild = ctx.guild
            msg = 'Please use **{prefix}{cmd_name}** in the following channel'.format(cmd_name=ctx.invoked_with, prefix=prefix)
            pvp_channels = bot.guild_dict[guild.id]['configure_dict']['pvp']['report_channels']
            if len(pvp_channels) > 1:
                msg += 's:\n'
            else:
                msg += ': '
            counter = 0
            for c in pvp_channels:
                channel = discord.utils.get(guild.channels, id=c)
                if counter > 0:
                    msg += '\n'
                if channel:
                    msg += channel.mention
                else:
                    msg += '\n#deleted-channel'
                counter += 1
            error = await ctx.channel.send(embed=discord.Embed(colour=discord.Colour.red(), description=msg))
            await delete_error(ctx.message, error, 10)
        elif isinstance(error, RaidChannelCheckFail):
            guild = ctx.guild
            msg = 'Please use **{prefix}{cmd_name}** in a Raid channel. Use **{prefix}list** in any '.format(cmd_name=ctx.invoked_with, prefix=prefix)
            city_channels = bot.guild_dict[guild.id]['configure_dict']['raid']['report_channels']
            if len(city_channels) > 10:
                msg += 'Region report channel to see active raids.'
            else:
                msg += 'of the following Region channels to see active raids:'
                for c in city_channels:
                    channel = discord.utils.get(guild.channels, id=c)
                    if channel:
                        msg += '\n' + channel.mention
                    else:
                        msg += '\n#deleted-channel'
            error = await ctx.channel.send(embed=discord.Embed(colour=discord.Colour.red(), description=msg))
            await delete_error(ctx.message, error, 10)
        elif isinstance(error, EggChannelCheckFail):
            guild = ctx.guild
            msg = 'Please use **{prefix}{cmd_name}** in an Egg channel. Use **{prefix}list** in any '.format(cmd_name=ctx.invoked_with, prefix=prefix)
            city_channels = bot.guild_dict[guild.id]['configure_dict']['raid']['report_channels']
            if len(city_channels) > 10:
                msg += 'Region report channel to see active raids.'
            else:
                msg += 'of the following Region channels to see active raids:'
                for c in city_channels:
                    channel = discord.utils.get(guild.channels, id=c)
                    if channel:
                        msg += '\n' + channel.mention
                    else:
                        msg += '\n#deleted-channel'
            error = await ctx.channel.send(embed=discord.Embed(colour=discord.Colour.red(), description=msg))
            await delete_error(ctx.message, error, 10)
        elif isinstance(error, NonRaidChannelCheckFail):
            msg = "**{prefix}{cmd_name}** can't be used in a Raid channel.".format(cmd_name=ctx.invoked_with, prefix=prefix)
            error = await ctx.channel.send(embed=discord.Embed(colour=discord.Colour.red(), description=msg))
            await delete_error(ctx.message, error, 10)
        elif isinstance(error, ActiveRaidChannelCheckFail):
            guild = ctx.guild
            msg = 'Please use **{prefix}{cmd_name}** in an Active Raid channel. Use **{prefix}list** in any '.format(cmd_name=ctx.invoked_with, prefix=prefix)
            city_channels = bot.guild_dict[guild.id]['configure_dict']['raid']['report_channels']
            try:
                egg_check = bot.guild_dict[guild.id]['raidchannel_dict'][ctx.channel.id].get('type',None)
                meetup = bot.guild_dict[guild.id]['raidchannel_dict'][ctx.channel.id].get('meetup',{})
            except:
                egg_check = ""
                meetup = False
            if len(city_channels) > 10:
                msg += 'Region report channel to see active channels.'
            else:
                msg += 'of the following Region channels to see active channels:'
                for c in city_channels:
                    channel = discord.utils.get(guild.channels, id=c)
                    if channel:
                        msg += '\n' + channel.mention
                    else:
                        msg += '\n#deleted-channel'
            if egg_check == "egg" and not meetup:
                msg += '\nThis is an egg channel. The channel needs to be activated with **{prefix}raid <pokemon>** before I accept commands!'.format(prefix=prefix)
            error = await ctx.channel.send(embed=discord.Embed(colour=discord.Colour.red(), description=msg))
            await delete_error(ctx.message, error, 10)
        elif isinstance(error, ActiveChannelCheckFail):
            guild = ctx.guild
            msg = 'Please use **{prefix}{cmd_name}** in an Active channel. Use **{prefix}list** in any '.format(cmd_name=ctx.invoked_with, prefix=prefix)
            city_channels = bot.guild_dict[guild.id]['configure_dict']['raid']['report_channels']
            try:
                egg_check = bot.guild_dict[guild.id]['raidchannel_dict'][ctx.channel.id].get('type',None)
                meetup = bot.guild_dict[guild.id]['raidchannel_dict'][ctx.channel.id].get('meetup',{})
            except:
                egg_check = ""
                meetup = False
            if len(city_channels) > 10:
                msg += 'Region report channel to see active raids.'
            else:
                msg += 'of the following Region channels to see active raids:'
                for c in city_channels:
                    channel = discord.utils.get(guild.channels, id=c)
                    if channel:
                        msg += '\n' + channel.mention
                    else:
                        msg += '\n#deleted-channel'
            if egg_check == "egg" and not meetup:
                msg += '\nThis is an egg channel. The channel needs to be activated with **{prefix}raid <pokemon>** before I accept commands!'.format(prefix=prefix)
            error = await ctx.channel.send(embed=discord.Embed(colour=discord.Colour.red(), description=msg))
            await delete_error(ctx.message, error, 10)
        elif isinstance(error, CityRaidChannelCheckFail):
            guild = ctx.guild
            msg = 'Please use **{prefix}{cmd_name}** in either a Raid channel or '.format(cmd_name=ctx.invoked_with, prefix=prefix)
            city_channels = bot.guild_dict[guild.id]['configure_dict']['raid']['report_channels']
            if len(city_channels) > 10:
                msg += 'a Region report channel.'
            else:
                msg += 'one of the following region channels:'
                for c in city_channels:
                    channel = discord.utils.get(guild.channels, id=c)
                    if channel:
                        msg += '\n' + channel.mention
                    else:
                        msg += '\n#deleted-channel'
            error = await ctx.channel.send(embed=discord.Embed(colour=discord.Colour.red(), description=msg))
            await delete_error(ctx.message, error, 10)
        elif isinstance(error, RegionEggChannelCheckFail):
            guild = ctx.guild
            msg = 'Please use **{prefix}{cmd_name}** in either a Raid Egg channel or '.format(cmd_name=ctx.invoked_with, prefix=prefix)
            city_channels = bot.guild_dict[guild.id]['configure_dict']['raid']['report_channels']
            if len(city_channels) > 10:
                msg += 'a Region report channel.'
            else:
                msg += 'one of the following region channels:'
                for c in city_channels:
                    channel = discord.utils.get(guild.channels, id=c)
                    if channel:
                        msg += '\n' + channel.mention
                    else:
                        msg += '\n#deleted-channel'
            error = await ctx.channel.send(embed=discord.Embed(colour=discord.Colour.red(), description=msg))
            await delete_error(ctx.message, error, 10)
        elif isinstance(error, RegionExRaidChannelCheckFail):
            guild = ctx.guild
            msg = 'Please use **{prefix}{cmd_name}** in either a EX Raid channel or one of the following region channels:'.format(cmd_name=ctx.invoked_with, prefix=prefix)
            city_channels = bot.guild_dict[guild.id]['configure_dict']['exraid']['report_channels']
            if len(city_channels) > 10:
                msg += 'a Region report channel.'
            else:
                msg += 'one of the following region channels:'
                for c in city_channels:
                    channel = discord.utils.get(guild.channels, id=c)
                    if channel:
                        msg += '\n' + channel.mention
                    else:
                        msg += '\n#deleted-channel'
            error = await ctx.channel.send(embed=discord.Embed(colour=discord.Colour.red(), description=msg))
            await delete_error(ctx.message, error, 10)
        elif isinstance(error, ExRaidChannelCheckFail):
            guild = ctx.guild
            msg = 'Please use **{prefix}{cmd_name}** in a EX Raid channel. Use **{prefix}list** in any of the following region channels to see active raids:'.format(cmd_name=ctx.invoked_with, prefix=prefix)
            city_channels = bot.guild_dict[guild.id]['configure_dict']['exraid']['report_channels']
            if len(city_channels) > 10:
                msg += 'a Region report channel.'
            else:
                msg += 'one of the following region channels:'
                for c in city_channels:
                    channel = discord.utils.get(guild.channels, id=c)
                    if channel:
                        msg += '\n' + channel.mention
                    else:
                        msg += '\n#deleted-channel'
            error = await ctx.channel.send(embed=discord.Embed(colour=discord.Colour.red(), description=msg))
            await delete_error(ctx.message, error, 10)
        elif isinstance(error, ResearchReportChannelCheckFail):
            guild = ctx.guild
            msg = 'Please use **{prefix}{cmd_name}** in '.format(cmd_name=ctx.invoked_with, prefix=prefix)
            city_channels = bot.guild_dict[guild.id]['configure_dict']['research']['report_channels']
            if len(city_channels) > 10:
                msg += 'a Region report channel.'
            else:
                msg += 'one of the following region channels:'
                for c in city_channels:
                    channel = discord.utils.get(guild.channels, id=c)
                    if channel:
                        msg += '\n' + channel.mention
                    else:
                        msg += '\n#deleted-channel'
            error = await ctx.channel.send(embed=discord.Embed(colour=discord.Colour.red(), description=msg))
            await delete_error(ctx.message, error, 10)
        elif isinstance(error, MeetupReportChannelCheckFail):
            guild = ctx.guild
            msg = 'Please use **{prefix}{cmd_name}** in '.format(cmd_name=ctx.invoked_with, prefix=prefix)
            city_channels = bot.guild_dict[guild.id]['configure_dict']['meetup']['report_channels']
            if len(city_channels) > 10:
                msg += 'a Region report channel.'
            else:
                msg += 'one of the following region channels:'
                for c in city_channels:
                    channel = discord.utils.get(guild.channels, id=c)
                    if channel:
                        msg += '\n' + channel.mention
                    else:
                        msg += '\n#deleted-channel'
            error = await ctx.channel.send(embed=discord.Embed(colour=discord.Colour.red(), description=msg))
            await delete_error(ctx.message, error, 10)
        elif isinstance(error, WildReportChannelCheckFail):
            guild = ctx.guild
            msg = 'Please use **{prefix}{cmd_name}** in '.format(cmd_name=ctx.invoked_with, prefix=prefix)
            city_channels = bot.guild_dict[guild.id]['configure_dict']['wild']['report_channels']
            if len(city_channels) > 10:
                msg += 'a Region report channel.'
            else:
                msg += 'one of the following region channels:'
                for c in city_channels:
                    channel = discord.utils.get(guild.channels, id=c)
                    if channel:
                        msg += '\n' + channel.mention
                    else:
                        msg += '\n#deleted-channel'
            error = await ctx.channel.send(embed=discord.Embed(colour=discord.Colour.red(), description=msg))
            await delete_error(ctx.message, error, 10)
        elif isinstance(error, LureReportChannelCheckFail):
            guild = ctx.guild
            msg = 'Please use **{prefix}{cmd_name}** in '.format(cmd_name=ctx.invoked_with, prefix=prefix)
            city_channels = bot.guild_dict[guild.id]['configure_dict']['lure']['report_channels']
            if len(city_channels) > 10:
                msg += 'a Region report channel.'
            else:
                msg += 'one of the following region channels:'
                for c in city_channels:
                    channel = discord.utils.get(guild.channels, id=c)
                    if channel:
                        msg += '\n' + channel.mention
                    else:
                        msg += '\n#deleted-channel'
            error = await ctx.channel.send(embed=discord.Embed(colour=discord.Colour.red(), description=msg))
            await delete_error(ctx.message, error, 10)
        elif isinstance(error, RegionChangeCheckFail):
            guild = ctx.guild
            msg = 'Please use **{prefix}{cmd_name}** in '.format(cmd_name=ctx.invoked_with, prefix=prefix)
            city_channels = bot.guild_dict[guild.id]['configure_dict']['regions']['command_channels']
            msg += 'one of the following channels:'
            for c in city_channels:
                channel = discord.utils.get(guild.channels, id=c)
                if channel:
                    msg += '\n' + channel.mention
                else:
                    msg += '\n#deleted-channel'
            error = await ctx.channel.send(embed=discord.Embed(colour=discord.Colour.red(), description=msg))
            await delete_error(ctx.message, error, 10)
        elif isinstance(error, UserBanned):
            message = ctx.message
            await message.author.send("Your ability to use the bot has been disabled. If you believe this is an error, please contact a mod or admin.")
            await asyncio.sleep(2)
            await message.delete()
        else:
            logger.exception(type(error).__name__, exc_info=error)
