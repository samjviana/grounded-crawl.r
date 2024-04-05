from typing import Any
from .base_crawler import BaseCrawler
from pathlib import Path
from models import ChatWheel, DisplayName
from util import string_table_names
import uuid

class ChatWheelCrawler(BaseCrawler):
    """
    This class is responsible for crawling the chat_wheel data from the game.
    """
    def __init__(self, hide_unknown_fields: bool = False):
        super().__init__(
            name='chat_wheel',
            json_path=Path('Maine/Content/Blueprints/DataTables/Table_ChatWheel.json'),
            hide_unknown_fields=hide_unknown_fields
        )
    
    def _get_crawled_data(self, key: str, value: dict, unknown_fields: dict[str, Any]) -> ChatWheel:
        chatter_event = uuid.UUID(value['ChatterEvent']['ID'])

        name = DisplayName(
            table_id=value['ChatWheelName']['StringTableID'],
            string_id=value['ChatWheelName']['StringID'],
            string_table_name=value['ChatWheelName']['StringTableName']
        )
        if name.string_table_name == 'None':
            name.string_table_name = string_table_names[name.table_id]

        icon = self._get_media_path(value['ChatWheelIcon'])

        chat_wheel = ChatWheel(
            chatter_event=chatter_event,
            name=name,
            key_name=key,
            icon=icon,
            unknown_fields=unknown_fields
        )
        return chat_wheel
    