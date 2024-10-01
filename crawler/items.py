from pathlib import Path
from typing import Any
from crawler.base_crawler import BaseCrawler
from models.item import Item
from models.recipe_component import RecipeComponent
from models.item_effects_info import ItemEffectsInfo
from models.equippable_data import EquippableData

class ItemsCrawler(BaseCrawler):
    """
    Class responsible for crawling the items data.
    """

    def __init__(self, hide_unknown_fields: bool = False):
        super().__init__(
            name='items',
            json_path=Path('Maine/Content/Blueprints/Items/Table_AllItems.json'),
            hide_unknown_fields=hide_unknown_fields
        )
        self.unknown_field_list = Item.get_unknown_fields() 

    def dispose(self) -> None:
        return super().dispose()
    
    def _get_crawled_data(self, key: str, value: dict, unknown_fields: dict[str, Any]) -> Item:
        display_name = self._get_display_name(value['LocalizedDisplayName'])
        description = self._get_display_name(value['LocalizedDescription'])

        icon_path = self._get_media_path(value['Icon'])
        icon_modifier_path = self._get_media_path(value['ModIcon'])

        item = Item(
            key_name=key,
            name=display_name,
            description=description,
            icon_path=icon_path,
            icon_modifier_path=icon_modifier_path,
            tier=value['Tier'],
            equippable_data=self._parse_equippable_data(value['EquippableData']),
            actor_name=value['WorldActor']['AssetPathName'],
            duplication_cost=value['DuplicateBaseCost'],
            stack_size_tag=value['StackSizeTag']['TagName'],
            consumable_data=value['ConsumableData'],
            consume_animation_type=value['ConsumeAnimType'],
            ugc_tag=value['PlacementData']['UGCSubcategoryTag']['TagName'],
            unknown_fields=unknown_fields
        )

        return item