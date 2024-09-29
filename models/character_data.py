from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from .display_name import DisplayName
    from .ue_datatable_reference import UEDataTableReference

from pathlib import Path

class CharacterData:
    """
    This class is responsible for representing a character data.
    #### Parameters
    - `name` : `str`
        - The name of the character data.
    - `icon`: `Path`
        - The icon of the character data.
    - `hud_icon` : `Path`
        - The HUD icon of the character data.
    - `character_name` : `DisplayName`
        - The character name of the character data.
    - `character_tags` : `list[str]`
        - The character tags of the character data.
    - `tameable` : `bool`
        - The tameable of the character data.
    - `taming_food`: `list[UEDataTableReference]`
        - The taming food of the character data.
    - `active_pet_passive_effects` : `list[UEDataTableReference]`
        - The active pet passive effects of the character data.
    - `bestiary_item` : `UEDataTableReference`
        - The bestiary item of the character data.
    - `actor_path`: `str`
        - The actor path of the character data.
    - `unknown_fields` : `dict`
        - The unknown fields of the character data.
    """
    def __init__(self, name: str, icon: Path, hud_icon: Path, character_name: 'DisplayName', character_tags: list[str], tameable: bool, taming_food: list['UEDataTableReference'], active_pet_passive_effects: list['UEDataTableReference'], bestiary_item: 'UEDataTableReference', actor_path: str, unknown_fields: dict):
        self.name = name
        self.icon = icon
        self.hud_icon = hud_icon
        self.character_name = character_name
        self.character_tags = character_tags
        self.tameable = tameable
        self.taming_food = taming_food
        self.active_pet_passive_effects = active_pet_passive_effects
        self.bestiary_item = bestiary_item
        self.actor_path = actor_path
        self.unknown_fields = unknown_fields

    def to_dict(self) -> dict:
        """
        This method is responsible for converting the character data to a dictionary.
        #### Returns
        - `dict` : The converted character data.
        """
        return {
            'name': self.name,
            'icon': self.icon.as_posix(),
            'hud_icon': self.hud_icon.as_posix(),
            'character_name': self.character_name.to_dict(),
            'character_tags': self.character_tags,
            'tameable': self.tameable,
            'taming_food': [taming_food.to_dict() for taming_food in self.taming_food],
            'active_pet_passive_effects': [active_pet_passive_effect.to_dict() for active_pet_passive_effect in self.active_pet_passive_effects],
            'bestiary_item': self.bestiary_item.to_dict(),
            'actor_path': self.actor_path,
            'unknown_fields': self.unknown_fields
        }
        
    def from_dict(data: dict) -> 'CharacterData':
        """
        This method is responsible for converting the dictionary to a CharacterData object.
        #### Parameters
        - `data`: `dict`
            - The dictionary to convert.
        #### Returns
        - `CharacterData` : The converted CharacterData object.
        """
        return CharacterData(
            data['name'],
            Path(data['icon']),
            Path(data['hud_icon']),
            DisplayName.from_dict(data['character_name']),
            data['character_tags'],
            data['tameable'],
            [UEDataTableReference.from_dict(taming_food) for taming_food in data['taming_food']],
            [UEDataTableReference.from_dict(active_pet_passive_effect) for active_pet_passive_effect in data['active_pet_passive_effects']],
            UEDataTableReference.from_dict(data['bestiary_item']),
            data['actor_path'],
            data['unknown_fields']
        )

    @staticmethod
    def get_unknown_fields() -> list[str]:
        """
        This method is responsible for getting the unknown fields of the character data.
        #### Returns
        - `list` : The unknown fields of the character data.
        """
        return [
            'ModIcon',
            'PetPersonalities',
            'PlacementData'
        ]