import os

import discord
from discord.ext import commands

from exceptions import WrongNumberError, InsufficientBalanceError, MinimalBetError, WrongColorError
from roulette import RouletteGame

TOKEN = os.environ.get('DISCORD_BOT_TOKEN')

intents = discord.Intents(messages=True, message_content=True, guilds=True, guild_messages=True)
bot = commands.Bot(command_prefix='$', intents=intents)

SPECIFY_COLOR_PARAMETERS_MSG = "Please indicate both the color and the amount: $color [color] [amount]"
SPECIFY_NUMBER_PARAMETERS_MSG = "Please indicate both the number and the amount: $number [number] [amount]"
SPIN_THE_WHEEL_MSG = "Spinning the wheel..."
SPIN_RESULT_MSG = "The result is {} {}"
CONGRATS_MSG = "Congrats, you won {} coins!"
SORRY_MSG = "Sorry, you lost the bet."
BALANCE_MSG = "{}'s balance is {} coins."


@bot.command(name="balance", help="Check your balance in the game")
async def balance(ctx):
    """
    Retrieves the current balance of the player in the roulette game.

    Args:
    - ctx (discord.ext.commands.Context): The invocation context of the command.

    Returns:
    - None

    Raises:
    - None
    """
    roulette = RouletteGame(ctx.author.id)
    await ctx.send(BALANCE_MSG.format(ctx.author.name, roulette.get_balance()))


@bot.command(name="number", help="Bet on a number in roulette")
async def bet_number_command(ctx, bet_number: int = None, bet_amount: int = None):
    """
    Allows the user to bet on a number in roulette.

    Parameters:
    - ctx (discord.ext.commands.Context): The context object representing the invocation of the command.
    - bet_number (int, optional): The number the user wants to bet on. Defaults to None.
    - bet_amount (int, optional): The amount of coins the user wants to bet. Defaults to None.

    Returns:
    - None: The function does not return anything,
            but sends messages to the channel to inform the user of the outcome of the bet.
    """

    if not bet_number or not bet_amount:
        await ctx.send(SPECIFY_NUMBER_PARAMETERS_MSG)
        return

    roulette = RouletteGame(ctx.author.id)

    try:
        roulette.bet_number(bet_number, bet_amount)
        result = roulette.spin_the_wheel()

        await ctx.send(SPIN_THE_WHEEL_MSG)
        await ctx.send(SPIN_RESULT_MSG.format(result, roulette.get_color(result)))

        prize = roulette.calculate_number_prize(bet_number, result, bet_amount)

        if prize > 0:
            roulette.add_to_balance(prize)
            await ctx.send(CONGRATS_MSG.format(prize))
        else:
            await ctx.send(SORRY_MSG)

        await ctx.send(BALANCE_MSG.format(ctx.author.name, roulette.get_balance()))

    except InsufficientBalanceError as e:
        await ctx.send(e)
    except WrongNumberError as e:
        await ctx.send(e)
    except MinimalBetError as e:
        await ctx.send(e)


@bot.command(name="color", help="Bet on a color in roulette")
async def bet_color_command(ctx, bet_color: str = None, bet_amount: int = None):
    """
    Allows the user to bet on a color in roulette.

    Parameters:
    - ctx (discord.ext.commands.Context): The context object representing the invocation of the command.
    - bet_color (str, optional): The color the user wants to bet on (either 'red' or 'black'). Defaults to None.
    - bet_amount (int, optional): The amount of coins the user wants to bet. Defaults to None.

    Returns:
    - None: The function does not return anything,
            but sends messages to the channel to inform the user of the outcome of the bet.
    """

    if not bet_color or not bet_amount:
        await ctx.send(SPECIFY_COLOR_PARAMETERS_MSG)
        return

    roulette = RouletteGame(ctx.author.id)

    try:
        roulette.bet_color(bet_color, bet_amount)
        result = roulette.spin_the_wheel()

        await ctx.send(SPIN_THE_WHEEL_MSG)
        await ctx.send(SPIN_RESULT_MSG.format(result, roulette.get_color(result)))

        prize = roulette.calculate_color_prize(bet_color, result, bet_amount)

        if prize > 0:
            roulette.add_to_balance(prize)
            await ctx.send(CONGRATS_MSG.format(prize))
        else:
            await ctx.send(SORRY_MSG)

        await ctx.send(BALANCE_MSG.format(ctx.author.name, roulette.get_balance()))

    except InsufficientBalanceError as e:
        await ctx.send(e)
    except WrongColorError as e:
        await ctx.send(e)
    except MinimalBetError as e:
        await ctx.send(e)


bot.remove_command('help')


@bot.command(name="help", help="Get help for a specific command. Usage: $help <command>")
async def help_command(ctx, command: str = None):
    """
    Provides help for a specific command, or a list of available commands if no command is specified.

    Args:
    - ctx (discord.ext.commands.Context): The context object representing the invocation of the command.
    - command (str, optional): The name of the command to provide help for. Defaults to None.

    Returns:
    - None: The function does not return anything, but sends messages to the channel to provide help.

    Raises:
    - None
    """

    if not command:
        embed = discord.Embed(title="Commands", description="List of available commands:")
        embed.add_field(name="$balance", value="Check your balance in the game.", inline=False)
        embed.add_field(name="$number [number] [amount]", value="Bet on a number in roulette.", inline=False)
        embed.add_field(name="$color [red/black] [amount]", value="Bet on a color in roulette.", inline=False)

        await ctx.send(embed=embed)
        return

    command_obj = bot.get_command(command)

    if not command_obj or command_obj.hidden:
        await ctx.send(f"Command '{command}' not found.")
        return

    usage_text = f"{ctx.prefix}{command_obj.qualified_name} {command_obj.signature.replace('=None', '')}\n"

    embed = discord.Embed(title=f"Help for command `{command}`:\n")
    embed.add_field(name="Description", value=f"{command_obj.help}\n", inline=False)
    embed.add_field(name="Usage", value=usage_text, inline=False)

    await ctx.send(embed=embed)


bot.run(TOKEN)
