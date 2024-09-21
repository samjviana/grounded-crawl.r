import json
import os
import uuid

from pathlib import Path
from typing import Any

from models import HarvestNode, DisplayName, UEObject, HarvestNodeInfo
from .base_crawler import BaseCrawler

class HarvestNodesCrawler(BaseCrawler):
    """
    This class is responsible for crawling the harvest nodes data from the game.
    """
    def __init__(self, hide_unknown_fields: bool = False):
        super().__init__(
            name='harvest_nodes',
            json_path=Path('Maine/Content/Blueprints/DataTables/Table_AllHarvestNodes.json'),
            hide_unknown_fields=hide_unknown_fields
        )
        self.unknown_field_list = [
            'SearchableKeywords',
            'ModelViewerMeshOverride',
            'ModelViewerMaterialsOverride',
            'PlacementData>bPermitForUGC',
            'PlacementData>bHasUGCInteractions',
            'PlacementData>ActorFlipped',
            'PlacementData>ActorWall',
            'PlacementData>ActorCeiling',
            'PlacementData>SlotType',
            'PlacementData>bUseAlternateSlotType',
            'PlacementData>AlternateSlotType',
            'PlacementData>EmbedMode',
            'PlacementData>bPlaceAtPlayerRotation',
            'PlacementData>bPermitExtraRotationAxes',
            'PlacementData>bPermitRescaling',
            'PlacementData>bAllowPlaceInWater',
            'PlacementData>RandomRotateIncrement',
            'PlacementData>RotationOffset',
            'PlacementData>BuoyantPlacement',
            'PlacementData>TerrainConform',
            'PlacementData>MaxSlope',
            'PlacementData>OverridePlacementDistance',
            'PlacementData>PlacementOriginOffset',
            'PlacementData>AttachedPlacementOffset',
            'PlacementData>bDoOverrideAllowedWallNormal',
            'PlacementData>OverrideAllowedWallNormal',
            'PlacementData>DefaultScale'
        ]

    # TODO: Figure out a more readable way to set a field "recursively-safe" without using try-except (maybe a function?)
    def _parse_harvest_node_info(self, asset_path_name: str) -> HarvestNodeInfo:
        harvest_node_bp_path = self._build_real_path(asset_path_name)
        harvest_node_bp = None
        if not os.path.exists(harvest_node_bp_path):
            return None
        with open(harvest_node_bp_path, 'r') as file:
            harvest_node_bp = json.load(file)
        if harvest_node_bp is None:
            return None
        
        components = {
            'DefaultComponent': {},
            'HealthComponent': {},
            'LootComponent': {},
        }
        for component in harvest_node_bp:
            if component['Name'].startswith('Default__'):
                components['DefaultComponent'] = component['Properties']
                if 'Template' in component:
                    components['DefaultComponentTemplate'] = component['Template']
                continue
            if component['Type'] not in components:
                continue

            components[component['Type']] = {}
            if 'Properties' in component:
                components[component['Type']] = component['Properties']

            if 'Template' in component:
                components[f'{component["Type"]}Template'] = component['Template']

        harvest_node_info = HarvestNodeInfo(
            health=0,
            required_damage_type_flags=0,
            tags=[],
            loot=[]
        )
        for component in components:
            if component.endswith('Template'):
                template = self._parse_harvest_node_info(components[component]['ObjectPath'])

                if component.startswith('HealthComponent'):
                    harvest_node_info.required_damage_type_flags = template.required_damage_type_flags
                if component.startswith('DefaultComponent'):
                    harvest_node_info.tags = template.tags

        try:
            harvest_node_info.required_damage_type_flags = components['HealthComponent']['RequiredDamageTypeFlags']
        except:
            pass

        try:
            harvest_node_info.health = components['HealthComponent']['MaxHealth']
        except:
            pass

        try:
            harvest_node_info.tags = components['DefaultComponent']['HarvestNodeTags']
        except:
            pass

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

        harvest_node_info = HarvestNodeInfo(
            health=harvest_node_info.health,
            required_damage_type_flags=harvest_node_info.required_damage_type_flags,
            tags=harvest_node_info.tags,
            loot=loot
        )

        return harvest_node_info

    def _get_crawled_data(self, key: str, value: dict, unknown_fields: dict[str, Any]) -> HarvestNode:
        display_name = DisplayName(
            table_id=value['DisplayName']['StringTableID'],
            string_id=value['DisplayName']['StringID'],
            string_table_name=value['DisplayName']['StringTableName']
        )
        if display_name.string_table_name == 'None':
            display_name.string_table_name = DisplayName.string_table_names[display_name.table_id]

        icon_path = self._get_media_path(value['Icon'])

        harvest_node_info = self._parse_harvest_node_info(value['PlacementData']['Actor']['AssetPathName'])

        harvest_node = HarvestNode(
            name=key,
            display_name=display_name,
            icon=icon_path,
            asset_path_name=value['PlacementData']['Actor']['AssetPathName'],
            month_to_unlock=value['PlacementData']['MonthToUnlockForUGC'],
            subcategory_tag=value['PlacementData']['UGCSubcategoryTag']['TagName'],
            info=harvest_node_info,
            unknown_fields=unknown_fields,
        )

        return harvest_node