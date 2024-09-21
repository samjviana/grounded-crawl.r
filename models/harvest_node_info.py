class HarvestNodeInfo:
    # TODO: Revise the `required_damage_type_flags` parameter to be a list of strings.
    """
    This class is responsible for representing detailed information about a harvest node.
    #### Parameters
    - `health` : `float`
        - The health of the harvest node.
    - `required_damage_type_flags` : `int`
        - The required damage type flags of the harvest node.
    - `tags` : `list[str]`
        - The tags of the harvest node.
    - `loot` : `list[dict]`
        - The loot of the harvest node.
    """
    def __init__(self, health: float, required_damage_type_flags: int, tags: list[str], loot: list[dict]):
        self.health = health
        self.required_damage_type_flags = required_damage_type_flags
        self.tags = tags
        self.loot = loot

    def to_dict(self) -> dict:
        """
        This method is responsible for converting the harvest node info to a dictionary.
        #### Returns
        - `dict` : The converted harvest node info.
        """
        return {
            'health': self.health,
            'required_damage_type_flags': self.required_damage_type_flags,
            'tags': self.tags,
            'loot': self.loot
        }

    def from_dict(data: dict) -> 'HarvestNodeInfo':
        """
        This method is responsible for converting a dictionary to a harvest node info.
        #### Parameters
        - `data` : `dict`
            - The dictionary to convert.
        #### Returns
        - `HarvestNodeInfo` : The converted harvest node info.
        """
        return HarvestNodeInfo(
            health=data['health'],
            required_damage_type_flags=data['required_damage_type_flags'],
            tags=data['tags'],
            loot=data['loot']
        )