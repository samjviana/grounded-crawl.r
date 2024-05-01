class DamageData:
    """
    Wraps information about a damage data of a Tool or Weapon.
    #### Parameters
    - `damage`: `float`
        - The damage of the Tool or Weapon.
    - `damage_type`: `str`
        - The type of the damage.
    - `stun_damage`: `float`
        - The stun damage of the Tool or Weapon.
    - `pushback_damage`: `float`
        - The damage that pushes back the target.
    - `unknown_fields`: `dict`
        - The unknown fields of the damage data.
    """
    def __init__(self, damage: float, damage_type: str, stun_damage: float, pushback_damage: float, unknown_fields: dict):
        self.damage = damage
        self.damage_type = damage_type
        self.stun_damage = stun_damage
        self.pushback_damage = pushback_damage
        self.unknown_fields = unknown_fields

    def to_dict(self) -> dict:
        """
        This method is responsible for converting the Damage data to a dictionary.
        #### Returns
        - `dict` : The converted Damage data.
        """
        return {
            'damage': self.damage,
            'damage_type': self.damage_type,
            'stun_damage': self.stun_damage,
            'pushback_damage': self.pushback_damage,
            'unknown_fields': self.unknown_fields
        }
    
    @staticmethod
    def from_dict(data: dict) -> 'DamageData':
        """
        This method is responsible for converting the dictionary to a DamageData object.
        #### Parameters
        - `data`: `dict`
            - The dictionary to convert.
        #### Returns
        - `DamageData` : The converted DamageData object.
        """
        return DamageData(
            data['damage'],
            data['damage_type'],
            data['stun_damage'],
            data['pushback_damage'],
            data['unknown_fields']
        )

    @staticmethod
    def get_unknown_fields() -> list[str]:
        """
        This method is responsible for getting the unknown fields of the Damage data.
        #### Returns
        - `list` : The unknown fields of the Damage data.
        """
        return [
            'DamageEventType',
            'ForcedHitReaction',
            'DeathNotification'
        ]