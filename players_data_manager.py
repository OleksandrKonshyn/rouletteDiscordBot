import json
from abc import ABC, abstractmethod


class PlayersDataManager(ABC):
    """
    Abstract base class for players data manager.

    This abstract class defines the methods that must be implemented by any subclass that wants to manage players data.
    """

    @abstractmethod
    def load_players_data(self) -> dict[str:int]:
        """
        Load players data and return them as a dictionary.

        Returns:
            dict[str, int]: A dictionary containing players data.
        """
        pass

    @abstractmethod
    def save_players_data(self, players: dict[str:int]) -> None:
        """
        Save players data.

        Args:
            players (dict[str, int]): A dictionary containing the players data to be saved.
        """
        pass


class PlayersDataManagerFileBased(PlayersDataManager):
    """
    Players data manager that saves and loads players data from a JSON file.

    This class implements the abstract methods of PlayersDataManager to load and save players data to a JSON file.
    """

    def load_players_data(self) -> dict[str:int]:
        """
        Load players data from a JSON file.

        Returns:
            dict[str, int]: A dictionary containing players data.
        """
        try:
            with open("users_data.json", "r") as file:
                return json.load(file)
        except (json.decoder.JSONDecodeError, FileNotFoundError):
            return {}

    def save_players_data(self, players: dict[str:int]) -> None:
        """
        Save players data to a JSON file.

        Args:
            players (dict[str, int]): A dictionary containing players data to be saved.
        """
        with open("users_data.json", "w") as file:
            json.dump(players, file)
