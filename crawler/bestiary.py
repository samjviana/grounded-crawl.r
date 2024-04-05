import json

from pathlib import Path
from typing import Any

from models import Creature
from .base_crawler import BaseCrawler

class BestiaryCrawler(BaseCrawler):
    """
    This class is responsible for crawling the bestiary data from the game.
    """
    def __init__(self, hide_unknown_fields: bool = False):
        super().__init__(
            name='bestiary',
            json_path=Path('Maine/Content/Blueprints/DataTables/Table_Bestiary.json'),
            hide_unknown_fields=hide_unknown_fields
        )
        self.unknown_field_list = [
            'Creature>SubPathString',
            'Stats',
            'RareUnlockItemData>DataTable',
        ]

    def _get_crawled_data(self, key: str, value: dict, unknown_fields: dict[str, Any]) -> Creature:
        creature = Creature(
            name=key,
            asset_path_name=value['Creature']['AssetPathName'],
            weakpoint_tags=value['WeakpointTags'],
            rare_unlock_item_name=value['RareUnlockItemData']['RowName'],
            rare_drop_chance=value['RareDropChance'],
            unknown_fields=unknown_fields
        )
        return creature