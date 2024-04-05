from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from .display_name import DisplayName

import uuid

from pathlib import Path

class ChatWheel:
    """
    This class is responsible for crawling the chat wheel data from the game.
    #### Parameters
    - `chatter_event` : `uuid.UUID`
        - The chatter event of the chat wheel.
    - `name`: `DisplayName`
        - The chat wheel name of the chat wheel.
    - `key_name` : `str`
        - The key name of the chat wheel.
    - `icon` : `Path`
        - The icon of the chat wheel.
    - `unknown_fields` : `dict`
        - The unknown fields of the chat wheel.
    """
    def __init__(self, chatter_event: uuid.UUID, name: 'DisplayName', key_name: str, icon: Path, unknown_fields: dict):
        self.chatter_event = chatter_event
        self.name = name
        self.key_name = key_name
        self.icon = icon
        self.unknown_fields = unknown_fields

    def to_dict(self) -> dict:
        """
        This method is responsible for converting the chat wheel to a dictionary.
        #### Returns
        - `dict` : The converted chat wheel.
        """
        return {
            'chatter_event': str(self.chatter_event),
            'name': self.name.to_dict(),
            'key_name': self.key_name,
            'icon': self.icon.as_posix(),
            'unknown_fields': self.unknown_fields
        }