import json
import uuid

from pathlib import Path
from typing import Any

from models import HarvestNode, DisplayName, UEObject
from .base_crawler import BaseCrawler

class HarvestNodesCrawler(BaseCrawler):
    """
    This class is responsible for crawling the harvest nodes data from the game.
    """
    def __init__(self, hide_unknown_fields: bool = False):
        super().__init__(
            name='harvest_nodes',
            json_path=Path('Maine/Content/Blueprints/DataTables/Table_AllHarvestNodes.json'),
            hide_unknown_fields=hide_unknown_fields
        )
        self.unknown_field_list = [
            'SearchableKeywords',
            'ModelViewerMeshOverride',
            'ModelViewerMaterialsOverride',
            'PlacementData',
        ]

    def _get_crawled_data(self, key: str, value: dict, unknown_fields: dict[str, Any]) -> HarvestNode:
        display_name = DisplayName(
            table_id=value['DisplayName']['StringTableID'],
            string_id=value['DisplayName']['StringID'],
            string_table_name=value['DisplayName']['StringTableName']
        )
        if display_name.string_table_name == 'None':
            display_name.string_table_name = DisplayName.string_table_names[display_name.table_id]

        icon_path = self._get_media_path(value['Icon'])

        harvest_node = HarvestNode(
            name=key,
            display_name=display_name,
            icon=icon_path,
            unknown_fields=unknown_fields,
        )
        return harvest_node    