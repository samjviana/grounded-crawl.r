from __future__ import annotations

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from .display_name import DisplayName
    from .ue_object import UEObject

from pathlib import Path

class HarvestNode:
    """
    This class represents a harvest node in the game.
    #### Parameters
    - `name`: `str`
        - The name of the harvest node.
    - `display_name`: `DisplayName`
        - The display name information of the harvest node.
    - `icon`: `pathlib.Path`
        - The path to the icon of the harvest node.
    - `unknown_fields`: `dict`
        - The unknown fields of the harvest node.
    """
    def __init__(self, name: str, display_name: 'DisplayName', icon: Path, unknown_fields: dict):
        self.name = name
        self.display_name = display_name
        self.icon = icon
        self.unknown_fields = unknown_fields

    def to_dict(self) -> dict:
        """
        This method is responsible for converting the harvest node to a dictionary.
        #### Returns
        - `dict` : The converted harvest node.
        """
        return {
            'name': self.name,
            'display_name': self.display_name.to_dict(),
            'icon': self.icon.as_posix(),
            'unknown_fields': self.unknown_fields
        }