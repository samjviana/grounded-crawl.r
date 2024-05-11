from models import DisplayName, StatusEffect
from pathlib import Path

class MutationTier:
    """
    Represents a mutation(perk) in the game.
    #### Parameters
    - `condition`: `int`
        - The condition of the mutation tier to be unlocked.
    - `status_effects`: `list[StatusEffect]`
        - The status effects unlocked by the mutation tier.
    - `recipes`: `list[str]`
        - The recipes unlocked by the mutation tier.
    """
    def __init__(self, condition: int, status_effects: list[StatusEffect], recipes: list[str]):
        self.condition = condition
        self.status_effects = status_effects
        self.recipes = recipes

    def to_dict(self) -> dict:
        """
        This method is responsible for converting the object to a dictionary.
        #### Returns
        - `dict` : The dictionary representation of the object.
        """
        return {
            'condition': self.condition,
            'status_effects': [status_effect.to_dict() for status_effect in self.status_effects],
            'recipes': self.recipes
        }
    
    @staticmethod
    def from_dict(data: dict) -> 'MutationTier':
        """
        This method is responsible for creating a Mutation from a dictionary.
        #### Parameters
        - `data` : `dict`
            - The dictionary data.
        #### Returns
        - `Mutation` : The created MutationTier.
        """
        return MutationTier(
            data['condition'],
            [StatusEffect.from_dict(status_effect) for status_effect in data['status_effects']],
            data['recipes']
        )

    @staticmethod
    def get_unknown_fields() -> list[str]:
        """
        This method is responsible for getting the unknown fields of the model
        #### Returns
        - `list` : The unknown fields.
        """
        return []