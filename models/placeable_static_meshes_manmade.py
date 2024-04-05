    #   "ArmyManABlue": {
    #     "DisplayName": {
    #       "StringTableID": 342,
    #       "StringID": 3,
    #       "StringTableName": "None"
    #     },
    #     "LocalizedDescription": {
    #       "StringTableID": -1,
    #       "StringID": -1,
    #       "StringTableName": "None"
    #     },
    #     "SearchableKeywords": [],
    #     "Icon": {
    #       "ObjectName": "Texture2D'ICO_Army_Man_A_Blue'",
    #       "ObjectPath": "/Game/Blueprints/Items/Icons/ICO_Army_Man_A_Blue.0"
    #     },
    #     "Mesh": {
    #       "ObjectName": "StaticMesh'SM_Army_Man_A_Blue'",
    #       "ObjectPath": "/Game/Art/World/ZN00_Global/Army_Men/SM_Army_Man_A_Blue.2"
    #     },
    #     "OverrideMaterials": [],
    #     "ModelViewerXRotation": -30.0,
    #     "ModelViewerYRotation": 20.0,
    #     "InspectModelOverrideSoft": {
    #       "AssetPathName": "None",
    #       "SubPathString": ""
    #     },
    #     "PlacementData": {
    #       "bPermitForUGC": true,
    #       "bHasUGCInteractions": false,
    #       "UGCSubcategoryTag": {
    #         "TagName": "Category.ActorPlacement.MeshesManmade.Toys"
    #       },
    #       "Actor": {
    #         "AssetPathName": "/Script/Maine.PlaceableStaticMeshActor",
    #         "SubPathString": ""
    #       },
    #       "ActorFlipped": {
    #         "AssetPathName": "None",
    #         "SubPathString": ""
    #       },
    #       "ActorWall": {
    #         "AssetPathName": "None",
    #         "SubPathString": ""
    #       },
    #       "ActorCeiling": {
    #         "AssetPathName": "None",
    #         "SubPathString": ""
    #       },
    #       "SlotType": "EBuildingSlotType::None",
    #       "bUseAlternateSlotType": true,
    #       "AlternateSlotType": "EBuildingSlotType::Cell",
    #       "EmbedMode": "EBuildingGroundEmbedMode::Encouraged",
    #       "bPlaceAtPlayerRotation": true,
    #       "bPermitExtraRotationAxes": true,
    #       "bPermitRescaling": true,
    #       "bAllowPlaceInWater": false,
    #       "RandomRotateIncrement": 0.0,
    #       "RotationOffset": 0.0,
    #       "BuoyantPlacement": "EBuildingBuoyantPlacementMode::None",
    #       "TerrainConform": "EBuildingTerrainConformMode::MatchTerrain",
    #       "MaxSlope": 360.0,
    #       "OverridePlacementDistance": 0.0,
    #       "PlacementOriginOffset": {
    #         "X": 0.0,
    #         "Y": 0.0,
    #         "Z": 0.0
    #       },
    #       "AttachedPlacementOffset": {
    #         "X": 0.0,
    #         "Y": 0.0,
    #         "Z": 0.0
    #       },
    #       "bDoOverrideAllowedWallNormal": false,
    #       "OverrideAllowedWallNormal": {
    #         "LowerBound": {
    #           "Type": "ERangeBoundTypes::Open",
    #           "Value": 0.0
    #         },
    #         "UpperBound": {
    #           "Type": "ERangeBoundTypes::Open",
    #           "Value": 0.0
    #         }
    #       },
    #       "DefaultScale": 1.0
    #     }
    #   },
from __future__ import annotations

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from .display_name import DisplayName
    from .placement_data import PlacementData

from pathlib import Path

class PlaceableStaticMeshesManmade:
    """
    Represents a placeable static mesh that is manmade.
    #### Parameters
    - `key_name` : `str`
        - The key name of the placeable static mesh.
    - `name` : `DisplayName`
        - The name of the placeable static mesh.
    - `description` : `DisplayName`
        - The description of the placeable static mesh.
    - `icon` : `Path`
        - The icon of the placeable static mesh.
    - `mesh` : `Path`
        - The mesh of the placeable static mesh.
    - `model_viewer_x_rotation` : `float`
        - The model viewer x rotation of the placeable static mesh.
    - `model_viewer_y_rotation` : `float`
        - The model viewer y rotation of the placeable static mesh.
    - `placement_data` : `PlacementData`
        - The placement data of the placeable static mesh.
    - `unknown_fields` : `dict`
        - The unknown fields of the placeable static mesh.
    """
    def __init__(self, key_name: str, name: 'DisplayName', description: 'DisplayName', icon: Path, mesh: Path, model_viewer_x_rotation: float, model_viewer_y_rotation: float, placement_data: 'PlacementData', unknown_fields: dict):
        self.key_name = key_name
        self.name = name
        self.description = description
        self.icon = icon
        self.mesh = mesh
        self.model_viewer_x_rotation = model_viewer_x_rotation
        self.model_viewer_y_rotation = model_viewer_y_rotation
        self.placement_data = placement_data
        self.unknown_fields = unknown_fields

    def to_dict(self) -> dict:
        """
        Converts the placeable static mesh to a dictionary.
        #### Returns
        - `dict` : The converted placeable static mesh.
        """
        return {
            'key_name': self.key_name,
            'name': self.name.to_dict(),
            'description': self.description.to_dict(),
            'icon': self.icon.as_posix(),
            'mesh': self.mesh.as_posix(),
            'model_viewer_x_rotation': self.model_viewer_x_rotation,
            'model_viewer_y_rotation': self.model_viewer_y_rotation,
            'placement_data': self.placement_data.to_dict(),
            'unknown_fields': self.unknown_fields
        }