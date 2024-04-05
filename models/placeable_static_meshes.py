from __future__ import annotations

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from .display_name import DisplayName
    from .placement_data import PlacementData

from pathlib import Path

class PlaceableStaticMeshes:
    """
    Represents a placeable static mesh that.
    #### Parameters
    - `key_name` : `str`
        - The key name of the placeable static mesh.
    - `mesh_type`: `str`
        - The mesh type of the placeable static mesh.
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
    def __init__(self, key_name: str, mesh_type: str, name: DisplayName, description: DisplayName, icon: Path, mesh: Path, model_viewer_x_rotation: float, model_viewer_y_rotation: float, placement_data: PlacementData, unknown_fields: dict):
        self.key_name = key_name
        self.mesh_type = mesh_type
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
            'mesh_type': self.mesh_type,
            'name': self.name.to_dict(),
            'description': self.description.to_dict(),
            'icon': self.icon.as_posix(),
            'mesh': self.mesh.as_posix(),
            'model_viewer_x_rotation': self.model_viewer_x_rotation,
            'model_viewer_y_rotation': self.model_viewer_y_rotation,
            'placement_data': self.placement_data.to_dict(),
            'unknown_fields': self.unknown_fields
        }