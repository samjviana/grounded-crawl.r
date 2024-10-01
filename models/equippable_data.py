from .item_effects_info import ItemEffectsInfo
from .recipe_component import RecipeComponent

class EquippableData:
    """
    This class is responsible for storing data about an equippable item.
    ####
    - `durability` : `float`
        - The durability of the item.
    - `flag_damage_reduction` : `float`
        - The flat damage reduction of the item.
    - `percentage_damage_reduction` : `float`
        - The percentage damage reduction of the item.
    - `item_effects_info` : `ItemEffectsInfo`
        - The effects of the item.
    - `repair_recipe` : `List[RecipeComponent]`
        - The recipe to repair the item.
    - `unknown_fields` : `dict`
        - Any unknown fields.
    """
    def __init__(self, durability: float, flat_damage_reduction: float, percentage_damage_reduction: float, item_effects_info: ItemEffectsInfo, repair_recipe: list[RecipeComponent], unknown_fields: dict):
        self.durability = durability
        self.flat_damage_reduction = flat_damage_reduction
        self.percentage_damage_reduction = percentage_damage_reduction
        self.item_effects_info = item_effects_info
        self.repair_recipe = repair_recipe
        self.unknown_fields = unknown_fields

    def to_dict(self) -> dict:
        """
        This method is responsible for converting the equippable data to a dictionary.
        #### Returns
        - `dict` : The converted equippable data.
        """
        return {
            'durability': self.durability,
            'flat_damage_reduction': self.flat_damage_reduction,
            'percentage_damage_reduction': self.percentage_damage_reduction,
            'item_effects_info': self.item_effects_info.to_dict() if self.item_effects_info else None,
            'repair_recipe': [component.to_dict() for component in self.repair_recipe],
            'unknown_fields': self.unknown_fields
        }
    
    def from_dict(data: dict) -> 'EquippableData':
        """
        This method is responsible for converting a dictionary to equippable data.
        #### Parameters
        - `data` : `dict`
            - The dictionary to convert.
        #### Returns
        - `EquippableData` : The converted equippable data.
        """
        return EquippableData(
            durability=data['durability'],
            flat_damage_reduction=data['flat_damage_reduction'],
            percentage_damage_reduction=data['percentage_damage_reduction'],
            item_effects_info=ItemEffectsInfo.from_dict(data['item_effects_info']) if data['item_effects_info'] else None,
            repair_recipe=[RecipeComponent.from_dict(component) for component in data['repair_recipe']],
            unknown_fields=data['unknown_fields']
        )
    
    @staticmethod
    def get_unknown_fields() -> dict:
        return [
            'EquipAudio', 'EquipAnim', 'HairType', 'RandomEffectType', 'DisablesThirdPersonShadowCastingInFirstPerson'
        ]