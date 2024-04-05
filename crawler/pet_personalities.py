
from .base_crawler import BaseCrawler
from pathlib import Path

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
    