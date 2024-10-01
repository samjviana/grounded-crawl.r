from .item import Item
from .recipe_component import RecipeComponent

class CraftingRecipe:
    """
    A recipe for crafting an item.
    #### Parameters
    - `key_name` : `str`
        - The key name of the recipe.
    - `item` : `Item`
        - The item that the recipe crafts.
    - `components` : `list[RecipeComponent]`
        - The components required to craft the item.
    - `quantity` : `int`
        - The quantity of the item that the recipe crafts.
    - `category` : `str`
        - The category of the recipe.
    - `unknown_fields` : `dict`
        - The unknown fields of the recipe.
    """

    def __init__(self, key_name: str, item: Item, components: list[RecipeComponent], quantity: int, category: str, unknown_fields: dict):
        self.key_name = key_name
        self.item = item
        self.components = components
        self.quantity = quantity
        self.category = category
        self.unknown_fields = unknown_fields

    def to_dict(self) -> dict:
        """
        This method is responsible for converting the recipe to a dictionary.
        #### Returns
        - `dict` : The converted recipe.
        """
        return {
            'key_name': self.key_name,
            'item': self.item.to_dict() if self.item else None,
            'components': [component.to_dict() if component else None for component in self.components],
            'quantity': self.quantity,
            'category': self.category,
            'unknown_fields': self.unknown_fields
        }
    
    def from_dict(data: dict) -> 'CraftingRecipe':
        """
        This method is responsible for converting a dictionary to a recipe.
        #### Parameters
        - `data` : `dict`
            - The dictionary to convert.
        #### Returns
        - `CraftingRecipe` : The converted recipe.
        """
        return CraftingRecipe(
            key_name=data['key_name'],
            item=Item.from_dict(data['item']) if data['item'] else None,
            components=[RecipeComponent.from_dict(component) if component else None for component in data['components']],
            quantity=data['quantity'],
            category=data['category'],
            unknown_fields=data['unknown_fields']
        )

    @staticmethod
    def get_unknown_fields() -> dict:
        """
        This method is responsible for getting the unknown fields of the recipe.
        #### Returns
        - `dict` : The unknown fields of the recipe.
        """
        return [
            'ToolRequired',                 'CraftingBuildingTag',  'RecipeMods',           'bBurgleQuestCanCraft',
            'BurgleQuestCraftRewardLevel',  'BurgleQuestMinCount',  'BurgleQuestMaxCount',  'BurgleQuestMaxCountProgress',
            'Visibility',                   'bWasCut',              'bHideInCraftingMenu',  'bDontAutoUnlockInCreative',
            'bQuestCritical',               'ReplaceRecipe',
        ]