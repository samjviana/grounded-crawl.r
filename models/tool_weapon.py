from models import DisplayName, BlockActionInfo, ItemEffectsInfo, RecipeComponent, AttacksInfo
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
    - `melee_attacks_info`: `AttacksInfo`
        - The melee attacks information of the tool or weapon.
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
                 repair_recipe: list[RecipeComponent], melee_attacks_info: AttacksInfo, ammo_attack_reference: str, ammo_attack_data: list, consumable_data: list, tags: list[str],
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
        self.melee_attacks_info = melee_attacks_info
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
            'display_name': self.display_name.to_dict(),
            'keywords': [keyword.to_dict() for keyword in self.keywords],
            'description': self.description.to_dict(),
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
            'melee_attacks_info': self.melee_attacks_info.to_dict(),
            'ammo_attack_reference': self.ammo_attack_reference,
            'ammo_attack_data': self.ammo_attack_data,
            'consumable_data': self.consumable_data,
            'tags': self.tags,
            'world_actor_path': self.world_actor_path,
            'equipped_actor_path': self.equipped_actor_path,
            'unknown_fields': self.unknown_fields
        }

    def from_dict(data: dict) -> 'ToolWeapon':
        """
        This method is responsible for creating a ToolWeapon object from a dictionary.
        #### Parameters
        - `data` : `dict`
            - The dictionary containing the ToolWeapon data.
        #### Returns
        - `ToolWeapon` : The ToolWeapon object created from the dictionary.
        """
        return ToolWeapon(
            data['key_name'],
            DisplayName.from_dict(data['display_name']),
            [DisplayName.from_dict(keyword) for keyword in data['keywords']],
            DisplayName.from_dict(data['description']),
            Path(data['icon_path']),
            Path(data['icon_modifier_path']),
            data['item_type'],
            data['new_game_plus'],
            data['duplicate_cost'],
            data['recycle_reward'],
            data['rarity_tag'],
            data['stack_size_tag'],
            data['tier'],
            data['can_enhance'],
            data['enhancement_tags'],
            data['slot'],
            data['two_handed'],
            BlockActionInfo.from_dict(data['block_action_info']),
            data['durability'],
            ItemEffectsInfo.from_dict(data['item_effects_info']),
            [RecipeComponent.from_dict(recipe_component) for recipe_component in data['repair_recipe']],
            AttacksInfo.from_dict(data['melee_attacks_info']),
            data['ammo_attack_reference'],
            data['ammo_attack_data'],
            data['consumable_data'],
            data['tags'],
            data['world_actor_path'],
            data['equipped_actor_path'],
            data['unknown_fields']
        )

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