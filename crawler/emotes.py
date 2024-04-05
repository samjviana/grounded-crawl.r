
from typing import Any
from .base_crawler import BaseCrawler
from pathlib import Path
from models import Emote, DisplayName
import uuid

class EmotesCrawler(BaseCrawler):
    """
    This class is responsible for crawling the emotes data from the game.
    """
    def __init__(self, hide_unknown_fields: bool = False):
        super().__init__(
            name='emotes',
            json_path=Path('Maine/Content/Blueprints/DataTables/Table_Emotes.json'),
            hide_unknown_fields=hide_unknown_fields
        )

    def _get_crawled_data(self, key: str, value: dict, unknown_fields: dict[str, Any]) -> Emote:
        emote_name = DisplayName(
            table_id=value['EmoteName']['StringTableID'],
            string_id=value['EmoteName']['StringID'],
            string_table_name=value['EmoteName']['StringTableName']
        )

        chatter_event = uuid.UUID(value['ChatterEvent']['ID'])

        emote = Emote(
            key_name=key,
            tag=value['EmoteTag']['TagName'],
            name=emote_name,
            icon_asset=value['EmoteIcon']['AssetPathName'],
            chatter_event=chatter_event,
            always_unlocked=value['bAlwaysUnlocked'],
            looping=value['bLooping'],
            unknown_fields=unknown_fields
        )

        return emote
    