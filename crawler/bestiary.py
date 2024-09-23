import json
import os

from pathlib import Path
from typing import Any

from models import Creature, CreatureInfo, StatusEffect, DisplayName
from .base_crawler import BaseCrawler

class BestiaryCrawler(BaseCrawler):
    """
    This class is responsible for crawling the bestiary data from the game.
    """
    status_effects_table = None

    def __init__(self, hide_unknown_fields: bool = False):
        super().__init__(
            name='bestiary',
            json_path=Path('Maine/Content/Blueprints/DataTables/Table_Bestiary.json'),
            hide_unknown_fields=hide_unknown_fields
        )
        self.unknown_field_list = [
            'Creature>SubPathString',
            'Stats',
            'RareUnlockItemData>DataTable',
        ]

    def dispose(self) -> None:
        self.status_effects_table = None

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
            health=0,
            loot=[],
            max_stun=0,
            stun_decay=0,
            stun_duration=0,
            stun_cooldown=0,
            status_effects=[],
            immunity_tags=[],
            team=0,
            unknown_fields={}
        )   
        name = None 
        for component in components:
            if component.endswith('Template'):
                templated_name, template = self._parse_creature_info(components[component]['ObjectPath'])

                if component.startswith('Default__'):
                    continue
                elif component.startswith('HealthComponent'):
                    creature_info.health = template.health
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
                unknown_fields=unknown_fields
            ))

        immunity_tags = []
        if 'ImmunityTags' in components['StatusEffectComponent']:
            immunity_tags = components['StatusEffectComponent']['ImmunityTags']


        team = None
        if 'TeamDataTable' in components['TeamComponent']:
            team = components['TeamComponent']['TeamDataTable']['RowName']

        unknown_fields = self._get_unknown_fields(creature_bp, CreatureInfo.get_unknown_fields())

        creature_info = CreatureInfo(
            health=creature_info.health,
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

    def _get_crawled_data(self, key: str, value: dict, unknown_fields: dict[str, Any]) -> Creature:
        name, creature_info = self._parse_creature_info(value['Creature']['AssetPathName'])

        creature = Creature(
            key_name=key,
            name=name,
            asset_path_name=value['Creature']['AssetPathName'],
            weakpoint_tags=value['WeakpointTags'],
            info=creature_info,
            rare_unlock_item_name=value['RareUnlockItemData']['RowName'],
            rare_drop_chance=value['RareDropChance'],
            unknown_fields=unknown_fields
        )
        return creature