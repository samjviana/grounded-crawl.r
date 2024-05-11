from models import DisplayName, MutationTier
from pathlib import Path

class Mutation:
    """
    Represents a mutation(perk) in the game.
    #### Parameters
    - `key_name`: `str`
        - The key name of the mutation.
    - `display_name`: `DisplayName`
        - The name of the mutation in the game.
    - `description`: `DisplayName`
        - The description of the mutation in the game.
    - `icon_path`: `Path`
        - The icon path of the mutation.
    - `stat`: `str`
        - The stat related to the mutation.
    - `tiers`: `list[MutationTier]`
        - The tiers of the mutation.
    - `unknown_fields`: `dict`
        - The unknown fields of the mutation.
    """
    def __init__(self, key_name: str, display_name: DisplayName, description: DisplayName, icon_path: Path, stat: str, tiers: list[MutationTier], unknown_fields: dict):
        self.key_name = key_name
        self.display_name = display_name
        self.description = description
        self.icon_path = icon_path
        self.stat = stat
        self.tiers = tiers
        self.unknown_fields = unknown_fields

    def to_dict(self) -> dict:
        """
        This method is responsible for converting the object to a dictionary.
        #### Returns
        - `dict` : The dictionary representation of the object.
        """
        return {
            'key_name': self.key_name,
            'display_name': self.display_name.to_dict(),
            'description': self.description.to_dict(),
            'icon_path': str(self.icon_path),
            'stat': self.stat,
            'tiers': [tier.to_dict() for tier in self.tiers]
        }
    
    @staticmethod
    def from_dict(data: dict) -> 'Mutation':
        """
        This method is responsible for creating a Mutation from a dictionary.
        #### Parameters
        - `data` : `dict`
            - The dictionary data.
        #### Returns
        - `Mutation` : The created Mutation.
        """
        return Mutation(
            data['key_name'],
            DisplayName.from_dict(data['display_name']),
            DisplayName.from_dict(data['description']),
            Path(data['icon_path']),
            data['stat'],
            [MutationTier.from_dict(tier) for tier in data['tiers']],
            data['unknown_fields']
        )

    @staticmethod
    def get_unknown_fields() -> list[str]:
        """
        This method is responsible for getting the unknown fields of the mutation
        #### Returns
        - `list` : The unknown fields of the mutation.
        """
        return [
            'GlobalVariable'
        ]