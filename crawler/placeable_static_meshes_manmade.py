
from .base_crawler import BaseCrawler
from pathlib import Path

class PlaceableStaticMeshesManmadeCrawler(BaseCrawler):
    """
    This class is responsible for crawling the placeable_static_meshes_manmade data from the game.
    """
    def __init__(self, hide_unknown_fields: bool = False):
        super().__init__(
            name='placeable_static_meshes_manmade',
            json_path=Path('Maine/Content/Blueprints/DataTables/Table_PlaceableStaticMeshes_Manmade.json'),
            hide_unknown_fields=hide_unknown_fields
        )
    