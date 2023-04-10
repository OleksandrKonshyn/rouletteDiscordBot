import random
from typing import Tuple

from exceptions import WrongNumberError, MinimalBetError, InsufficientBalanceError, WrongColorError
from players_data_manager import PlayersDataManager, PlayersDataManagerFileBased


class RouletteGame:
    """
    A class representing a game of roulette.

    Attributes:
        __current_player_id (str): The ID of the player currently playing the game.
        __players_data_manager (PlayersDataManager, optional): The data manager used to load and save players data.
        __players_data (dict): A dictionary containing data about the players.

    Constants:
        MINIMAL_BET (int): The minimum amount that can be bet.
        STARTING_BALANCE (int): The starting balance for a new player.
        COLORS (Tuple[str, str]): A tuple containing the two possible colors for a bet.
        RED_NUMBERS (Tuple[int, ...]): A tuple containing the numbers that are red on the roulette wheel.
        BLACK_NUMBERS (Tuple[int, ...]): A tuple containing the numbers that are black on the roulette wheel.
        GREEN_NUMBERS (Tuple[int, ...]): A tuple containing the numbers that are green on the roulette wheel.

    Methods:
        __load_players_data(): Loads the players data from the storage.
        __save_players_data(): Saves the players data to the storage.
        get_color(num: int) -> str: Returns the color (red, black, or green) for the given number on the roulette
                                    wheel.
        spin_the_wheel() -> int: Spins the roulette wheel and returns the resulting number.
        has_sufficient_funds(amount: int) -> bool: Returns True if the player has enough coins to make the bet,
                                                   False otherwise.
        bet_number(num: int, amount: int) -> None: Places a bet on a number on the roulette wheel.
        bet_color(color: str, amount: int) -> None: Places a bet on a color on the roulette wheel.
        get_balance() -> int: Returns the player's current balance.
        add_to_balance(prize: int) -> None: Adds the prize to the player's balance.
        calculate_number_prize(num: int, result: int, amount: int) -> int: Calculates the prize
                                                                           for a bet on a number.
        calculate_color_prize(color: str, result: int, amount: int) -> int: Calculates the prize
                                                                            for a bet on a color.
    """

    MINIMAL_BET: int = 1
    STARTING_BALANCE: int = 100

    COLORS: Tuple[str, str] = ("red", "black")

    # fmt: off
    RED_NUMBERS: Tuple[int, ...] = (1, 3, 5, 7, 9, 12, 14, 16, 18, 19, 21, 23, 25, 27, 30, 32, 34, 36,)
    BLACK_NUMBERS: Tuple[int, ...] = (2, 4, 6, 8, 10, 11, 13, 15, 17, 20, 22, 24, 26, 28, 29, 31, 33, 35,)
    # fmt: on
    GREEN_NUMBERS: Tuple[int, ...] = (0,)

    def __init__(self, player_id: int, players_data_manager: PlayersDataManager = PlayersDataManagerFileBased):
        """
        Initializes a new instance of the RouletteGame class.

        Args:
            player_id (int): The ID of the player playing the game.
            players_data_manager (PlayersDataManager, optional): The data manager used to load and save players data.
                Defaults to PlayersDataManagerFileBased.
        """
        self.__current_player_id = str(player_id)
        self.__players_data_manager = players_data_manager()
        self.__players_data = self.__load_players_data()

    def __load_players_data(self) -> dict[str:int]:
        """
        Loads players data using data manager and returns them as a dictionary.

        Returns:
            dict[str, int]: A dictionary containing players data.
        """
        if players_data := self.__players_data_manager.load_players_data():
            return players_data
        return {self.__current_player_id: self.STARTING_BALANCE}

    def __save_players_data(self):
        """
        Saves players data using data manager.
        """
        self.__players_data_manager.save_players_data(players=self.__players_data)

    def get_color(self, num: int) -> str:
        """
        Returns the color of the number on the roulette wheel.

        Args:
            num (int): The number to check the color of.

        Returns:
            str: The color of the number (red, black or green).

        Raises:
            WrongNumberError: If the given number is not on the roulette wheel.
        """
        if num in self.RED_NUMBERS:
            return "red"
        elif num in self.BLACK_NUMBERS:
            return "black"
        elif num in self.GREEN_NUMBERS:
            return "green"
        raise WrongNumberError(num)

    def spin_the_wheel(self) -> int:
        """
        Spins the roulette wheel and returns the result.

        Returns:
            int: The number on which the roulette ball lands.
        """

        return random.randint(0, 36)

    def has_sufficient_funds(self, amount: int) -> bool:
        """
        Checks whether the player has sufficient funds for a bet.

        Args:
            amount (int): The amount of coins the player wants to bet.

        Returns:
            bool: True if the player has sufficient funds, False otherwise.
        """
        return (self.get_balance() - amount) >= 0

    def bet_number(self, num: int, amount: int) -> None:
        """
        Places a bet on a specific number.

        Args:
            num (int): The number to bet on.
            amount (int): The amount of coins to bet.

        Raises:
            WrongNumberError: If the given number is not on the roulette wheel.
            MinimalBetError: If the given amount is less than the minimum bet amount.
            InsufficientBalanceError: If the player does not have sufficient funds to make the bet.
        """
        color = self.get_color(num)
        self.bet_color(color, amount)

    def bet_color(self, color: str, amount: int) -> None:
        """Place a bet on a specific color.

        Args:
            color (str): The color to bet on ('red', 'black', or 'green').
            amount (int): The amount of money to bet.

        Raises:
            WrongColorError: If the provided color is not on the roulette wheel.
            MinimalBetError: If the provided amount is less than or equal to 0.
            InsufficientBalanceError: If the player's balance is less than the provided amount.

        Returns:
            None
        """
        if color.lower() not in self.COLORS:
            raise WrongColorError(color, self.COLORS)
        if amount <= 0:
            raise MinimalBetError(self.MINIMAL_BET)
        if not self.has_sufficient_funds(amount):
            raise InsufficientBalanceError(self.get_balance(), amount)

        self.__players_data[self.__current_player_id] -= amount
        self.__save_players_data()

    def get_balance(self) -> int:
        """Get the current balance of the player.

        Returns:
            int: The current balance of the player.
        """
        return self.__players_data[self.__current_player_id]

    def add_to_balance(self, prize: int) -> None:
        """Add the prize to the player's balance.

        Args:
            prize (int): The amount of money won by the player.

        Returns:
            None
        """
        self.__players_data[self.__current_player_id] += prize
        self.__save_players_data()

    def calculate_number_prize(self, num: int, result: int, amount: int) -> int:
        """
        Calculate the prize amount for a number bet based on the result of the spin.

        Args:
            num (int): The number that was bet on.
            result (int): The result of the spin.
            amount (int): The amount that was bet.

        Returns:
            int: The prize amount for the bet.
        """
        return amount * 36 if num == result else 0

    def calculate_color_prize(self, color: str, result: int, amount: int) -> int:
        """
        Calculate the prize amount for a color bet based on the result of the spin.

        Args:
            color (str): The color that was bet on.
            result (int): The result of the spin.
            amount (int): The amount that was bet.

        Returns:
            int: The prize amount for the bet.
        """
        return amount * 2 if color.lower() == self.get_color(result) else 0
