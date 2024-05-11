from pathlib import Path
from .base_crawler import BaseCrawler
from models import Mutation, DisplayName, MutationTier
from typing import Any
from global_database import GlobalDatabase

class MutationsCrawler(BaseCrawler):
    """
    Crawler for the mutations(perks) data.
    """
    def __init__(self, hide_unknown_fields: bool = False):
        super().__init__(
            name='mutations',
            json_path=Path('Maine/Content/Design/Perks/Table_Perks.json'),
            hide_unknown_fields=hide_unknown_fields
        )
        self.unknown_fields = Mutation.get_unknown_fields()

    def dispose(self) -> None:
        pass

    def _get_tiers(self, tiers: list[dict[str, Any]]) -> list[MutationTier]:
        mutation_tiers = []
        for tier in tiers:
            status_effects = []
            for status_effect in tier['Reward']['StatusEffects']:
                status_effect_key = status_effect['RowName']
                status_effects.append(GlobalDatabase.get_crawled_data('status_effects', status_effect_key))

            recipes = [ recipe['RowName'] for recipe in tier['Reward']['Recipes'] ]

            mutation_tiers.append(MutationTier(
                condition=tier['Condition']['Value'],
                status_effects=status_effects,
                recipes=recipes
            ))

        return mutation_tiers

    def _get_crawled_data(self, key: str, value: dict, unknown_fields: dict[str, Any]) -> Mutation:
        name = self._get_display_name(value['LocalizedDisplayName'])
        description = self._get_display_name(value['LocalizedDescription'])

        icon_path = self._get_media_path(value['Icon'])

        stat_obj = value['Stat']
        stat = None if stat_obj == None else stat_obj['ObjectPath'].split('/')[-1].split('.')[0]

        tiers = self._get_tiers(value['Tiers'])

        return Mutation(
            key_name=key,
            display_name=name,
            description=description,
            icon_path=icon_path,
            stat=stat,
            tiers=tiers,
            unknown_fields=unknown_fields
        )
