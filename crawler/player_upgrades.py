
from .base_crawler import BaseCrawler
from pathlib import Path

class PlayerUpgradesCrawler(BaseCrawler):
    """
    This class is responsible for crawling the player_upgrades data from the game.
    """
    def __init__(self, hide_unknown_fields: bool = False):
        super().__init__(
            name='player_upgrades',
            json_path=Path('Maine/Content/Blueprints/DataTables/Table_PlayerUpgrades.json'),
            hide_unknown_fields=hide_unknown_fields
        )
    