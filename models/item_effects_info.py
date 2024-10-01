from .status_effect import StatusEffect

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

    def count_valid_effects(self) -> int:
        """
        This method is responsible for counting the valid effects.
        #### Returns
        - `bool` : The result of the count.
        """
        count = 0
        for status_effect in self.main_status_effects:
            if status_effect.display_name.text != 'UNKNOWN':
                count += 1
        for status_effect in self.hidden_status_effects:
            if status_effect.display_name.text != 'UNKNOWN':
                count += 1
        return count

    def to_dict(self) -> 'ItemEffectsInfo':
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
    
    def from_dict(data: dict) -> 'ItemEffectsInfo':
        """
        This method is responsible for converting the dictionary to an ItemEffectsInfo object.
        #### Parameters
        - `data`: `dict`
            - The dictionary to convert.
        #### Returns
        - `ItemEffectsInfo` : The converted ItemEffectsInfo object.
        """
        return ItemEffectsInfo(
            [StatusEffect.from_dict(status_effect) for status_effect in data['main_status_effects']],
            [StatusEffect.from_dict(status_effect) for status_effect in data['hidden_status_effects']],
            data['random_effect_type']
        )