import json
import uuid

from pathlib import Path
from models import Achievement
from typing import Any
from .base_crawler import BaseCrawler

class AchievementsCrawler(BaseCrawler):
    """
    This class is responsible for crawling the achievements data from the game.
    """
    def __init__(self, hide_unknown_fields: bool = False):
        super().__init__(
            name='achievements',
            json_path=Path('Maine/Content/Blueprints/DataTables/Table_Achievements.json'),
            hide_unknown_fields=hide_unknown_fields
        )
        self.unknown_field_list = [
            'PlayerStat',
            'bTotalPartyPlayerStat',
            'AchievementStat',
            'ComparisonOperator',
            'ConditionalValue',
            'bHostMustBePresentAtValueChange',
            'bClientMustBePresentAtValueChange'
        ]

    def _get_crawled_data(self, key: str, value: dict, unknown_fields: dict[str, Any]) -> Achievement:
        achievement = Achievement(
            id=uuid.UUID(value['GlobalVariable']['ID']),
            name=key,
            unlock_tag=value['AchievementUnlockTag'],
            can_unlock_in_creative=value['bCanUnlockInCreativeMode'],
            unknown_fields=unknown_fields
        )
        return achievement