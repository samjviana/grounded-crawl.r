from models.display_name import DisplayName
from models.recipe_component import RecipeComponent
from pathlib import Path

class Item:
    """
    Class that represents an item in the game.
    #### Parameters
    - `key_name` : `str`
        - The key name of the item.
    - `name` : `DisplayName`
        - The name of the item.
    - `description` : `DisplayName`
        - The description of the item.
    - `icon_path` : `Path`
        - The icon path of the item.
    - `icon_modifier_path` : `Path`
        - The icon modifier path of the item.
    - `tier` : `int`
        - The tier of the item.
    - `repair_recipe` : list[RecipeComponent]
        - The repair recipe of the item (if it has one).
    - `actor_name` : `str`
        - The actor name of the item.
    - `duplication_cost`: `int`
        - The duplication cost of the item.
    - `stack_size_tag`: `str`
        - The stack size tag of the item.
    # TODO: This is a temporary field and should be added inside `ConsumableInfo` info in the future.
    - `consumable_data`: `list`
        - The consumable data of the item.
    - `consume_animation_type`: `str`
        - The consume animation type of the item.
    # TODO: This is a temporary field and should be added inside `PlacementData` info in the future.
    - `ugc_tag`: `str`
        - The UGC tag of the item.
    - `unknown_fields` : `dict`
        - The unknown fields of the item.
    """
    def __init__(self, key_name: str, name: DisplayName, description: DisplayName, icon_path: Path, icon_modifier_path: Path, tier: int, repair_recipe: list[RecipeComponent], actor_name: str, duplication_cost: int, stack_size_tag: str, consumable_data: list, consume_animation_type: str, ugc_tag: str, unknown_fields: dict):
        self.key_name = key_name
        self.name = name
        self.description = description
        self.icon_path = icon_path
        self.icon_modifier_path = icon_modifier_path
        self.tier = tier
        self.repair_recipe = repair_recipe
        self.actor_name = actor_name
        self.duplication_cost = duplication_cost
        self.stack_size_tag = stack_size_tag
        self.consumable_data = consumable_data
        self.consume_animation_type = consume_animation_type
        self.ugc_tag = ugc_tag
        self.unknown_fields = unknown_fields

    def to_dict(self) -> dict:
        """
        This method is responsible for converting the item to a dictionary.
        #### Returns
        - `dict` : The converted item.
        """
        return {
            'key_name': self.key_name,
            'name': self.name.to_dict() if self.name else None,
            'description': self.description.to_dict() if self.description else None,
            'icon_path': self.icon_path.as_posix(),
            'icon_modifier_path': self.icon_modifier_path.as_posix(),
            'tier': self.tier,
            'repair_recipe': [component.to_dict() for component in self.repair_recipe],
            'actor_name': self.actor_name,
            'duplication_cost': self.duplication_cost,
            'stack_size_tag': self.stack_size_tag,
            'consumable_data': self.consumable_data,
            'consume_animation_type': self.consume_animation_type,
            'ugc_tag': self.ugc_tag,
            'unknown_fields': self.unknown_fields
        }
    
    def from_dict(data: dict) -> 'Item':
        """
        This method is responsible for converting a dictionary to an item.
        #### Parameters
        - `data` : `dict`
            - The dictionary to convert.
        #### Returns
        - `Item` : The converted item.
        """
        return Item(
            key_name=data['key_name'],
            name=DisplayName.from_dict(data['name']) if data['name'] else None,
            description=DisplayName.from_dict(data['description']) if data['description'] else None,
            icon_path=Path(data['icon_path']),
            icon_modifier_path=Path(data['icon_modifier_path']),
            tier=data['tier'],
            repair_recipe=[RecipeComponent.from_dict(component) for component in data['repair_recipe']],
            actor_name=data['actor_name'],
            duplication_cost=data['duplication_cost'],
            stack_size_tag=data['stack_size_tag'],
            consumable_data=data['consumable_data'],
            consume_animation_type=data['consume_animation_type'],
            ugc_tag=data['ugc_tag'],
            unknown_fields=data['unknown_fields']
        )
    
    @staticmethod
    def get_unknown_fields() -> dict:
        """
        This method is responsible for getting the unknown fields of the item.
        #### Returns
        - `dict` : The unknown fields of the item.
        """
        return []