# Roulette Bot
## This is a Discord bot that allows users to play roulette with fake coins

### Requirements

- [Python 3.9](https://www.python.org/downloads/) or higher
- Packages listed in [`requirements.txt`](requirements.txt)

If you wish to host an instance of this bot yourself, follow the instructions below.

1. Create an application in the [Discord Developer Portal](https://discord.com/developers/applications)
2. Create a bot for the application
3. Clone this repository
4. Create virtual environment and install dependencies
```bash
$ python -m venv env
$ source env/bin/activate
$ pip install -r requirements.txt
```
5. Copy the bot token from the Developer Portal and add it to environment variables
6. Run the bot with 
```bash 
$ python bot.py
```

### Rules
1. Initially, every user has **100** coins
2. For correctly guessed colour, winnings are **2** times the sum they bet
3. For correctly guessed number, winnings are **36** times the sum they bet


### Commands
- `$balance`: Check your balance in the game.
- `$number <number> <amount>`: Bet on a number in roulette. `<number>` must be an integer between 0 and 36 (inclusive). `<amount>` is the number of coins to bet.
- `$color <color> <amount>`: Bet on a color in roulette. `<color>` must be either "red" or "black". `<amount>` is the number of coins to bet.
- `$help`: Get help for a specific command. Usage: `$help <command>`. If no command is specified, lists available commands.
