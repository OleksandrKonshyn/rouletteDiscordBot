import random
from typing import Tuple

from exceptions import WrongNumberError, WrongColorError, MinimalBetError, InsufficientBalanceError
from models import PlayerBetResult, PlayersStats, Bet
from players_data_manager import PlayersDataManager, PlayersDataManagerFileBased


class RouletteGame:
    """
    A class representing a roulette game.

    Attributes:
        MINIMAL_BET (int): The minimal bet amount.
        STARTING_BALANCE (int): The starting balance amount for a new player.
        NUMBER_PRIZE_MULTIPLIER (int): The multiplier for winning number bets.
        COLOR_PRIZE_MULTIPLIER (int): The multiplier for winning color bets.
        COLORS (Tuple[str, str]): The available colors for betting.
        RED_NUMBERS (Tuple[int, ...]): The red numbers on the roulette table.
        BLACK_NUMBERS (Tuple[int, ...]): The black numbers on the roulette table.
        GREEN_NUMBERS (Tuple[int, ...]): The green numbers on the roulette table.

    Methods:
        __init__(self, players_data_manager: PlayersDataManager = PlayersDataManagerFileBased):
            Initializes a new RouletteGame instance.

        __load_players_data(self) -> dict[str:int]:
            Loads players data using data manager and returns them as a dictionary.

        __save_players_data(self):
            Saves players data using data manager.

        add_players(self, players: list[str]):
            Adds new players to the game.

        spin_the_wheel(self):
            Simulates a spin of the roulette wheel and returns the winning number.

        has_sufficient_funds(self, player_id: str, amount: int) -> bool:
            Checks if the player has sufficient funds to place a bet.

        place_bet(self, bet):
            Places a bet for a player.

        get_color(self, num: int) -> str:
            Returns the color of a given number.

        add_to_balance(self, player_id: str, amount: int) -> None:
            Adds an amount to a player's balance.

        subtract_from_balance(self, player_id: str, amount: int) -> None:
            Subtracts an amount from a player's balance.

        get_player_balance(self, player_id: str):
            Returns the balance of a given player.

        calculate_number_prize(self, num: int, winning_number: int, amount: int) -> int:
            Calculates the prize for a winning number bet.

        calculate_color_prize(self, color: str, winning_number: int, amount: int) -> int:
            Calculates the prize for a winning color bet.

        calculate_prize(self, bet, winning_number):
            Calculates the prize for a given bet.

        calculate_results(self, winning_number: int):
            Calculates the results of the game and returns the statistics for each player.
    """

    MINIMAL_BET: int = 1
    STARTING_BALANCE: int = 100

    NUMBER_PRIZE_MULTIPLIER: int = 36
    COLOR_PRIZE_MULTIPLIER: int = 2

    COLORS: Tuple[str, str] = ("red", "black")

    # fmt: off
    RED_NUMBERS: Tuple[int, ...] = (1, 3, 5, 7, 9, 12, 14, 16, 18, 19, 21, 23, 25, 27, 30, 32, 34, 36,)
    BLACK_NUMBERS: Tuple[int, ...] = (2, 4, 6, 8, 10, 11, 13, 15, 17, 20, 22, 24, 26, 28, 29, 31, 33, 35,)
    # fmt: on
    GREEN_NUMBERS: Tuple[int, ...] = (0,)

    def __init__(self, players_data_manager: PlayersDataManager = PlayersDataManagerFileBased) -> None:
        """
        Initialize a new RouletteGame instance.

        Args:
            players_data_manager (PlayersDataManager, optional): An instance of a class implementing PlayersDataManager
                interface that will be used to load and save players data. Defaults to PlayersDataManagerFileBased.
        """
        self.bets = []
        self.__players_data_manager = players_data_manager()
        self.__players_data = self.__load_players_data()

    def __load_players_data(self) -> dict[str:int]:
        """
        Loads players data using data manager and returns them as a dictionary.

        Returns:
            dict[str, int]: A dictionary containing players data.
        """
        return self.__players_data_manager.load_players_data()

    def __save_players_data(self) -> None:
        """
        Saves players data using data manager.

        Returns:
            None
        """
        self.__players_data_manager.save_players_data(players=self.__players_data)

    def add_players(self, players_ids: list[str]) -> None:
        """
        Adds new players to the game.

        Args:
            players_ids (list[str]): A list of player IDs to be added.

        Returns:
            None
        """
        for player_id in players_ids:
            if player_id not in self.__players_data:
                self.__players_data[player_id] = 100
        self.__save_players_data()

    def spin_the_wheel(self) -> int:
        """Simulates a spin of a roulette wheel and returns the result as an integer from 0 to 36.

        Returns:
            int: The result of the spin.

        """
        return random.randint(0, 36)

    def has_sufficient_funds(self, player_id: str, amount: int) -> bool:
        """Checks whether a player has sufficient funds to make a bet.

        Args:
            player_id (str): The unique identifier of the player.
            amount (int): The amount of the bet.

        Returns:
            bool: True if the player has sufficient funds, False otherwise.
        """
        return (self.get_player_balance(player_id) - amount) >= 0

    def place_bet(self, bet: Bet) -> None:
        """Places a bet on the roulette table.

        This function takes a Bet object as an argument and adds it to the list of bets on the table.
        The function also checks that the color of the bet is valid and that the amount of the bet is greater than zero.
        If the color of the bet is not valid, a WrongColorError is raised.
        If the bet amount is less than or equal to zero, a MinimalBetError is raised.
        If the player does not have sufficient funds, an InsufficientFundsError is raised.

        Args:
            bet (models.Bet): The bet to be placed on the table.

        Raises:
            WrongColorError: If the color of the bet is not valid.
            MinimalBetError: If the bet amount is less than or equal to zero.
            InsufficientFundsError: If the player does not have sufficient funds.

        Returns:
            None.
        """
        color = self.get_color(bet.number) if bet.number else bet.color

        if color.lower() not in self.COLORS:
            raise WrongColorError(color, self.COLORS)
        if bet.amount <= 0:
            raise MinimalBetError(self.MINIMAL_BET)

        self.subtract_from_balance(bet.player.id, bet.amount)
        self.bets.append(bet)

    def get_color(self, num: int) -> str:
        """Returns the color of a number on the roulette table.

        This function takes an integer argument and returns the color of the corresponding number on the roulette table.
        The function checks whether the number is a red, black, or green number and returns the corresponding color.
        If the number is not valid, a WrongNumberError is raised.

        Args:
            num (int): The number to get the color of.

        Raises:
            WrongNumberError: If the number is not valid.

        Returns:
            str: The color of the number (either 'red', 'black', or 'green').
        """
        if num in self.RED_NUMBERS:
            return "red"
        elif num in self.BLACK_NUMBERS:
            return "black"
        elif num in self.GREEN_NUMBERS:
            return "green"
        raise WrongNumberError(num)

    def add_to_balance(self, player_id: str, amount: int) -> None:
        """Adds the specified amount to a player's balance.

        This function takes a player ID and an integer amount as arguments,
        and adds the specified amount to the player's balance.

        The updated balance is then saved to the players data file.

        Args:
            player_id (str): The ID of the player whose balance will be updated.
            amount (int): The amount to add to the player's balance.

        Returns:
        """
        player_balance = self.get_player_balance(player_id)
        self.__players_data[player_id] = player_balance + amount
        self.__save_players_data()

    def subtract_from_balance(self, player_id: str, amount: int) -> None:
        """Subtracts the specified amount from a player's balance.

        This function takes a player ID and an integer amount as arguments,
        and subtracts the specified amount from the player's balance.

        The function first checks whether the player has sufficient funds to cover the bet,
        and raises an InsufficientBalanceError if the balance is not sufficient.

        The updated balance is then saved to the players data file.

        Args:
            player_id (str): The ID of the player whose balance will be updated.
            amount (int): The amount to subtract from the player's balance.

        Raises:
            InsufficientBalanceError: If the player's balance is not sufficient to cover the bet.

        Returns:
            None
        """
        if not self.has_sufficient_funds(player_id, amount):
            raise InsufficientBalanceError(self.get_player_balance(player_id), amount)
        self.__players_data[player_id] -= amount
        self.__save_players_data()

    def get_player_balance(self, player_id: str) -> int:
        """Retrieves the current balance of a player.

        This function takes a player ID as an argument and returns the current balance of the player.
        If the player is not found in the players data file, the function returns 0.

        Args:
            player_id (str): The ID of the player whose balance will be retrieved.

        Returns:
            int: The current balance of the player.
        """
        return self.__players_data.get(player_id, 0)

    def calculate_number_prize(self, num: int, winning_number: int, amount: int) -> int:
        """Calculates the prize amount for a number bet.

        This function takes a number bet, the winning number, and the bet amount as arguments,
        and calculates the prize amount for the bet.

        If the number bet matches the winning number,
        the function returns the bet amount multiplied by the number prize multiplier.

        Otherwise, the function returns 0.

        Args:
            num (int): The number that was bet on.
            winning_number (int): The winning number.
            amount (int): The bet amount.

        Returns:
            int: The prize amount for the number bet.
        """
        return amount * self.NUMBER_PRIZE_MULTIPLIER if num == winning_number else 0

    def calculate_color_prize(self, color: str, winning_number: int, amount: int) -> int:
        """Calculates the prize amount for a color bet.

        This function takes a color bet, the winning number, and the bet amount as arguments,
        and calculates the prize amount for the bet.

        If the color bet matches the color of the winning number,
        the function returns the bet amount multiplied by the color prize multiplier.

        Otherwise, the function returns 0.

        Args:
            color (str): The color that was bet on ('red', 'black', or None for green).
            winning_number (int): The winning number.
            amount (int): The bet amount.

        Returns:
            int: The prize amount for the color bet.
        """
        return amount * self.COLOR_PRIZE_MULTIPLIER if color and color.lower() == self.get_color(winning_number) else 0

    def calculate_prize(self, bet: Bet, winning_number: int) -> int:
        """Calculates the prize amount for a given bet and winning number.

        This function takes a Bet object and the winning number as arguments, and calculates the prize amount for it.
        If Bet object contains a number bet, the function calculates the prize amount using the number prize multiplier.
        If Bet object contains a color bet, the function calculates the prize amount using the color prize multiplier.
        The function returns the prize amount.

        Args:
            bet (Bet): A Bet object representing the bet.
            winning_number (int): The winning number.

        Returns:
            int: The prize amount for the bet.
        """
        if bet.number:
            return self.calculate_number_prize(bet.number, winning_number, bet.amount)
        return self.calculate_color_prize(bet.color, winning_number, bet.amount)

    def calculate_results(self, winning_number: int) -> list:
        """Calculates and returns the results of the game.

        This function takes the winning number as an argument
        and calculates the results of the game based on the bets placed.

        It iterates through the list of bets placed and calculates the prize amount for each bet
        using the calculate_prize function.

        It then adds the prize amount to the player's balance using the add_to_balance function,
        and adds the result to the PlayersStats object.

        The function returns a list of PlayerBetResult objects, containing the results of the game for each player.

        Args:
            winning_number (int): The winning number.

        Returns:
            list: A list of PlayerBetResult objects, containing the results of the game for each player.
        """
        players_stats = PlayersStats()
        while self.bets:
            bet = self.bets.pop()
            prize = self.calculate_prize(bet, winning_number)
            self.add_to_balance(bet.player.id, prize)
            balance = self.get_player_balance(bet.player.id)
            players_stats.add_result(PlayerBetResult(bet.player, prize, balance))
        return players_stats.get_results()
