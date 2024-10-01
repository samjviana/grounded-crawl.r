import json
from pathlib import Path
from typing import Any
from crawler.base_crawler import BaseCrawler
from models import ItemSet, StatusEffect, DisplayName, Item, RecipeComponent

class ItemSetsCrawler(BaseCrawler):
    """
    Class responsible for crawling the item sets.
    """
    status_effects_table = None
    items_table = None

    def __init__(self, hide_unknown_fields: bool = False):
        super().__init__(
            name='item_sets',
            json_path=Path('Maine/Content/Blueprints/Items/ItemTables/Table_ItemSets.json'),
            hide_unknown_fields=hide_unknown_fields
        )
        self.unknown_field_list = []

    def dispose(self) -> None:
        ItemSetsCrawler.status_effects_table = None
        ItemSetsCrawler.items_table = None
    
    @staticmethod
    def _get_armor_set_name(item_names: list[str]) -> str:
        if len(item_names) == 0:
            return ''
        
        shortest_string = min(item_names, key=len)
        for length in range(len(shortest_string), 0, -1):
            for start in range(len(shortest_string) - length + 1):
                substring = shortest_string[start:start+length]
                if all(substring in s for s in item_names):
                    armor_set = substring.strip().replace('of the ', '')
                    return armor_set
        
        return ''

    # TODO: Those `_parse_` methods can be moved into a utility class (or made the code depend on each other)
    def _get_crawled_data(self, key: str, value: dict, unknown_fields: dict[str, Any]) -> ItemSet:
        items: list[Item] = []
        for item in value['Items']:
            items.append(self._parse_item(item))

        status_effects = []
        for status_effect in value['StatusEffects']:
            status_effects.append(self._parse_status_effect(status_effect))

        duplications_costs = [item.duplication_cost for item in items]
        duplication_cost = sum(duplications_costs) / len(duplications_costs)
        if any([_duplication_cost != duplication_cost for _duplication_cost in duplications_costs]):
            raise ValueError('The duplication costs of the items in the set are not the same.')

        name = self._get_armor_set_name([item.name.text for item in items])

        tier_set = set([item.tier for item in items])
        if len(tier_set) != 1:
            raise ValueError('The items in the set have different tiers.')
        tier = tier_set.pop()

        item_set = ItemSet(
            key_name=key,
            name=name,
            tier=tier,
            items=items,
            status_effects=status_effects,
            duplication_cost=duplication_cost,
        )

        return item_set