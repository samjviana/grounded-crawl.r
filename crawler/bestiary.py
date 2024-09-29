import json
import os

from pathlib import Path
from typing import Any

from models import Creature, CreatureInfo, StatusEffect, DisplayName, Item, CharacterData
from models import UEDataTableReference, UEObject, Weakpoint
from .base_crawler import BaseCrawler

class BestiaryCrawler(BaseCrawler):
    """
    This class is responsible for crawling the bestiary data from the game.
    """
    status_effects_table = None
    items_table = None
    character_data_table = None

    def __init__(self, hide_unknown_fields: bool = False):
        super().__init__(
            name='bestiary',
            json_path=Path('Maine/Content/Blueprints/DataTables/Table_Bestiary.json'),
            hide_unknown_fields=hide_unknown_fields
        )
        self.unknown_field_list = [
            'Creature>SubPathString',
            'Stats'
        ]

    def dispose(self) -> None:
        BestiaryCrawler.status_effects_table = None
        BestiaryCrawler.items_table = None
        BestiaryCrawler.character_data_table = None

    def _parse_item(self, datatable: dict[str, Any]) -> Item:
        key_name = datatable['RowName']
        object_path = self._get_object_path(datatable['DataTable'])

        if BestiaryCrawler.items_table is None and 'Table_AllItems' in object_path.name:
            BestiaryCrawler.items_table = json.loads(object_path.read_text(encoding='utf-8'))[0]['Rows']
        elif 'Table_AllItems' not in object_path.name:
            raise ValueError('The provided object path is not an items table.')
        
        item_json = BestiaryCrawler.items_table[key_name]

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

    # TODO: Revise this parsing since the Creature Blueprint has a structure of its own
    def _parse_creature_info(self, asset_path_name: str) -> tuple[DisplayName, CreatureInfo]:
        creature_bp_path = self._build_real_path(asset_path_name)
        creature_bp = None
        if not os.path.exists(creature_bp_path):
            return None, None
        with open(creature_bp_path, 'r') as file:
            creature_bp = json.load(file)
        if creature_bp is None:
            return None, None
        
        components = {
            'DefaultComponent': {},
            'HealthComponent': {},
            'LootComponent': {},
            'ReactionComponent': {},
            'StatusEffectComponent': {},
            'TeamComponent': {}
        }
        for component in creature_bp:
            if component['Name'].startswith('Default__'):
                components['DefaultComponent'] = component['Properties']
                continue
            if component['Type'] not in components:
                continue

            components[component['Type']] = {}
            if 'Properties' in component:
                components[component['Type']] = component['Properties']

            if 'Template' in component:
                components[f'{component["Type"]}Template'] = component['Template']
        
        creature_info = CreatureInfo(
            health=None,
            base_damage_reduction=None,
            weakpoints=None,
            loot=None,
            max_stun=None,
            stun_decay=None,
            stun_duration=None,
            stun_cooldown=None,
            status_effects=None,
            immunity_tags=None,
            team=None,
            unknown_fields=None
        )   
        name = None 
        for component in components:
            if component.endswith('Template'):
                templated_name, template = self._parse_creature_info(components[component]['ObjectPath'])

                if template is not None:
                    creature_info = template

                if component.startswith('Default__'):
                    continue
                elif component.startswith('HealthComponent'):
                    creature_info.health = template.health
                    creature_info.base_damage_reduction = template.base_damage_reduction
                    if templated_name is not None:
                        name = templated_name
                elif component.startswith('LootComponent'):
                    continue
                elif component.startswith('ReactionComponent'):
                    continue
                elif component.startswith('StatusEffectComponent'):
                    continue
                elif component.startswith('TeamComponent'):
                    continue

        try:
            creature_info.health = components['HealthComponent']['MaxHealth']
        except:
            pass

        try:
            creature_info.base_damage_reduction = components['HealthComponent']['BaseDamageReduction']
        except:
            pass

        weakpoints = []
        collision_configs = [] if 'ColliderConfigs' not in components['HealthComponent'] else components['HealthComponent']['ColliderConfigs']
        for weakpoint in collision_configs:
            weakpoints.append(Weakpoint(
                key_name=weakpoint['ComponentName'],
                damage_multiplier=weakpoint['DamageMultiplier'],
                damage_sources=weakpoint['DamageSourceTags'],
                unknown_fields=self._get_unknown_fields(weakpoint, Weakpoint.get_unknown_fields())
            ))
        
        # TODO: Implement a class to hold the Loot information
        loot = []
        items = [] if 'Items' not in components['LootComponent'] else components['LootComponent']['Items']
        for item in items:
            loot.append({
                'item': {
                    'key': item['ItemData']['RowName'],
                },
                'quantity': item['Count'],
                'drop_chance': item['DropChance'],
                'ignore_luck': item['bIgnoreLuck'],
                'spawn_type': item['SpawnType'],
                'location_type': item['LocationType'],
                'stealable': item['bStealable'],
                'ngplus_tier': item['RequiredNewGamePlusTier']
            })

        try:
            max_stun = components['ReactionComponent']['MaxStunValue']
            stun_decay = components['ReactionComponent']['StunDecayRate']
            stun_duration = components['ReactionComponent']['StunDuration']
            stun_cooldown = components['ReactionComponent']['StunCooldown']
        except KeyError:
            max_stun = 0
            stun_decay = 0
            stun_duration = 0
            stun_cooldown = 0

        if BestiaryCrawler.status_effects_table is None:
            with open(self._build_real_path('/Game/Blueprints/Attacks/Table_StatusEffects.json'), 'r') as file:
                BestiaryCrawler.status_effects_table = json.load(file)[0]['Rows']

        status_effects = []
        default_status_effects = []
        if 'DefaultStatusEffects' in components['StatusEffectComponent']:
            default_status_effects = components['StatusEffectComponent']['DefaultStatusEffects']
        for status_effect_obj in default_status_effects:
            status_effect_json = BestiaryCrawler.status_effects_table[status_effect_obj['RowName']]

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
            
            status_effects.append(StatusEffect(
                key_name=status_effect_obj['RowName'],
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
            ))

        immunity_tags = []
        if 'ImmunityTags' in components['StatusEffectComponent']:
            immunity_tags = components['StatusEffectComponent']['ImmunityTags']


        team = creature_info.team
        if 'TeamDataTable' in components['TeamComponent']:
            team = components['TeamComponent']['TeamDataTable']['RowName']

        unknown_fields = self._get_unknown_fields(creature_bp, CreatureInfo.get_unknown_fields())

        creature_info = CreatureInfo(
            health=creature_info.health,
            base_damage_reduction=creature_info.base_damage_reduction,
            weakpoints=weakpoints,
            loot=loot,
            max_stun=max_stun,
            stun_decay=stun_decay,
            stun_duration=stun_duration,
            stun_cooldown=stun_cooldown,
            status_effects=status_effects,
            immunity_tags=immunity_tags,
            team=team,
            unknown_fields=unknown_fields
        )

        try:
            table_id = 9
            if 'StringTableID' in components['DefaultComponent']['CharacterName']:
                table_id = components['DefaultComponent']['CharacterName']['StringTableID']

            name = DisplayName(
                table_id=table_id,
                string_id=components['DefaultComponent']['CharacterName']['StringID'],
                string_table_name=''
            )
        except:
            pass

        return (name, creature_info)

    def _get_character_data(self, asset_path_name: str) -> dict[str, Any]:
        creature_bp_path = self._build_real_path(asset_path_name)
        creature_bp = None
        if not os.path.exists(creature_bp_path):
            return None
        with open(creature_bp_path, 'r') as file:
            creature_bp = json.load(file)
        if creature_bp is None:
            return None

        main_component = None
        template_component = None
        for component in creature_bp:
            if component['Name'].startswith('Default__'):
                main_component = component['Properties']
            if 'Template' in component:
                template_component = component['Template']

        if main_component is None:
            return None
        
        if template_component is not None:
            # print(f'Found template component: {template_component} for {asset_path_name}')
            character_data_datatable = self._get_character_data_table(template_component['ObjectPath'])
            if character_data_datatable is not None:
                main_component['CharacterData']['DataTable'] = character_data_datatable

        if 'DataTable' not in main_component['CharacterData']:
            return None

        return self._parse_character_data(main_component['CharacterData'])

    def _get_character_data_table(self, asset_path_name: str) -> dict[str, Any]:
        creature_bp_path = self._build_real_path(asset_path_name)
        creature_bp = None
        if not os.path.exists(creature_bp_path):
            return None
        with open(creature_bp_path, 'r') as file:
            creature_bp = json.load(file)
        if creature_bp is None:
            return None
        
        main_component = None
        template_component = None
        for component in creature_bp:
            if component['Name'].startswith('Default__'):
                main_component = component['Properties']
            if 'Template' in component:
                template_component = component['Template']

        if template_component is not None:
            character_data_datatable = self._get_character_data_table(template_component['ObjectPath'])
            if character_data_datatable is not None:
                return character_data_datatable

        if main_component is None or 'DataTable' not in main_component['CharacterData']:
            return None
        
        return main_component['CharacterData']['DataTable']

    def _parse_character_data(self, datatable: dict[str, Any]) -> CharacterData:
        key_name = datatable['RowName']
        object_path = self._get_object_path(datatable['DataTable'])

        if BestiaryCrawler.character_data_table is None and 'Table_CharacterData' in object_path.name:
            BestiaryCrawler.character_data_table = json.loads(object_path.read_text(encoding='utf-8'))[0]['Rows']
        elif 'Table_CharacterData' not in object_path.name:
            raise ValueError('The provided object path is not an character data table.')
        
        character_data_json = BestiaryCrawler.character_data_table[key_name]

        icon = self._get_media_path(character_data_json['Icon'])
        hud_icon = self._get_media_path(character_data_json['HudIcon'])

        character_name = self._get_display_name(character_data_json['CharacterName'])

        active_pet_passive_effects = []
        for active_pet_passive_effect_json in character_data_json['ActivePetPassiveEffects']:
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
        for taming_food_json in character_data_json['TamingFood']:
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
            row_name=character_data_json['BestiaryItem']['RowName'],
            data_table=UEObject(
                name=character_data_json['BestiaryItem']['DataTable']['ObjectName'],
                path=character_data_json['BestiaryItem']['DataTable']['ObjectPath']
            )
        )

        unknown_fields = self._get_unknown_fields(character_data_json, CharacterData.get_unknown_fields())

        character_data = CharacterData(
            name=key_name,
            icon=icon,
            hud_icon=hud_icon,
            character_name=character_name,
            character_tags=character_data_json['CharacterTags'],
            tameable=character_data_json['bTameable'],
            taming_food=taming_food,
            active_pet_passive_effects=active_pet_passive_effects,
            bestiary_item=bestiary_item,
            actor_path=character_data_json['PlacementData']['Actor']['AssetPathName'],
            unknown_fields=unknown_fields
        )

        return character_data

    def _get_crawled_data(self, key: str, value: dict, unknown_fields: dict[str, Any]) -> Creature:
        if key == 'SpiderOrb':
            print('Found SpiderOrb')
        name, creature_info = self._parse_creature_info(value['Creature']['AssetPathName'])

        character_data = self._get_character_data(value['Creature']['AssetPathName'])

        creature = Creature(
            key_name=key,
            name=name,
            asset_path_name=value['Creature']['AssetPathName'],
            weakpoint_tags=value['WeakpointTags'],
            info=creature_info,
            character_data=character_data,
            rare_unlock_item=self._parse_item(value['RareUnlockItemData']),
            rare_drop_chance=value['RareDropChance'],
            unknown_fields=unknown_fields
        )
        return creature