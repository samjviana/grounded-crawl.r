
from typing import Any
from .base_crawler import BaseCrawler
from pathlib import Path
from models import PetPersonality, DisplayName

class PetPersonalitiesCrawler(BaseCrawler):
    """
    This class is responsible for crawling the pet_personalities data from the game.
    """
    def __init__(self, hide_unknown_fields: bool = False):
        super().__init__(
            name='pet_personalities',
            json_path=Path('Maine/Content/Blueprints/DataTables/Table_PetPersonalities.json'),
            hide_unknown_fields=hide_unknown_fields
        )
        self.unknown_field_list = [
            'Weight'
        ]

    def _get_crawled_data(self, key: str, value: dict, unknown_fields: dict[str, Any]) -> PetPersonality:
        pet_personality_name = DisplayName(
            table_id=value['DisplayName']['StringTableID'],
            string_id=value['DisplayName']['StringID'],
            string_table_name=value['DisplayName']['StringTableName']
        )

        pet_personality = PetPersonality(
            key_name=key,
            name=pet_personality_name,
            unknown_fields=unknown_fields
        )

        return pet_personality
    
    