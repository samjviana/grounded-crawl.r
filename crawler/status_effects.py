from pathlib import Path
from .base_crawler import BaseCrawler
from models import StatusEffect, DisplayName
from typing import Any

class StatusEffectsCrawler(BaseCrawler):
    """
    Crawler for the status effects data.
    """
    def __init__(self, hide_unknown_fields: bool = False):
        super().__init__(
            name='status_effects',
            json_path=Path('Maine/Content/Blueprints/Attacks/Table_StatusEffects.json'),
            hide_unknown_fields=hide_unknown_fields
        )
        self.unknown_fields = StatusEffect.get_unknown_fields()

    def dispose(self) -> None:
        pass

    def _get_crawled_data(self, key: str, value: dict, unknown_fields: dict[str, Any]) -> StatusEffect:
        display_name = self._get_display_name(value['DisplayData']['Name'])
        description = self._get_display_name(value['DisplayData']['Description'])

        icon_path = self._get_media_path(value['DisplayData']['Icon'])

        return StatusEffect(
            key_name=key,
            display_name=display_name,
            description=description,
            icon_path=icon_path,
            effect_type=value['Type'],
            value=value['Value'],
            duration_type=value['DurationType'],
            duration=value['Duration'],
            interval=value['Interval'],
            max_stack=value['MaxStackCount'],
            is_negative_effect=value['bIsNegativeEffectInUI'],
            unknown_fields=unknown_fields
        )