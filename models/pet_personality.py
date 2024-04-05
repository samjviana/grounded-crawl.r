from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from .display_name import DisplayName

class PetPersonality:
    """
    Represents a pet personality in the game.
    #### Parameters
    - `key_name` : `str`
        - The key name of the pet personality.
    - `name`: `DisplayName`
        - The name of the pet personality.
    - `unknown_fields` : `dict`
        - The unknown fields of the pet personality.
    """
    def __init__(self, key_name: str, name: 'DisplayName', unknown_fields: dict):
        self.key_name = key_name
        self.name = name
        self.unknown_fields = unknown_fields

    def to_dict(self) -> dict:
        """
        Converts the pet personality to a dictionary.
        #### Returns
        - `dict` : The converted pet personality.
        """
        return {
            'key_name': self.key_name,
            'name': self.name.to_dict(),
            'unknown_fields': self.unknown_fields
        }