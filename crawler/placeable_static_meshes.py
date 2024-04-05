
from .base_crawler import BaseCrawler
from pathlib import Path

class PlaceableStaticMeshesCrawler(BaseCrawler):
    """
    This class is responsible for crawling the placeable_static_meshes data from the game.
    """
    def __init__(self, hide_unknown_fields: bool = False):
        super().__init__(
            name='placeable_static_meshes',
            json_path=Path('Maine/Content/Blueprints/DataTables/Table_PlaceableStaticMeshes.json'),
            hide_unknown_fields=hide_unknown_fields
        )
    