from models import DamageData
from models.status_effect import StatusEffect

class Attack:
    """
    Represents the data related to the attack of a Tool or Weapon.
    #### Parameters
    - `key_name`: `str`
        - The key name of the attack.
    - `main_damage_data`: `DamageData`
        - The main damage data of the attack.
    - `secondary_damage_data`: `list[DamageData]`
        - The secondary damage data of the attack.
    - `charged_damage_data`: `DamageData`
        - The charged damage data of the attack.
    - `charge_time`: `float`
        - The charge time of the attack.
    - `range`: `float`
        - The range of the attack.
    - `stamina_cost`: `float`
        - The stamina cost of the attack.
    - `ranged_attack`: `bool`
        - A flag to determine if the attack is ranged.
    - `throw_attack`: `bool`
        - A flag to determine if the attack is a throw attack.
    - `tags`: `list[str]`
        - The tags of the attack.
    - `status_effects`: `list[StatusEffect]`
        - The status effects of the attack.
    - `status_effect_apply_type`: `str`
        - Tag that determines how the status effects are applied.
    - `unknown_fields`: `dict`
        - The unknown fields of the attack.
    """
    def __init__(self, key_name: str, main_damage_data: DamageData, secondary_damage_data: list[DamageData], charged_damage_data: DamageData, charge_time: float, range: float, stamina_cost: float, ranged_attack: bool, throw_attack: bool, tags: list[str], status_effects: list[StatusEffect], status_effect_apply_type: str, unknown_fields: dict):
        self.key_name = key_name
        self.main_damage_data = main_damage_data
        self.secondary_damage_data = secondary_damage_data
        self.charged_damage_data = charged_damage_data
        self.charge_time = charge_time
        self.range = range
        self.stamina_cost = stamina_cost
        self.ranged_attack = ranged_attack
        self.throw_attack = throw_attack
        self.tags = tags
        self.status_effects = status_effects
        self.status_effect_apply_type = status_effect_apply_type
        self.unknown_fields = unknown_fields

    def to_dict(self) -> dict:
        """
        This method is responsible for converting the Attack data to a dictionary.
        #### Returns
        - `dict` : The converted Attacks data.
        """
        return {
            'key_name': self.key_name,
            'main_damage_data': self.main_damage_data.to_dict(),
            'secondary_damage_data': [damage_data.to_dict() for damage_data in self.secondary_damage_data],
            'charged_damage_data': self.charged_damage_data.to_dict(),
            'charge_time': self.charge_time,
            'range': self.range,
            'stamina_cost': self.stamina_cost,
            'ranged_attack': self.ranged_attack,
            'throw_attack': self.throw_attack,
            'tags': self.tags,
            'status_effects': [status_effect.to_dict() for status_effect in self.status_effects],
            'status_effect_apply_type': self.status_effect_apply_type,
            'unknown_fields': self.unknown_fields
        }
    
    def from_dict(data: dict) -> 'Attack':
        """
        This method is responsible for converting the dictionary to a Attack object.
        #### Parameters
        - `data`: `dict`
            - The dictionary to convert.
        #### Returns
        - `Attack` : The converted Attack object.
        """
        return Attack(
            data['key_name'],
            DamageData.from_dict(data['main_damage_data']),
            [DamageData.from_dict(damage_data) for damage_data in data['secondary_damage_data']],
            DamageData.from_dict(data['charged_damage_data']),
            data['charge_time'],
            data['range'],
            data['stamina_cost'],
            data['ranged_attack'],
            data['throw_attack'],
            data['tags'],
            [StatusEffect.from_dict(status_effect) for status_effect in data['status_effects']],
            data['status_effect_apply_type'],
            data['unknown_fields']
        )
    
    @staticmethod
    def get_unknown_fields() -> list[str]:
        """
        This method is responsible for getting the unknown fields of the Attack data.
        #### Returns
        - `list` : The unknown fields of the Attacks data.
        """
        return [
            'bChargeHoldChainsAttack', 'ChargedRange',               'OverrideTraceRadius',            'ConeAngle',                    
            'ConeBaseDirectionAngle',  'ConeBaseDirectionSymetry',   'bIgnoreVisibilityCheck',         'Duration',                     
            'SoundIntensity',          'SoundRange',                 'HitResolutionType',              'bIsHostile',                   
            'bFriendlyFire',           'bIgnoreOwner',               'bDropHauledItems',               'FireAttackOnFullCharge',       
            'bEndAttackOnHit',         'bHitFrameLoops',             'bIsJumpAttack',                  'bChargeHitOnlyOnCharacter',    
            'bSelfDestruct',           'bDestroyTarget',             'bIgnoreItemDamageTypeModifiers', 'bCanTriggerOnTriggeredAttacks',
            'AIParams',                'bConsumeStaminaOnHitFrame',  'ProjectileClass',                'ChargedProjectileClass',       
            'SummonClass',             'Hazards',                    'bBurrowAttack',                  'bBurrowOnEndAttack',           
            'bUnBurrowOnEndAttack',    'bForceSwapFoliageOnHit',     'ProjectileAttackTime',           'OriginSocket',                 
            'LaunchOrientationOffset', 'LaunchOrientationDeviation', 'bUseLegacyOffset',               'MinThrowIntensity',            
            'MaxThrowIntensity',       'bSummonBossMobsPhase',       #'StatusEffects',                  'StatusEffectApplyType',        
            'AttackAnim',              'WeaponAnim',                 'DeflectAnim',                    'DeathNotification',            
            'StartVFX',                'ChargingVFX',                'LaunchVFX',                      'AttackVFX',                    
            'AttackChargedVFX',        'SoundFX',                    'ChargingSFX',                    'LaunchSFX',                    
            'HitEffect',               'bActivateWeaponEffects',    
        ]