from __future__ import annotations

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from .display_name import DisplayName
    from .ue_object import UEObject

from pathlib import Path

class Creature:
    """
    This class is responsible for representing a creature.
    #### Parameters
    - `name` : `str`
        - The name of the creature.
    - `asset_path_name` : `str`
        - The asset path name of the creature.
    - `weakpoint_tags` : `list`
        - The weakpoint tags of the creature.
    - `rare_unlock_item_name` : `str`
        - The rare unlock item name of the creature.
    - `rare_drop_chance` : `float`
        - The rare drop chance of the creature.
    - `unknown_fields` : `dict`
        - The unknown fields of the creature.
    """
    def __init__(self, name: str, asset_path_name: str, weakpoint_tags: list, rare_unlock_item_name: str, rare_drop_chance: float, unknown_fields: dict):
        self.name = name
        self.asset_path_name = asset_path_name
        self.weakpoint_tags = weakpoint_tags
        self.rare_unlock_item_name = rare_unlock_item_name
        self.rare_drop_chance = rare_drop_chance
        self.unknown_fields = unknown_fields

    def to_dict(self) -> dict:
        """
        This method is responsible for converting the creature to a dictionary.
        #### Returns
        - `dict` : The converted creature.
        """
        return {
            'name': self.name,
            'asset_path_name': self.asset_path_name,
            'weakpoint_tags': self.weakpoint_tags,
            'rare_unlock_item_name': self.rare_unlock_item_name,
            'rare_drop_chance': self.rare_drop_chance,
            'unknown_fields': self.unknown_fields
        }