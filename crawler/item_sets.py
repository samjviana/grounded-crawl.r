import json
from pathlib import Path
from typing import Any
from crawler.base_crawler import BaseCrawler
from models import ItemSet, StatusEffect, DisplayName, Item

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
    
    def _parse_item(self, datatable: dict[str, Any]) -> Item:
        key_name = datatable['RowName']
        object_path = self._get_object_path(datatable['DataTable'])

        if ItemSetsCrawler.items_table is None and 'Table_AllItems' in object_path.name:
            ItemSetsCrawler.items_table = json.loads(object_path.read_text(encoding='utf-8'))[0]['Rows']
        elif 'Table_AllItems' not in object_path.name:
            raise ValueError('The provided object path is not an items table.')
        
        item_json = ItemSetsCrawler.items_table[key_name]

        display_name = self._get_display_name(item_json['LocalizedDisplayName'])
        description = self._get_display_name(item_json['LocalizedDescription'])

        icon_path = self._get_media_path(item_json['Icon'])
        icon_modifier_path = self._get_media_path(item_json['ModIcon'])

        unknown_fields = self._get_unknown_fields(item_json, Item.get_unknown_fields())

        return Item(
            key_name=key_name,
            name=display_name,
            description=description,
            icon_path=icon_path,
            icon_modifier_path=icon_modifier_path,
            actor_name=item_json['WorldActor']['AssetPathName'],
            duplication_cost=item_json['DuplicateBaseCost'],
            stack_size_tag=item_json['StackSizeTag']['TagName'],
            consumable_data=item_json['ConsumableData'],
            consume_animation_type=item_json['ConsumeAnimType'],
            ugc_tag=item_json['PlacementData']['UGCSubcategoryTag']['TagName'],
            unknown_fields=unknown_fields
        )

    def _parse_status_effect(self, datatable: dict[str, Any]) -> StatusEffect:
        # TODO: Move this to a separate crawler
        key_name = datatable['RowName']
        object_path = self._get_object_path(datatable['DataTable'])

        if ItemSetsCrawler.status_effects_table is None and 'Table_StatusEffects' in object_path.name:
            ItemSetsCrawler.status_effects_table = json.loads(object_path.read_text(encoding='utf-8'))[0]['Rows']
        elif 'Table_StatusEffects' not in object_path.name:
            raise ValueError('The provided object path is not a status effects table.')
        
        status_effect_json = ItemSetsCrawler.status_effects_table[key_name]

        display_name = self._get_display_name(status_effect_json['DisplayData']['Name'])
        description = self._get_display_name(status_effect_json['DisplayData']['Description'])
        icon_path = self._get_media_path(status_effect_json['DisplayData']['Icon'])

        unknown_fields = self._get_unknown_fields(status_effect_json, StatusEffect.get_unknown_fields())

        return StatusEffect(
            key_name=key_name,
            display_name=display_name,
            description=description,
            icon_path=icon_path,
            effect_type=status_effect_json['Type'],
            value=status_effect_json['Value'],
            duration_type=status_effect_json['DurationType'],
            duration=status_effect_json['Duration'],
            interval=status_effect_json['Interval'],
            max_stack=status_effect_json['MaxStackCount'],
            is_negative_effect=status_effect_json['bIsNegativeEffectInUI'],
            effect_tags=status_effect_json['EffectTags'],
            unknown_fields=unknown_fields
        )

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

        item_set = ItemSet(
            key_name=key,
            name=key.replace('Set', ''),
            items=items,
            status_effects=status_effects,
            duplication_cost=duplication_cost,
        )

        return item_set
