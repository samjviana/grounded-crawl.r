from models import DisplayName
from pathlib import Path

class StatusEffect:
    """
    Represents a status effect in the game.
    #### Parameters
    - `key_name`: `str`
        - The key name of the status effect.
    - `display_name`: `DisplayName`
        - The display name of the status effect.
    - `description`: `DisplayName`
        - The description of the status effect.
    - `icon_path`: `Path`
        - The icon path of the status effect.
    - `effect_type`: `str`
        - The type of the status effect.
    - `value`: `float`
        - The value of the status effect.
    - `duration_type`: `str`
        - The duration type of the status effect.
    - `duration`: `float`
        - The duration of the status effect.
    - `interval`: `float`
        - The interval of the status effect.
    - `max_stack`: `int`
        - The max stack of the status effect.
    - `is_negative_effect`: `bool`
        - A flag to indicate if the status effect is a negative effect.
    - `unknown_fields`: `dict`
        - The unknown fields of the status effect.
    """
    def __init__(self, key_name: str, display_name: DisplayName, description: DisplayName, icon_path: Path, 
                 effect_type: str, value: float, duration_type: str, duration: float, interval: float, 
                 max_stack: int, is_negative_effect: bool, unknown_fields: dict):
        self.key_name = key_name
        self.display_name = display_name
        self.description = description
        self.icon_path = icon_path
        self.effect_type = effect_type
        self.value = value
        self.duration_type = duration_type
        self.duration = duration
        self.interval = interval
        self.max_stack = max_stack
        self.is_negative_effect = is_negative_effect
        self.unknown_fields = unknown_fields

    def to_dict(self) -> dict:
        """
        This method is responsible for converting the object to a dictionary.
        #### Returns
        - `dict` : The dictionary representation of the object.
        """
        return {
            'key_name': self.key_name,
            'display_name': self.display_name.get_string(),
            'description': self.description.get_string(),
            'icon_path': str(self.icon_path),
            'effect_type': self.effect_type,
            'value': self.value,
            'duration_type': self.duration_type,
            'duration': self.duration,
            'interval': self.interval,
            'max_stack': self.max_stack,
            'is_negative_effect': self.is_negative_effect,
            'unknown_fields': self.unknown_fields
        }
    
    @staticmethod
    def get_unknown_fields() -> list[str]:
        """
        This method is responsible for getting the unknown fields of the status effect.
        #### Returns
        - `list` : The unknown fields of the status effect.
        """
        return [
            'DamageTypeFlags',  'DamageType',       'ApplicationTags', 'EffectTags',  
            'DamageSourceTags', 'DamageTargetTags', 'UniqueTag',       'ApplyType',   
            'AttackChargeType', 'ClearFlags',       'ExtraData',       'SpawnedActor',
            'ScreenEffectData', 'VisualEffectData', 'bShowInUI',       'bStackInUI',  
        ]