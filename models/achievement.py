import uuid

class Achievement:
    """
    This class represents an achievement.
    #### Parameters
    - `id`: `uuid.UUID`
      - The id of the achievement.
    - `name`: `str`
        - The name of the achievement.
    - `unlock_tag`: `str`
        - The tag of the achievement.
    - `can_unlock_in_creative`: `bool`
        - Whether the achievement can be unlocked in creative mode.
    - `unknown_fields`: `dict`
        - The unknown fields of the achievement.
    """
    def __init__(self, id: uuid.UUID, name: str, unlock_tag: str, can_unlock_in_creative: bool, unknown_fields: dict):
        self.id = id
        self.name = name
        self.unlock_tag = unlock_tag
        self.can_unlock_in_creative = can_unlock_in_creative
        self.unknown_fields = unknown_fields
    
    def to_dict(self) -> dict:
        """
        This method is responsible for converting the achievement to a dictionary.
        #### Returns
        - `dict` : The converted achievement.
        """
        return {
            'id': str(self.id),
            'name': self.name,
            'unlock_tag': self.unlock_tag,
            'can_unlock_in_creative': self.can_unlock_in_creative,
            'unknown_fields': self.unknown_fields
        }