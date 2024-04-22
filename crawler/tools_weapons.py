import json 

from .base_crawler import BaseCrawler
from pathlib import Path
from typing import Any
from models import PlayerUpgrade, DisplayName, ToolWeapon, BlockActionInfo, StatusEffect, ItemEffectsInfo
from models import RecipeComponent

class ToolsWeaponsCrawler(BaseCrawler):
    """
    This class is responsible for crawling the tools and weapons data from the game.
    """
    status_effects_table = None
    items_table = None
    attacks_table = None

    def __init__(self, hide_unknown_fields: bool = False):
        super().__init__(
            name='tools_weapons',
            json_path=Path('Maine/Content/Blueprints/Items/ItemTables/Table_Items_Tools.json'),
            hide_unknown_fields=hide_unknown_fields
        )
        self.unknown_field_list = ToolWeapon.get_unknown_fields()
    
    def dispose(self) -> None:
        ToolsWeaponsCrawler.status_effects_table = None
        ToolsWeaponsCrawler.items_table = None
        ToolsWeaponsCrawler.attacks_table = None

    def _parse_status_effect(self, datatable: dict[str, Any]) -> StatusEffect:
        # TODO: Move this to a separate crawler
        key_name = datatable['RowName']
        object_path = self._get_object_path(datatable['DataTable'])

        if ToolsWeaponsCrawler.status_effects_table is None and 'Table_StatusEffects' in object_path.name:
            ToolsWeaponsCrawler.status_effects_table = json.loads(object_path.read_text(encoding='utf-8'))[0]['Rows']
        elif 'Table_StatusEffects' not in object_path.name:
            raise ValueError('The provided object path is not a status effects table.')
        
        status_effect_json = ToolsWeaponsCrawler.status_effects_table[key_name]

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

        unknown_fields = []
        if self.hide_unknown_fields is False:
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
            unknown_fields=unknown_fields
        )

    def _parse_recipe_component(self, component: dict[str, Any]) -> RecipeComponent:
        # TODO: Move this to a separate crawler
        item_key = component['Item']['RowName']
        quantity = component['ItemCount']
        datatable_path = self._get_object_path(component['Item']['DataTable'])

        if ToolsWeaponsCrawler.items_table is None and 'Table_AllItems' in datatable_path.name:
            ToolsWeaponsCrawler.items_table = json.loads(datatable_path.read_text(encoding='utf-8'))[0]['Rows']
        elif 'Table_AllItems' not in datatable_path.name:
            raise ValueError('The provided object path is not an items table.')
        
        item_json = ToolsWeaponsCrawler.items_table[item_key]

        display_name = DisplayName(
            table_id=item_json['LocalizedDisplayName']['StringTableID'],
            string_id=item_json['LocalizedDisplayName']['StringID'],
            string_table_name=item_json['LocalizedDisplayName']['StringTableName']
        )
        description = DisplayName(
            table_id=item_json['LocalizedDescription']['StringTableID'],
            string_id=item_json['LocalizedDescription']['StringID'],
            string_table_name=item_json['LocalizedDescription']['StringTableName']
        )
        icon_path = self._get_media_path(item_json['Icon'])
        icon_modifier_path = self._get_media_path(item_json['ModIcon'])

        return RecipeComponent(
            item_key=item_key,
            quantity=quantity,
            display_name=display_name,
            description=description,
            icon_path=icon_path,
            icon_modifier_path=icon_modifier_path
        )

    def _get_crawled_data(self, key: str, value: dict, unknown_fields: dict[str, Any]) -> PlayerUpgrade:
        display_name = DisplayName(
            table_id=value['LocalizedDisplayName']['StringTableID'],
            string_id=value['LocalizedDisplayName']['StringID'],
            string_table_name=value['LocalizedDisplayName']['StringTableName']
        )
        keywords = []
        for keyword in value['SearchableKeywords']:
            keywords.append(DisplayName(
                table_id=keyword['StringTableID'],
                string_id=keyword['StringID'],
                string_table_name=keyword['StringTableName']
            ))

        description = DisplayName(
            table_id=value['LocalizedDescription']['StringTableID'],
            string_id=value['LocalizedDescription']['StringID'],
            string_table_name=value['LocalizedDescription']['StringTableName']
        )

        icon_path = self._get_media_path(value['Icon'])
        icon_modifier_path = self._get_media_path(value['ModIcon'])

        block_action_info = BlockActionInfo(
            can_block=value['bCanBlock'],
            cannot_block_while_attacking=value['bCannotBlockWhileAttacking'],
            block_damage_reduction=value['BlockDamageMultiplier'],
            block_stamina_cost=value['BlockStaminaCost'],
            block_stamina_regen_multiplier=value['BlockStaminaRegenMultiplier']
        )

        main_status_effects = []
        for status_effect in value['EquippableData']['StatusEffects']:
            main_status_effects.append(self._parse_status_effect(status_effect))

        hidden_status_effects = []
        for status_effect in value['EquippableData']['HiddenStatusEffects']:
            hidden_status_effects.append(self._parse_status_effect(status_effect))

        item_effects_info = ItemEffectsInfo(
            main_status_effects=main_status_effects,
            hidden_status_effects=hidden_status_effects,
            random_effect_type=value['EquippableData']['RandomEffectType']
        )

        recipe = []
        for component in value['EquippableData']['RepairRecipe']:
            recipe.append(self._parse_recipe_component(component))

        tool_weapon = ToolWeapon(
            key_name=key,
            display_name=display_name,
            keywords=keywords,
            description=description,
            icon_path=icon_path,
            icon_modifier_path=icon_modifier_path,
            item_type=value['ItemType'],
            new_game_plus=value['bNewGamePlus'],
            duplicate_cost=value['DuplicateBaseCost'],
            recycle_reward=value['RecycleReward'],
            rarity_tag=value['RarityTag']['TagName'],
            stack_size_tag=value['StackSizeTag']['TagName'],
            tier=value['Tier'],
            can_enhance=value['bCanEnhance'],
            enhancement_tags=value['ValidEnhancementTags'],
            slot=value['Slot'],
            two_handed=value['TwoHanded'],
            block_action_info=block_action_info,
            durability=value['EquippableData']['Durability'],
            item_effects_info=item_effects_info,
            repair_recipe=recipe,
            main_attack_combo=value['AttackComboData']['Attacks'],
            main_scaling_type=value['AttackComboData']['ScalingType']['TagName'],
            alternate_attack_combo=value['AlternateAttackComboData']['Attacks'],
            alternate_scaling_type=value['AlternateAttackComboData']['ScalingType']['TagName'],
            swimming_attack_combo=value['SwimmingAttackComboData']['Attacks'],
            swimming_scaling_type=value['SwimmingAttackComboData']['ScalingType']['TagName'],
            ammo_attack_reference=value['AmmoAttackReference'],
            ammo_attack_data=value['AmmoAttackData'],
            consumable_data=value['ConsumableData'],
            tags=value['Tags'],
            world_actor_path=value['WorldActor']['AssetPathName'],
            equipped_actor_path=value['PlayerEquippedActor']['AssetPathName'],
            unknown_fields=unknown_fields
        )

        return tool_weapon