from __future__ import annotations

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from .ue_object import UEObject

from .display_name import DisplayName
from pathlib import Path
from models import CreatureInfo

class Creature:
    """
    This class is responsible for representing a creature.
    #### Parameters
    - `key_name` : `str`
        - The key name of the creature.
    - `name` : `DisplayName`
        - The name of the creature.
    - `asset_path_name` : `str`
        - The asset path name of the creature.
    - `weakpoint_tags` : `list`
        - The weakpoint tags of the creature.
    - `info`: `CreatureInfo`
        - Details about the creature.
    - `rare_unlock_item_name` : `str`
        - The rare unlock item name of the creature.
    - `rare_drop_chance` : `float`
        - The rare drop chance of the creature.
    - `unknown_fields` : `dict`
        - The unknown fields of the creature.
    """
    def __init__(self, key_name: str, name: DisplayName, asset_path_name: str, weakpoint_tags: list, info: CreatureInfo, rare_unlock_item_name: str, rare_drop_chance: float, unknown_fields: dict):
        self.key_name = key_name
        self.name = name
        self.asset_path_name = asset_path_name
        self.weakpoint_tags = weakpoint_tags
        self.info = info
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
            'key_name': self.key_name,
            'name': self.name.to_dict() if self.name else None,
            'asset_path_name': self.asset_path_name,
            'weakpoint_tags': self.weakpoint_tags,
            'info': self.info.to_dict() if self.info else None,
            'rare_unlock_item_name': self.rare_unlock_item_name,
            'rare_drop_chance': self.rare_drop_chance,
            'unknown_fields': self.unknown_fields
        }
    
    valid_damage_types = [
        'general',  'smashing', 'chopping',  'slashing',
        'stabbing', 'fresh',    'salty',     'sour',    
        'spicy',    'burning',  'explosive', 'shock',   
    ]
    def get_weakness_or_resistance(self, damage_type: str) -> float:
        """
        This method is responsible for getting the weakness or resistance of the creature.
        #### Parameters
        - `damage_type` : `str`
            - The damage type to get the weakness or resistance.
        #### Returns
        - `float` : The weakness or resistance multiplier.
        """
        if damage_type not in Creature.valid_damage_types:
            raise ValueError(f"Invalid damage type: {damage_type}")
        if self.info is None:
            return 1.0

        for effect in self.info.status_effects:
            if effect.key_name.startswith('DamageResist') and damage_type in effect.key_name.lower():
                return effect.value
            
        return 1.0

    @staticmethod
    def from_dict(data: dict) -> 'Creature':
        """
        This method is responsible for converting the dictionary to a Creature object.
        #### Parameters
        - `data`: `dict`
            - The dictionary to convert.
        #### Returns
        - `Creature` : The converted Creature object.
        """
        return Creature(
            data['key_name'],
            DisplayName.from_dict(data['name']) if data['name'] else None,
            data['asset_path_name'],
            data['weakpoint_tags'],
            CreatureInfo.from_dict(data['info']) if data['info'] else None,
            data['rare_unlock_item_name'],
            data['rare_drop_chance'],
            data['unknown_fields']
        )
    