from typing import Any
from .base_crawler import BaseCrawler
from pathlib import Path
from models import CharacterData, DisplayName, UEDataTableReference, UEObject

class CharacterDataCrawler(BaseCrawler):
    """
    This class is responsible for crawling the character_data data from the game.
    """
    def __init__(self, hide_unknown_fields: bool = False):
        super().__init__(
            name='character_data',
            json_path=Path('Maine/Content/Blueprints/DataTables/Table_CharacterData.json'),
            hide_unknown_fields=hide_unknown_fields
        )
        self.unknown_field_list = [
            'ModIcon',
            'PetPersonalities',
            'PlacementData'
        ]

    def _get_crawled_data(self, key: str, value: dict, unknown_fields: dict[str, Any]) -> CharacterData:
        icon = self._get_media_path(value['Icon'])
        hud_icon = self._get_media_path(value['HudIcon'])

        character_name = DisplayName(
            table_id=value['CharacterName']['StringTableID'],
            string_id=value['CharacterName']['StringID'],
            string_table_name=value['CharacterName']['StringTableName']
        )
        if character_name.string_table_name == 'None':
            character_name.string_table_name = DisplayName.string_table_names[character_name.table_id]

        active_pet_passive_effects = []
        for active_pet_passive_effect_json in value['ActivePetPassiveEffects']:
            ue_object = UEObject(
                name=active_pet_passive_effect_json['DataTable']['ObjectName'],
                path=active_pet_passive_effect_json['DataTable']['ObjectPath']
            )
            active_pet_passive_effect = UEDataTableReference(
                row_name=active_pet_passive_effect_json['RowName'],
                data_table=ue_object
            )
            active_pet_passive_effects.append(active_pet_passive_effect)

        taming_food = []
        for taming_food_json in value['TamingFood']:
            ue_object = UEObject(
                name=taming_food_json['DataTable']['ObjectName'],
                path=taming_food_json['DataTable']['ObjectPath']
            )
            taming_food_item = UEDataTableReference(
                row_name=taming_food_json['RowName'],
                data_table=ue_object
            )
            taming_food.append(taming_food_item)

        bestiary_item = UEDataTableReference(
            row_name=value['BestiaryItem']['RowName'],
            data_table=UEObject(
                name=value['BestiaryItem']['DataTable']['ObjectName'],
                path=value['BestiaryItem']['DataTable']['ObjectPath']
            )
        )

        character_data = CharacterData(
            name=key,
            icon=icon,
            hud_icon=hud_icon,
            character_name=character_name,
            character_tags=value['CharacterTags'],
            tameable=value['bTameable'],
            taming_food=taming_food,
            active_pet_passive_effects=active_pet_passive_effects,
            bestiary_item=bestiary_item,
            unknown_fields=unknown_fields
        )

        return character_data
    