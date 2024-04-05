from typing import Any
from .base_crawler import BaseCrawler
from pathlib import Path
from models import PlaceableStaticMeshes, DisplayName, PlacementData

class PlaceableStaticMeshesNaturalCrawler(BaseCrawler):
    """
    This class is responsible for crawling the placeable_static_meshes_natural data from the game.
    """
    def __init__(self, hide_unknown_fields: bool = False):
        super().__init__(
            name='placeable_static_meshes_natural',
            json_path=Path('Maine/Content/Blueprints/DataTables/Table_PlaceableStaticMeshes_Natural.json'),
            hide_unknown_fields=hide_unknown_fields
        )
        self.unknown_field_list = [
            'SearchableKeywords',
            'OverrideMaterials',
            'InspectModelOverrideSoft'
        ]

    def _get_crawled_data(self, key: str, value: dict, unknown_fields: dict[str, Any]) -> PlaceableStaticMeshes:
        name = DisplayName(
            table_id=value['DisplayName']['StringTableID'],
            string_id=value['DisplayName']['StringID'],
            string_table_name=value['DisplayName']['StringTableName']
        )
        description = DisplayName(
            table_id=value['LocalizedDescription']['StringTableID'],
            string_id=value['LocalizedDescription']['StringID'],
            string_table_name=value['LocalizedDescription']['StringTableName']
        )

        icon = self._get_media_path(value['Icon'])
        mesh = self._get_media_path(value['Mesh'])

        placement_data = PlacementData(
            subcategory_tag=value['PlacementData']['UGCSubcategoryTag']['TagName'],
            max_slope=value['PlacementData']['MaxSlope'],
            scale=value['PlacementData']['DefaultScale'],
            unknown_fields=PlacementData.get_unknown_fields()
        )

        placeable_static_meshes_manmade = PlaceableStaticMeshes(
            key_name=key,
            mesh_type='NATURAL',
            name=name,
            description=description,
            icon=icon,
            mesh=mesh,
            model_viewer_x_rotation=value['ModelViewerXRotation'],
            model_viewer_y_rotation=value['ModelViewerYRotation'],
            placement_data=placement_data,
            unknown_fields=unknown_fields
        )

        return placeable_static_meshes_manmade
    