from dataclasses import dataclass


@dataclass
class Player:
    """
    A class representing a player in the casino.

    Attributes:
        id (str): The unique identifier of the player.
        name (str): The name of the player.
        channel_id (int): The ID of the channel where the player is playing.
    """

    id: str
    name: str
    channel_id: int


@dataclass
class Bet:
    """
    A class representing a bet made by a player in the casino.

    Attributes:
        player (Player): The player who made the bet.
        color (str or None): The color chosen by the player to bet on. If a number was chosen, this attribute is None.
        number (int or None): The number chosen by the player to bet on. If a color was chosen, this attribute is None.
        amount (int): The amount of money the player bet.
    """

    player: Player
    color: str or None
    number: int or None
    amount: int


@dataclass
class PlayerBetResult:
    """Stores the result of a player's bet.

    Attributes:
        player (Player): The player who placed the bet.
        prize (int): The amount of prize won by the player.
        balance (int): The current balance of the player after the bet.
    """

    player: Player
    prize: int
    balance: int

    def __repr__(self):
        """Returns the string representation of the object.

        Returns:
            str: The string representation of the object.
        """
        return f"{self.player.name} prize: {self.prize} balance: {self.balance}"


class PlayersStats:
    """
    A class representing the overall statistics of all players in the casino.

    Attributes:
        __stats (dict): A dictionary storing the player ID as key and the player's bet result as value.
    """

    def __init__(self) -> None:
        """
        Initializes a new instance of the PlayersStats class.
        """
        self.__stats = {}

    def add_result(self, player_bet_result: PlayerBetResult) -> None:
        """
        Adds a new player's bet result to the overall statistics.

        Args:
            player_bet_result (PlayerBetResult): The player's bet result to be added.
        Returns:
            None
        """
        if item := self.__stats.get(player_bet_result.player.id):
            item.prize += player_bet_result.prize
            item.balance = player_bet_result.balance
        else:
            self.__stats[player_bet_result.player.id] = player_bet_result

    def get_results(self) -> list:
        """
        Returns the overall statistics of all players.

        Returns:
            list: A list containing all player's bet results in the overall statistics.
        """
        return list(self.__stats.values())
