from typing import Any
from pathlib import Path
from models import DisplayName
from models.status_effect import StatusEffect
from models.item import Item
from models.recipe_component import RecipeComponent
from models.item_effects_info import ItemEffectsInfo
from models.equippable_data import EquippableData
from global_database import GlobalDatabase

import json

class BaseCrawler:
    """
    This class is responsible for crawling the data from the game.
    #### Parameters
    - `crawler_name` : `str`
        - The name of the crawler.
    - `root_path` : `Path`
        - The path to the root directory.
    - `json_path` : `Path`
        - The path to the json data directory.
    - `media_path` : `Path`
        - The path to the media directory.
    - `hide_unknown_fields` : `bool`
        - A flag to hide the unknown fields.
    - `unknown_field_list` : `list`
        - The list of unknown fields.
    """
    root_path: Path = None

    items_table = None
    status_effects_table = None

    def __init__(self, name: str, json_path: Path, hide_unknown_fields: bool = False):
        self.crawler_name = name
        self.json_path = self.root_path / 'json_data' / json_path
        self.lang_path = self.root_path / 'json_data/Maine/Content/Exported/BaseGame/Localized' / BaseCrawler.locale / f'Text/Text_{BaseCrawler.locale}.json'
        self.media_path = self.root_path / 'media_data'
        self.hide_unknown_fields = hide_unknown_fields
        self.unknown_field_list = []
        self.crawled_data = {}

        DisplayName.init(self.lang_path)

    @staticmethod
    def init(root_path: Path, version: str, locale: str = 'enus'):
        """
        This method is responsible for initializing the crawler.
        #### Parameters
        - `root_path` : `Path`
            - The path to the root directory.
        """
        BaseCrawler.version = GameVersion(version)
        BaseCrawler.root_path = Path(f'{root_path}/{version}')
        BaseCrawler.locale = locale

    def dispose(self) -> None:
        """
        This method is responsible for disposing the crawler.
        """
        BaseCrawler.items_table = None
        BaseCrawler.status_effects_table = None

    def crawl(self) -> list:
        """
        This method is responsible for crawling the data from the game.
        #### Returns
        - `list` : The crawled data.
        """
        json_data = self.json_path.read_text()
        data = json.loads(json_data)
        if len(data) > 1:
            print('There are more than 1 entry in the creatures DataTable.')
            return []
        data = data[0]['Rows']
        self.raw_data = data

        crawled_data = {}
        for key, value in data.items():
            if self.hide_unknown_fields:
                unknown_fields = None
            else:
                unknown_fields = self._get_unknown_fields(value, self.unknown_field_list)

            crawled_data[key] = self._get_crawled_data(key, value, unknown_fields)
        
        GlobalDatabase.add_crawled_data(self.crawler_name, crawled_data)

        self._save(crawled_data, f'{self.crawler_name}.json')

        self.dispose()

        self.crawled_data = crawled_data

        return crawled_data

    def _get_display_name(self, string_json: dict) -> DisplayName:
        """
        This method is responsible for getting the display name.
        #### Parameters
        - `string_json` : `dict`
            - The json data of the string.
        #### Returns
        - `DisplayName` : The display name.
        """
        return DisplayName(
            table_id=string_json['StringTableID'],
            string_id=string_json['StringID'],
            string_table_name=string_json['StringTableName']
        )

    def _get_crawled_data(self, key: str, value: dict, unknown_fields: dict[str, Any]) -> Any:
        """
        This method is responsible for getting the crawled data.
        #### Parameters
        - `key` : `str`
            - The key of the data.
        - `value` : `dict`
            - The value of the data.
        - `unknown_fields` : `dict`
            - The unknown fields of the data.
        #### Returns
        - `Any` : The crawled data.
        """
        pass

    # TODO: Refactor this function so it can handle index based unknown fields (like the ones in the creature info)
    def _get_unknown_fields(self, value: dict, fields: list[str]) -> dict[str, Any]:
        """
        This method is responsible for getting the unknown fields of the creature.
        #### Parameters
        - `value` : `dict`
            - The value of the creature.
        - `fields` : `list`
            - The fields to be extracted.
        #### Returns
        - `dict` : The unknown fields of the creature.
        """
        if self.hide_unknown_fields:
            return None

        unknown_fields = {}
        for field in fields:
            if '>' in field:
                keys = field.split('>')
                first_key = keys[0]
                second_key = '>'.join(keys[1:])
                if first_key not in unknown_fields:
                    unknown_fields[first_key] = {}
                unknown_fields[first_key].update(self._get_unknown_fields(value[first_key], [second_key]))
            else:
                unknown_fields[field] = value[field]

        return unknown_fields

    def _get_media_path(self, value: dict) -> Path:
        """
        This method is responsible for getting the media path of the harvest node.
        #### Parameters
        - `value` : `dict`
          - The value of the harvest node.
        #### Returns
        - `Path` : The media path of the harvest node.
        """
        if value == None:
            return Path()
        if 'ObjectPath' in value and value['ObjectPath'] == 'None':
            return Path()
        if 'AssetPathName' in value and value['AssetPathName'] == 'None':
            return Path()
        
        path = value['ObjectPath'] if 'ObjectPath' in value else value['AssetPathName']

        icon_ingame_path = path.replace('Game/', 'Maine/Content/')
        icon_ingame_path = f'{icon_ingame_path.split('.')[0]}.png'
        icon_path = str(self.media_path) + icon_ingame_path
        return Path(icon_path)

    def _build_real_path(self, path: str) -> str:
        """
        This method is responsible for building the real path of a "game file path".
        #### Parameters
        - `path` : `str`
            - The game file path to be built.
        #### Returns
        - `str` : The real path of the path.
        """
        real_path = path.replace('Game/', 'Maine/Content/')
        real_path = f'{real_path.split('.')[0]}.json'
        real_path = str(self.root_path) + '/json_data/' + real_path
        return real_path

    def _get_object_path(self, value: dict) -> Path:
        """
        This method is responsible for getting the object path of the harvest node.
        #### Parameters
        - `value` : `dict`
          - The value of the harvest node.
        #### Returns
        - `Path` : The object path of the harvest node.
        """
        if value == None:
            return Path()
        if 'ObjectPath' in value and value['ObjectPath'] == 'None':
            return Path()

        path = value['ObjectPath']
        object_path = path.replace('Game/', 'Maine/Content/')
        object_path = f'{object_path.split('.')[0]}.json'
        object_path = str(self.root_path) + '/json_data/' + object_path
        return Path(object_path)

    def _save(self, data: list, file_name: str) -> None:
        """
        This method is responsible for saving the data to a file.
        #### Parameters
        - `data` : `list`
            - The data to be saved.
        - `file_name` : `str`
            - The name of the file to save the data.
        """
        crawled_data_path = Path(f'data/crawled/{BaseCrawler.version}')
        if not crawled_data_path.exists():
            crawled_data_path.mkdir(parents=True)
        data_path = crawled_data_path / file_name

        json_data = {}
        for key, value in data.items():
            json_data[key] = value.to_dict()
        data_path.write_text(json.dumps(json_data, indent=4))

    def _parse_status_effect(self, datatable: dict[str, Any]) -> StatusEffect:
        key_name = datatable['RowName']
        object_path = self._get_object_path(datatable['DataTable'])

        if BaseCrawler.status_effects_table is None and 'Table_StatusEffects' in object_path.name:
            BaseCrawler.status_effects_table = json.loads(object_path.read_text(encoding='utf-8'))[0]['Rows']
        elif 'Table_StatusEffects' not in object_path.name:
            raise ValueError('The provided object path is not a status effects table.')
        
        status_effect_json = BaseCrawler.status_effects_table[key_name]

        display_name = DisplayName(
            table_id=status_effect_json['DisplayData']['Name']['StringTableID'],
            string_id=status_effect_json['DisplayData']['Name']['StringID'],
            string_table_name=status_effect_json['DisplayData']['Name']['StringTableName']
        )
        description = DisplayName(
            table_id=status_effect_json['DisplayData']['Description']['StringTableID'],
            string_id=status_effect_json['DisplayData']['Description']['StringID'],
            string_table_name=status_effect_json['DisplayData']['Description']['StringTableName']
        )
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
            show_in_ui=status_effect_json['bShowInUI'],
            effect_tags=status_effect_json['EffectTags'],
            unknown_fields=unknown_fields
        )

    def _parse_equippable_data(self, value: dict) -> EquippableData:
        repair_recipe = []
        recipe = [] if 'RepairRecipe' not in value else value['RepairRecipe']
        for component in recipe:
            quantity = component['ItemCount']
            item = self._parse_item(component['Item'])
            repair_recipe.append(RecipeComponent(
                item_key=item.key_name,
                quantity=quantity,
                display_name=item.name,
                description=item.description,
                icon_path=item.icon_path,
                icon_modifier_path=item.icon_modifier_path,
            ))

        main_status_effects = []
        for status_effect in value['StatusEffects']:
            main_status_effects.append(self._parse_status_effect(status_effect))

        hidden_status_effects = []
        for status_effect in value['HiddenStatusEffects']:
            hidden_status_effects.append(self._parse_status_effect(status_effect))

        item_effects_info = ItemEffectsInfo(
            main_status_effects=main_status_effects,
            hidden_status_effects=hidden_status_effects,
            random_effect_type=value['RandomEffectType']
        )

        unknown_fields = self._get_unknown_fields(value, EquippableData.get_unknown_fields())

        return EquippableData(
            durability=value['Durability'],
            flat_damage_reduction=value['FlatDamageReduction'],
            percentage_damage_reduction=value['PercentageDamageReduction'],
            item_effects_info=item_effects_info,
            repair_recipe=repair_recipe,
            unknown_fields=unknown_fields
        )

    def _parse_item(self, datatable: dict[str, Any]) -> Item:
        key_name = datatable['RowName']
        if key_name == 'None':
            return None
        object_path = self._get_object_path(datatable['DataTable'])

        if BaseCrawler.items_table is None and 'Table_AllItems' in object_path.name:
            BaseCrawler.items_table = json.loads(object_path.read_text(encoding='utf-8'))[0]['Rows']
        elif 'Table_AllItems' not in object_path.name:
            raise ValueError('The provided object path is not an items table.')
        
        # TODO: Keep track of this as this is the only different key that I found
        if key_name == 'CrossbowCrow':
            key_name = 'CrossBowCrow'
        item_json = BaseCrawler.items_table[key_name]

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
            tier=item_json['Tier'],
            equippable_data=self._parse_equippable_data(item_json['EquippableData']),
            actor_name=item_json['WorldActor']['AssetPathName'],
            duplication_cost=item_json['DuplicateBaseCost'],
            stack_size_tag=item_json['StackSizeTag']['TagName'],
            consumable_data=item_json['ConsumableData'],
            consume_animation_type=item_json['ConsumeAnimType'],
            ugc_tag=item_json['PlacementData']['UGCSubcategoryTag']['TagName'],
            unknown_fields=unknown_fields
        )

class GameVersion:
    """
    This class is responsible for handling the game version to ease comparisons across the code.
    """
    def __init__(self, version: str):
        splits = version.split('.')
        self.major = int(splits[0])
        self.minor = int(splits[1])
        self.patch = int(splits[2])
        self.build = int(splits[3]) if len(splits) > 3 else None

    def __str__(self):
        return f'{self.major}.{self.minor}.{self.patch}.{self.build}'