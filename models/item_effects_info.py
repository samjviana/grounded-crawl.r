from models import StatusEffect

class ItemEffectsInfo:
    """
    A class to represent data related to the effects of an item.
    #### Parameters
    - `main_status_effects`: `list[StatusEffect]`
        - The main status effects of the item.
    - `hidden_status_effects`: `list[StatusEffect]`
        - The hidden status effects of the item.
    - `random_effect_type`: `str`
        - The random effect type of the item.
    """
    def __init__(self, main_status_effects: list[StatusEffect], hidden_status_effects: list[StatusEffect], random_effect_type: str):
        self.main_status_effects = main_status_effects
        self.hidden_status_effects = hidden_status_effects
        self.random_effect_type = random_effect_type

    def to_dict(self) -> dict:
        """
        This method is responsible for converting the Item Effects data to a dictionary.
        #### Returns
        - `dict` : The converted Item Effects data.
        """
        return {
            'main_status_effects': [status_effect.to_dict() for status_effect in self.main_status_effects],
            'hidden_status_effects': [status_effect.to_dict() for status_effect in self.hidden_status_effects],
            'random_effect_type': self.random_effect_type
        }