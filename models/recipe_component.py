from models.display_name import DisplayName
from pathlib import Path

class RecipeComponent:
    """
    Wrapper for a recipe component in a recipe.
    #### Parameters
    - `item_key`: `str`
        - The key of the item.
    - `quantity`: `int`
        - The quantity of the item.
    - `display_name`: `DisplayName`
        - The display name of the item.
    - `description`: `DisplayName`
        - The description of the item.
    - `icon_path`: `Path`
        - The icon path of the item.
    - `icon_modifier_path`: `Path`
        - The icon modifier path of the item.
    """
    def __init__(self, item_key: str, quantity: int, display_name: DisplayName, description: DisplayName, icon_path: Path, icon_modifier_path: Path):
        self.item_key = item_key
        self.quantity = quantity
        self.display_name = display_name
        self.description = description
        self.icon_path = icon_path
        self.icon_modifier_path = icon_modifier_path

    def to_dict(self) -> dict:
        """
        This method is responsible for converting the object to a dictionary.
        #### Returns
        - `dict` : The dictionary representation of the object.
        """
        return {
            'item_key': self.item_key,
            'quantity': self.quantity,
            'display_name': self.display_name.to_dict(),
            'description': self.description.to_dict(),
            'icon_path': self.icon_path.as_posix(),
            'icon_modifier_path': self.icon_modifier_path.as_posix()
        }
    
    def from_dict(data: dict) -> 'RecipeComponent':
        """
        This method is responsible for creating a RecipeComponent from a dictionary.
        #### Parameters
        - `data` : `dict`
            - The dictionary data.
        #### Returns
        - `RecipeComponent` : The created RecipeComponent.
        """
        return RecipeComponent(
            data['item_key'],
            data['quantity'],
            DisplayName.from_dict(data['display_name']),
            DisplayName.from_dict(data['description']),
            Path(data['icon_path']),
            Path(data['icon_modifier_path'])
        )