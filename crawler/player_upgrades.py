
from .base_crawler import BaseCrawler
from pathlib import Path
from typing import Any
from models import PlayerUpgrade, DisplayName

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
        self.unknown_field_list = [
            'UpgradeType',
            'Tiers'
        ]
    
    def _get_crawled_data(self, key: str, value: dict, unknown_fields: dict[str, Any]) -> PlayerUpgrade:
        name = DisplayName(
            table_id=value['LocalizedDisplayName']['StringTableID'],
            string_id=value['LocalizedDisplayName']['StringID'],
            string_table_name=value['LocalizedDisplayName']['StringTableName']
        )

        player_upgrade = PlayerUpgrade(
            key_name=key,
            name=name,
            icon_asset_path=value['Icon']['AssetPathName'],
            base_cost=value['BaseCost'],
            unknown_fields=unknown_fields
        )

        return player_upgrade