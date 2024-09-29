from models import Item, StatusEffect

class ItemSet:
    """
    Class representing a set of items (e.g.: A specific armor set like "Acorn Set").
    #### Parameters
    - `key_name` : `str`
        - The key name of the item set.
    - `name` : `str`
        - The name of the item set.
    - `duplication_cost` : `int`
        - The duplication cost of any item in the set separately.
    - `items` : `list[Item]`
        - The items of the item set.
    - `status_effects` : `list[StatusEffect]`
        - The status effects of the item set.
    """
    def __init__(self, key_name: str, name: str, duplication_cost: int, items: list[Item], status_effects: list[StatusEffect]):
        self.key_name = key_name
        self.name = name
        self.duplication_cost = duplication_cost
        self.items = items
        self.status_effects = status_effects

    def to_dict(self) -> dict:
        """
        This method is responsible for converting the item set to a dictionary.
        #### Returns
        - `dict` : The converted item set.
        """
        return {
            'key_name': self.key_name,
            'name': self.name,
            'duplication_cost': self.duplication_cost,
            'items': [item.to_dict() for item in self.items],
            'status_effects': [status_effect.to_dict() for status_effect in self.status_effects]
        }
    
    def from_dict(data: dict) -> 'ItemSet':
        """
        This method is responsible for converting a dictionary to an item set.
        #### Parameters
        - `data` : `dict`
            - The dictionary to convert.
        #### Returns
        - `ItemSet` : The converted item set.
        """
        return ItemSet(
            key_name=data['key_name'],
            name=data['name'],
            duplication_cost=data['duplication_cost'],
            items=[Item.from_dict(item) for item in data['items']],
            status_effects=[StatusEffect.from_dict(status_effect) for status_effect in data['status_effects']]
        )