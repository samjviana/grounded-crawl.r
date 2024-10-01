import json 

from .base_crawler import BaseCrawler
from pathlib import Path
from typing import Any
from models import PlayerUpgrade, DisplayName, ToolWeapon, BlockActionInfo, StatusEffect, ItemEffectsInfo
from models import RecipeComponent, Attack, DamageData, AttacksInfo

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

        global_combat_data_path = self.root_path / 'json_data/Maine/Content/Blueprints/Global/GlobalCombatData.json'
        global_combat_data = json.loads(global_combat_data_path.read_text(encoding='utf-8'))[0]['Properties']
        self.combo_scaling_types = {}
        for scaling_type in global_combat_data['ComboScalingTypes']:
            tag_name = scaling_type['Tag']['TagName']
            self.combo_scaling_types[tag_name] = scaling_type['ScalingValue']
    
    def dispose(self) -> None:
        ToolsWeaponsCrawler.status_effects_table = None
        ToolsWeaponsCrawler.items_table = None
        ToolsWeaponsCrawler.attacks_table = None

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

    def _parse_attack(self, attack: dict[str, Any]) -> Attack:
        # TODO: Move this to a separate crawler
        key_name = attack['RowName']
        datatable_path = self._get_object_path(attack['DataTable'])
        if 'ItemAttacks' in datatable_path.name:
            datatable_path = datatable_path.parent / 'AllAttacks.json'

        if ToolsWeaponsCrawler.attacks_table is None and 'AllAttacks' in datatable_path.name:
            ToolsWeaponsCrawler.attacks_table = json.loads(datatable_path.read_text(encoding='utf-8'))[0]['Rows']
        elif 'AllAttacks' not in datatable_path.name and 'ItemAttacks' not in datatable_path.name:
            raise ValueError('The provided object path is not an attacks table.')
        
        attack_json = ToolsWeaponsCrawler.attacks_table[key_name]

        unknown_fields = self._get_unknown_fields(attack_json['DamageData'], DamageData.get_unknown_fields())
        damage_type = attack_json['DamageData']['DamageType']
        if damage_type is not None and 'ObjectPath' in damage_type:
            damage_type = damage_type['ObjectPath'].split('/')[-1].split('.')[0]

        main_damage_data = DamageData(
            damage=attack_json['DamageData']['Damage'],
            damage_type=damage_type,
            stun_damage=attack_json['DamageData']['HitStun'],
            pushback_damage=attack_json['DamageData']['Pushback'],
            unknown_fields=unknown_fields
        )
        
        secondary_damage_data = []
        for secondary_damage in attack_json['DamageDataSecondary']:
            unknown_fields = self._get_unknown_fields(secondary_damage, DamageData.get_unknown_fields())
            damage_type = secondary_damage['DamageType']
            if damage_type is not None and 'ObjectPath' in damage_type:
                damage_type = damage_type['ObjectPath'].split('/')[-1].split('.')[0]

            secondary_damage_data.append(DamageData(
                damage=secondary_damage['Damage'],
                damage_type=damage_type,
                stun_damage=secondary_damage['HitStun'],
                pushback_damage=secondary_damage['Pushback'],
                unknown_fields=unknown_fields
            ))

        unknown_fields = self._get_unknown_fields(attack_json['ChargedDamageData'], DamageData.get_unknown_fields())
        damage_type = attack_json['ChargedDamageData']['DamageType']
        if damage_type is not None and 'ObjectPath' in damage_type:
            damage_type = damage_type['ObjectPath'].split('/')[-1].split('.')[0]

        charged_damage_data = DamageData(
            damage=attack_json['ChargedDamageData']['Damage'],
            damage_type=damage_type,
            stun_damage=attack_json['ChargedDamageData']['HitStun'],
            pushback_damage=attack_json['ChargedDamageData']['Pushback'],
            unknown_fields=unknown_fields
        )

        status_effects = []
        for status_effect in attack_json['StatusEffects']:
            status_effects.append(self._parse_status_effect(status_effect))

        unknown_fields = self._get_unknown_fields(attack_json, Attack.get_unknown_fields())

        return Attack(
            key_name=key_name,
            main_damage_data=main_damage_data,
            secondary_damage_data=secondary_damage_data,
            charged_damage_data=charged_damage_data,
            charge_time=attack_json['ChargeTime'],
            range=attack_json['Range'],
            stamina_cost=attack_json['StaminaCost'],
            ranged_attack=attack_json['bRangedAttack'],
            throw_attack=attack_json['bThrowAttack'],
            tags=attack_json['Tags'],
            status_effects=status_effects,
            status_effect_apply_type=attack_json['StatusEffectApplyType'],
            unknown_fields=unknown_fields
        )

    def _get_scaling_values(self, scaling_type: str, attack_count: int) -> list[float]:
        if scaling_type == 'None':
            return [1.0] * attack_count

        return self.combo_scaling_types[scaling_type]

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

        main_combo = []
        for attack in value['AttackComboData']['Attacks']:
            main_combo.append(self._parse_attack(attack))

        alternate_combo = []
        for attack in value['AlternateAttackComboData']['Attacks']:
            alternate_combo.append(self._parse_attack(attack))

        swimming_combo = []
        for attack in value['SwimmingAttackComboData']['Attacks']:
            swimming_combo.append(self._parse_attack(attack))

        melee_attacks_info = AttacksInfo(
            main_combo=main_combo,
            main_scaling=self._get_scaling_values(value['AttackComboData']['ScalingType']['TagName'], len(main_combo)),
            alternate_combo=alternate_combo,
            alternate_scaling=self._get_scaling_values(value['AlternateAttackComboData']['ScalingType']['TagName'], len(alternate_combo)),
            swimming_combo=swimming_combo,
            swimming_scaling=self._get_scaling_values(value['SwimmingAttackComboData']['ScalingType']['TagName'], len(swimming_combo))
        )

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
            melee_attacks_info=melee_attacks_info,
            ammo_attack_reference=value['AmmoAttackReference'],
            ammo_attack_data=value['AmmoAttackData'],
            consumable_data=value['ConsumableData'],
            tags=value['Tags'],
            world_actor_path=value['WorldActor']['AssetPathName'],
            equipped_actor_path=value['PlayerEquippedActor']['AssetPathName'],
            unknown_fields=unknown_fields
        )

        return tool_weapon