from .base_crawler import BaseCrawler
from models import CraftingRecipe, RecipeComponent
from pathlib import Path
from typing import Any

class CraftingRecipesCrawler(BaseCrawler):
    """
    Class responsible for crawling the crafting recipes data.
    """

    def __init__(self, hide_unknown_fields: bool = False):
        super().__init__(
            name='crafting_recipes',
            json_path=Path('Maine/Content/Blueprints/Items/Table_CraftingRecipes.json'),
            hide_unknown_fields=hide_unknown_fields
        )
        self.unknown_field_list = CraftingRecipe.get_unknown_fields()

    def dispose(self) -> None:
        return super().dispose()
    
    def _get_crawled_data(self, key: str, value: dict, unknown_fields: dict[str, Any]) -> CraftingRecipe:
        item = self._parse_item(value['CraftedItem'])

        components = []
        for component in value['Requirements']:
            quantity = component['ItemCount']
            item_key = component['Item']['RowName']
            item = self._parse_item(component['Item'])
            recipe_component = None
            if item is not None:
                recipe_component = RecipeComponent(
                    item_key=item_key,
                    quantity=quantity,
                    display_name=item.name,
                    description=item.description,
                    icon_path=item.icon_path,
                    icon_modifier_path=item.icon_modifier_path,
                )

            components.append(recipe_component)

        return CraftingRecipe(
            key_name=key,
            item=item,
            components=components,
            quantity=value['CraftedItemCount'],
            category=value['CategoryTag']['TagName'],
            unknown_fields=unknown_fields
        )