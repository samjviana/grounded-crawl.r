class Weakpoint:
    """
    Class representing a weakpoint of a creature.
    #### Parameters
    - `key_name` : `str`
        - The key name of the item set.
    - `damage_multiplier` : `float`
        - The damage multiplier of the weakpoint.
    - `damage_sources` : `list[str]`
        - The damage sources that are effective against the weakpoint.
    - `unknown_fields` : `dict`
        - The unknown fields of the weakpoint.
    """
    def __init__(self, key_name: str, damage_multiplier: float, damage_sources: list[str], unknown_fields: dict):
        self.key_name = key_name    
        self.damage_multiplier = damage_multiplier
        self.damage_sources = damage_sources
        self.unknown_fields = unknown_fields

    def to_dict(self) -> dict:
        """
        This method is responsible for converting the weakpoint to a dictionary.
        #### Returns
        - `dict` : The converted weakpoint.
        """
        return {
            'key_name': self.key_name,
            'damage_multiplier': self.damage_multiplier,
            'damage_sources': self.damage_sources,
            'unknown_fields': self.unknown_fields
        }
    
    def from_dict(data: dict) -> 'Weakpoint':
        """
        This method is responsible for converting a dictionary to an weakpoint.
        #### Parameters
        - `data` : `dict`
            - The dictionary to convert.
        #### Returns
        - `ItemSet` : The converted weakpoint.
        """
        return Weakpoint(
            key_name=data['key_name'],
            damage_multiplier=data['damage_multiplier'],
            damage_sources=data['damage_sources'],
            unknown_fields=data['unknown_fields']
        )
    
    @staticmethod
    def get_unknown_fields() -> list[str]:
        """
        This method is responsible for returning the unknown fields of the weakpoint.
        #### Returns
        - `list[str]` : The unknown fields of the weakpoint.
        """
        return [
            'ForwardComponentName',
            'ForwardAngleRange',
            'DamageTypeFlags',
            'DamageType'
        ]