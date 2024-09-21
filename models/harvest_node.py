from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .display_name import DisplayName
    from .ue_object import UEObject
    from models import HarvestNodeInfo

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
    - `asset_path_name`: `str`
        - The asset path name of the harvest node.
    - `month_to_unlock`: `str`
        - The specific month in which the harvest node is unlocked, if any.
    - `subcategory_tag`: `str`
        - The placement subcategory tag of the harvest node.
    - `info`: `HarvestNodeInfo`
        - Detailed information about the harvest node.
    - `unknown_fields`: `dict`
        - The unknown fields of the harvest node.
    """
    def __init__(self, name: str, display_name: 'DisplayName', icon: Path, asset_path_name: str, month_to_unlock: str, subcategory_tag: str, info: 'HarvestNodeInfo', unknown_fields: dict):
        self.name = name
        self.display_name = display_name
        self.icon = icon
        self.asset_path_name = asset_path_name
        self.month_to_unlock = month_to_unlock
        self.subcategory_tag = subcategory_tag
        self.info = info
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
            'asset_path_name': self.asset_path_name,
            'month_to_unlock': self.month_to_unlock,
            'subcategory_tag': self.subcategory_tag,
            'info': self.info.to_dict() if self.info else None,
            'unknown_fields': self.unknown_fields
        }