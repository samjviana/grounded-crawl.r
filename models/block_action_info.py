class BlockActionInfo:
    """
    A class to represent data related to Block action of a Tool or Weapon.
    #### Parameters
    - `can_block`: `bool`
        - A flag to determine if the Tool or Weapon can block.
    - `cannot_block_while_attacking`: `bool`
        - A flag to determine if the Block action can interrupt the attack action.
    - `block_damage_reduction`: `float`
        - The damage reduction when blocking.
    - `block_stamina_cost`: `float`
        - The stamina cost when blocking.
    - `block_stamina_regen_multiplier`: `float`
        - The stamina regeneration multiplier when blocking.
    """
    def __init__(self, can_block: bool, cannot_block_while_attacking: bool, block_damage_reduction: float, block_stamina_cost: float, block_stamina_regen_multiplier: float):
        self.can_block = can_block
        self.cannot_block_while_attacking = cannot_block_while_attacking
        self.block_damage_reduction = block_damage_reduction
        self.block_stamina_cost = block_stamina_cost
        self.block_stamina_regen_multiplier = block_stamina_regen_multiplier

    def to_dict(self) -> dict:
        """
        This method is responsible for converting the Block data to a dictionary.
        #### Returns
        - `dict` : The converted Block data.
        """
        return {
            'can_block': self.can_block,
            'cannot_block_while_attacking': self.cannot_block_while_attacking,
            'block_damage_reduction': self.block_damage_reduction,
            'block_stamina_cost': self.block_stamina_cost,
            'block_stamina_regen_multiplier': self.block_stamina_regen_multiplier
        }