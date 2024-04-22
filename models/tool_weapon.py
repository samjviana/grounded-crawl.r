from models import DisplayName, BlockActionInfo, ItemEffectsInfo, RecipeComponent
from pathlib import Path

class ToolWeapon:
    # TODO: Wrap the Equippable information in a class
    # TODO: Wrap the AttackCombo information in a class
    """
    Represents a Tool or Weapon object in the game.
    #### Parameters
    - `key_name` : `str`
        - The key name of the tool or weapon in the game files.
    - `display_name` : `DisplayName`
        - The display name of the tool or weapon.
    - `keywords` : `list[DisplayName]`
        - The keywords of the tool or weapon.
    - `description` : `DisplayName`
        - The description of the tool or weapon.
    - `icon_path` : `Path`
        - The icon path of the tool or weapon.
    - `icon_modifier_path` : `Path`
        - The icon modifier path of the tool or weapon.
    - `item_type` : `str`
        - The item type of the tool or weapon.
    - `new_game_plus` : `bool`
        - Whether the tool or weapon is available in new game plus.
    - `duplicate_cost`: `int`
        - The duplicate cost of the tool or weapon.
    - `recycle_reward` : `int`
        - The recycle reward of the tool or weapon.
    - `rarity_tag` : `str`
        - The rarity tag of the tool or weapon.
    - `stack_size_tag` : `str`
        - The stack size tag of the tool or weapon.
    - `tier`: `int`
        - The tier of the tool or weapon.
    - `can_enhance` : `bool`
        - Whether the tool or weapon can be enhanced.
    - `enhancement_tags` : `list[str]`
        - The enhancement tags of the tool or weapon.
    - `slot`: `str`
        - The slot where the tool or weapon can be equipped.
    - `two_handed` : `bool`
        - Whether the tool or weapon is two handed.
    - `block_action_info`: `BlockActionInfo`
        - Information related to blocking with the tool or weapon.
    - `durability` : `float`
        - The durability of the tool or weapon.
    - `item_effects_info` : `ItemEffectsInfo`
        - The item effects information of the tool or weapon.
    - `repair_recipe` : list[RecipeComponent]
        - The repair recipe of the tool or weapon
    - `main_attack_combo` : `list[str]`
        - The main attack combo of the tool or weapon.
    - `main_scaling_type` : `str`
        - The scaling type of the main attack of the tool or weapon.
    - `alternate_attack_combo` : `list[str]`
        - The alternate attack combo of the tool or weapon.
    - `alternate_scaling_type` : `str`
        - The scaling stat of the alternate attack of the tool or weapon.
    - `swimming_attack_combo` : `list[str]`
        - The underwater attack combo of the tool or weapon.
    - `swimming_scaling_type` : `float`
        - The scaling stat of the underwater attack of the tool or weapon.
    - `ammo_attack_reference` : `str`
        - The ammo attack reference of the tool or weapon.
    - `ammo_attack_data` : `list`
        - The ammo attack data of the tool or weapon.
    - `consumable_data` : `list`
        - The consumable data of the tool or weapon.
    - `tags` : `list[str]`
        - The tags of the tool or weapon.
    - `world_actor_path` : `str`
        - The world actor path of the tool or weapon.
    - `equipped_actor_path` : `str`
        - The equipped actor path of the tool or weapon.
    - `unknown_fields` : `dict`
        - The unknown fields of the tool or weapon.
    """
    def __init__(self, key_name: str, display_name: DisplayName, keywords: list[DisplayName], description: DisplayName, icon_path: Path, icon_modifier_path: Path, item_type: str,
                 new_game_plus: bool, duplicate_cost: int, recycle_reward: int, rarity_tag: str, stack_size_tag: str, tier: int, can_enhance: bool, enhancement_tags: list[str],
                 slot: str, two_handed: bool, block_action_info: BlockActionInfo, durability: float, item_effects_info: ItemEffectsInfo,
                 repair_recipe: list[RecipeComponent], main_attack_combo: list[str], main_scaling_type: str, alternate_attack_combo: list[str], alternate_scaling_type: str,
                 swimming_attack_combo: list[str], swimming_scaling_type: float, ammo_attack_reference: str, ammo_attack_data: list, consumable_data: list, tags: list[str],
                 world_actor_path: str, equipped_actor_path: str, unknown_fields: dict):
        self.key_name = key_name
        self.display_name = display_name
        self.keywords = keywords
        self.description = description
        self.icon_path = icon_path
        self.icon_modifier_path = icon_modifier_path
        self.item_type = item_type
        self.new_game_plus = new_game_plus
        self.duplicate_cost = duplicate_cost
        self.recycle_reward = recycle_reward
        self.rarity_tag = rarity_tag
        self.stack_size_tag = stack_size_tag
        self.tier = tier
        self.can_enhance = can_enhance
        self.enhancement_tags = enhancement_tags
        self.slot = slot
        self.two_handed = two_handed
        self.block_action_info = block_action_info
        self.durability = durability
        self.item_effects_info = item_effects_info
        self.repair_recipe = repair_recipe
        self.main_attack_combo = main_attack_combo
        self.main_scaling_type = main_scaling_type
        self.alternate_attack_combo = alternate_attack_combo
        self.alternate_scaling_type = alternate_scaling_type
        self.swimming_attack_combo = swimming_attack_combo
        self.swimming_scaling_type = swimming_scaling_type
        self.ammo_attack_reference = ammo_attack_reference
        self.ammo_attack_data = ammo_attack_data
        self.consumable_data = consumable_data
        self.tags = tags
        self.world_actor_path = world_actor_path
        self.equipped_actor_path = equipped_actor_path
        self.unknown_fields = unknown_fields

    def to_dict(self) -> dict:
        """
        This method is responsible for converting the tool or weapon to a dictionary.
        #### Returns
        - `dict` : The converted tool or weapon.
        """
        return {
            'key_name': self.key_name,
            'display_name': self.display_name.get_string(),
            'keywords': [keyword.get_string() for keyword in self.keywords],
            'description': self.description.get_string(),
            'icon_path': self.icon_path.as_posix(),
            'icon_modifier_path': self.icon_modifier_path.as_posix(),
            'item_type': self.item_type,
            'new_game_plus': self.new_game_plus,
            'duplicate_cost': self.duplicate_cost,
            'recycle_reward': self.recycle_reward,
            'rarity_tag': self.rarity_tag,
            'stack_size_tag': self.stack_size_tag,
            'tier': self.tier,
            'can_enhance': self.can_enhance,
            'enhancement_tags': self.enhancement_tags,
            'slot': self.slot,
            'two_handed': self.two_handed,
            'block_action_info': self.block_action_info.to_dict(),
            'durability': self.durability,
            'item_effects_info': self.item_effects_info.to_dict(),
            'repair_recipe': [recipe_component.to_dict() for recipe_component in self.repair_recipe],
            'main_attack_combo': self.main_attack_combo,
            'main_scaling_type': self.main_scaling_type,
            'alternate_attack_combo': self.alternate_attack_combo,
            'alternate_scaling_type': self.alternate_scaling_type,
            'swimming_attack_combo': self.swimming_attack_combo,
            'swimming_scaling_type': self.swimming_scaling_type,
            'ammo_attack_reference': self.ammo_attack_reference,
            'ammo_attack_data': self.ammo_attack_data,
            'consumable_data': self.consumable_data,
            'tags': self.tags,
            'world_actor_path': self.world_actor_path,
            'equipped_actor_path': self.equipped_actor_path,
            'unknown_fields': self.unknown_fields
        }

    @staticmethod
    def get_unknown_fields() -> dict:
        # TODO: Move the ThrowData and PowerData to a separate class and add to the known fields 
        return [
            'Comment',                        'LocalizedWildcardDisplayName',                                 'DeduplicationItemRewardCount',            
            'KeyItemCategory',                'KeyItemSubCategory',                                           'BestiaryData',                            
            'OnKeyItemPickupVariable',        'OnKeyItemPickupVariableValue',                                 'OnKeyItemTurnedInVariable',               
            'OnKeyItemTurnedInVariableValue', 'KeyItemDateDay',                                               'KeyItemDateMonth',                        
            'KeyItemDateYear',                'NewGamePlusRewardItem',                                        'UnlockRecipes',                           
            'ResearchUnlockRecipes',          'NewResearchUnlockRecipes',                                     'TechTreeUnlocks',                         
            'DynamicMesh',                    'DynamicMaterials',                                             'bWorldMarker',                            
            'EnhancementTagUpdates',          'bHotDroppable',                                                'bTrashable',                              
            'bIsFlammable',                   'bWasCut',                                                      'bDecomposeOnLoad',                        
            'CustomEquippedActors',           'ArmorAttachData',                                              'FirstPersonArmorAttachData',              
            'Stance',                         'OverrideEquipSocket',                                          'MarkerType',                              
            'MarkerVariation',                'ItemSlotTintTag',                                              'bIsLightSource',                          
            'BlockAnim',                      'BlockItemAnim',                                                'BlockedEffectAnim',                       
            'BlockSound',                     'PerfectBlockSound',                                            'EquippableData>EquipAudio',               
            'EquippableData>EquipAnim',       'EquippableData>FlatDamageReduction',                           'EquippableData>PercentageDamageReduction',
            'EquippableData>HairType',        'EquippableData>DisablesThirdPersonShadowCastingInFirstPerson', 'AttackComboData>bLoop',                   
            'ConsumeChatterType',             'ConsumeChatterEvent',                                          'ConsumeAudio',                            
            'ConsumeAnimType',                'bHasConsumableCooldown',                                       'bBurgleQuestCanAnalyze',                  
            'BurgleQuestAnalyzeRewardLevel',  'OverrideTemplateConsumeAction',                                'HaulingData',                             
            'ProcessingOptions',              'ProcessingActorOverride',                                      'HatchTime',                               
            'HatchData',                      'GardenModifierType',                                           'GardenModifierValue',                     
            'SpoilData',                      'ThrowData',                                                    'PowerData',                               
            'InspectData',                    'GlidingData',                                                  'PlacementData',                           
            'bCanZipUp',                      'ResourceCategory',                                             'TelemetryTag',                            
            'WaveSpawnWeight',                'PickupAudio',                                                  'AudioData',                               
            'InteractAnimType',               'bDropsOnDeath',                                               
        ]