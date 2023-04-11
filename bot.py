import asyncio
import os

import discord
from discord.ext import commands

from exceptions import InsufficientBalanceError, WrongNumberError, MinimalBetError, WrongColorError
from roulette import RouletteGame
from models import Player, Bet

TOKEN = os.environ.get('DISCORD_BOT_TOKEN')

intents = discord.Intents(messages=True, message_content=True, guilds=True, guild_messages=True, members=True)
bot = commands.Bot(command_prefix='$', intents=intents)

ROULETTE_SPIN_FREQUENCY_IN_SECONDS = 120
SPECIFY_COLOR_PARAMETERS_MSG = "Please indicate both the color and the amount: $color [color] [amount]"
SPECIFY_NUMBER_PARAMETERS_MSG = "Please indicate both the number and the amount: $number [number] [amount]"
SPIN_THE_WHEEL_MSG = "Spinning the wheel..."
SPIN_RESULT_MSG = "The result is {} {}"
CONGRATS_MSG = "Congrats, you won {} coins!"
SORRY_MSG = "Sorry, you lost the bet."
BALANCE_MSG = "{}'s balance is {} coins."


roulette_game = RouletteGame()


@bot.command(name="balance", help="Check your balance in the game")
async def balance(ctx):
    """
    Retrieves the current balance of the player in the roulette game.
    Args:
    - ctx (discord.ext.commands.Context): The invocation context of the command.
    """
    await ctx.send(BALANCE_MSG.format(ctx.author.name, roulette_game.get_player_balance(str(ctx.author.id))))


@bot.command(name="number", help="Bet on a number in roulette")
async def bet_number_command(ctx, bet_number: int = None, bet_amount: int = None):
    """Place a bet on a number in the roulette game.

    Parameters:
    -----------
    ctx: Context
        The Discord context object.
    bet_number: int
        The number to bet on.
    bet_amount: int
        The amount of the bet.
    """
    if not bet_number or not bet_amount:
        await ctx.send(SPECIFY_NUMBER_PARAMETERS_MSG)
        return

    try:
        player = Player(str(ctx.author.id), ctx.author.name, ctx.channel.id)
        bet = Bet(player, None, bet_number, bet_amount)
        roulette_game.place_bet(bet)

    except (InsufficientBalanceError, WrongNumberError, MinimalBetError) as e:
        await ctx.send(e)


@bot.command(name="color", help="Bet on a color in roulette")
async def bet_color_command(ctx, bet_color: str = None, bet_amount: int = None):
    """Command to allow a player to bet on a color in roulette.

    Parameters:
    -----------
    ctx: Context
        The Discord context object.
    bet_color: str
        The color that the player wants to bet on.
    bet_amount: int
        The amount of the bet.
    """
    if not bet_color or not bet_amount:
        await ctx.send(SPECIFY_COLOR_PARAMETERS_MSG)
        return

    try:
        player = Player(str(ctx.author.id), ctx.author.name, ctx.channel.id)
        bet = Bet(player, bet_color, None, bet_amount)
        roulette_game.place_bet(bet)

    except (InsufficientBalanceError, WrongColorError, MinimalBetError) as e:
        await ctx.send(e)


@bet_number_command.error
@bet_color_command.error
async def bet_color_or_number_command_error(ctx, error):
    """
    An error handler for the `bet_number_command` and `bet_color_command` commands.
    If the error that was raised is a `BadArgument` error, this function sends a message to the user
    indicating that the argument they provided is invalid.

    Parameters:
    -----------
    ctx: commands.Context
        The context of the command invocation.
    error: Exception
        The error that was raised.
    """
    if isinstance(error, commands.BadArgument):
        message = (
            f"'{ctx.current_argument}' is not valid value for '{ctx.current_parameter.name}' parameter, "
            f"use value of {ctx.current_parameter.annotation} type"
        )
        await ctx.send(message)


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

    embed = discord.Embed(title="Commands", description="List of available commands:")
    embed.add_field(name="$balance", value="Check your balance in the game.", inline=False)
    embed.add_field(name="$number [number] [amount]", value="Bet on a number in roulette.", inline=False)
    embed.add_field(name="$color [red/black] [amount]", value="Bet on a color in roulette.", inline=False)
    embed.add_field(name="$help [balance/number/color]", value="Help for commands.", inline=False)

    if not command:
        await ctx.send(embed=embed)
        return

    command_obj = bot.get_command(command)

    if not command_obj or command_obj.hidden:
        await ctx.send(f"Command $help '{command}' not found.")
        await ctx.send(embed=embed)
        return

    usage_text = f"{ctx.prefix}{command_obj.qualified_name} {command_obj.signature.replace('=None', '')}\n"

    embed = discord.Embed(title=f"Help for command `{command}`:\n")
    embed.add_field(name="Description", value=f"{command_obj.help}\n", inline=False)
    embed.add_field(name="Usage", value=usage_text, inline=False)

    await ctx.send(embed=embed)


@bot.event
async def on_ready():
    """
    A coroutine function that is called when the bot is ready to start receiving events.

    This function adds all the users in the server to the game and starts the game loop in a separate task.

    Returns:
        None
    """
    players = [str(player.id) for player in bot.users]
    roulette_game.add_players(players)
    asyncio.create_task(game_loop())


@bot.event
async def on_member_join(member):
    """
    A function that is triggered when a new member joins a server.

    Parameters:
    member (discord.Member): The member who joined the server.

    """
    players = [str(member.id)]
    roulette_game.add_players(players)


async def game_loop():
    """
    Coroutine that runs indefinitely, periodically spinning the roulette wheel and sending the results to the players.
    """
    while True:
        await asyncio.sleep(ROULETTE_SPIN_FREQUENCY_IN_SECONDS)

        winning_number = roulette_game.spin_the_wheel()
        results = roulette_game.calculate_results(winning_number)

        for result in results:
            channel = bot.get_channel(result.player.channel_id)
            await channel.send(SPIN_THE_WHEEL_MSG)
            await channel.send(f"{winning_number} {roulette_game.get_color(winning_number)}")
            await channel.send(result)


bot.run(TOKEN)
