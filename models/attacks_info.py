from models import Attack

class AttacksInfo:
    """
    Wraps the information about the attacks of a Tool or Weapon.
    #### Parameters
    - `main_combo`: `list[Attack]`
        - The main combo attacks of the Tool or Weapon.
    - `main_scaling`: `list[float]`
        - The main scaling factors of the Tool or Weapon.
    - `alternate_combo`: `list[Attack]`
        - The alternate combo attacks of the Tool or Weapon.
    - `alternate_scaling`: `list[float]`
        - The alternate scaling factors of the Tool or Weapon.
    - `swimming_combo`: `list[Attack]`
        - The swimming combo attacks of the Tool or Weapon.
    - `swimming_scaling`: `list[float]`
        - The swimming scaling factors of the Tool or Weapon.
    """
    def __init__(self, main_combo: list[Attack], main_scaling: list[float], alternate_combo: list[Attack], alternate_scaling: list[float], swimming_combo: list[Attack], swimming_scaling: list[float]):
        self.main_combo = main_combo
        self.main_scaling = main_scaling
        self.alternate_combo = alternate_combo
        self.alternate_scaling = alternate_scaling
        self.swimming_combo = swimming_combo
        self.swimming_scaling = swimming_scaling

    def to_dict(self) -> dict:
        """
        This method is responsible for converting the Attacks data to a dictionary.
        #### Returns
        - `dict` : The converted Attacks data.
        """
        return {
            'main_combo': [attack.to_dict() for attack in self.main_combo],
            'main_scaling': self.main_scaling,
            'alternate_combo': [attack.to_dict() for attack in self.alternate_combo],
            'alternate_scaling': self.alternate_scaling,
            'swimming_combo': [attack.to_dict() for attack in self.swimming_combo],
            'swimming_scaling': self.swimming_scaling
        }
    
    def from_dict(data: dict) -> 'AttacksInfo':
        """
        This method is responsible for converting the dictionary to a AttacksInfo object.
        #### Parameters
        - `data`: `dict`
            - The dictionary to convert.
        #### Returns
        - `AttacksInfo` : The converted AttacksInfo object.
        """
        return AttacksInfo(
            [Attack.from_dict(attack) for attack in data['main_combo']],
            data['main_scaling'],
            [Attack.from_dict(attack) for attack in data['alternate_combo']],
            data['alternate_scaling'],
            [Attack.from_dict(attack) for attack in data['swimming_combo']],
            data['swimming_scaling']
        )