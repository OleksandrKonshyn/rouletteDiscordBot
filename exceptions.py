class InsufficientBalanceError(Exception):
    """
    Exception raised when a player tries to place a bet that exceeds their current balance.

    Attributes:
        balance (int): The current balance of the player.
        bet (int): The amount of coins the player is trying to bet.
        message (str): The error message.
    """

    def __init__(self, balance: int, bet: int):
        """
        Initializes the InsufficientBalanceError with the player's balance and the amount they are trying to bet.

        Args:
            balance (int): The current balance of the player.
            bet (int): The amount of coins the player is trying to bet.
        """
        self.balance = balance
        self.bet = bet
        self.message = f"Player's balance {balance} coins is not enough to bet {bet} coins"
        super().__init__(self.message)


class WrongColorError(Exception):
    """
    Exception raised when a player selects an invalid color to bet on.

    Attributes:
        color (str): The color selected by the player.
        colors (list): The available colors to bet on.
        message (str): The error message.
    """

    def __init__(self, color: str, colors: tuple[str, str]):
        """
        Initializes the WrongColorError with the selected color and the available colors.

        Args:
            color (str): The color selected by the player.
            colors (list): The available colors to bet on.
        """
        self.color = color
        self.colors = colors
        self.message = (
            f"The color '{color}' you have chosen is not valid. "
            f"Please choose a color from the available range: {colors}."
        )
        super().__init__(self.message)


class WrongNumberError(Exception):
    """
    Exception raised when a player selects an invalid number to bet on.

    Attributes:
        num (int): The number selected by the player.
        message (str): The error message.
    """

    def __init__(self, num: int):
        """
        Initializes the WrongNumberError with the selected number.

        Args:
            num (int): The number selected by the player.
        """
        self.num = num
        self.message = f"The number '{num}' you have selected is not valid. Please choose a number between 0 and 36."
        super().__init__(self.message)


class MinimalBetError(Exception):
    """
    Exception raised when a player tries to place a bet that is below the minimal bet.

    Attributes:
        minimal_bet (int): The minimal bet allowed.
        message (str): The error message.
    """

    def __init__(self, minimal_bet: int):
        """
        Initializes the MinimalBetError with the minimal bet allowed.

        Args:
            minimal_bet (int): The minimal bet allowed.
        """
        self.minimal_bet = minimal_bet
        self.message = f"The minimal bet is '{minimal_bet}' coin"
        super().__init__(self.message)
