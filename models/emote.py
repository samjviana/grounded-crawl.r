from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from .display_name import DisplayName
    from .ue_datatable_reference import UEDataTableReference

from pathlib import Path
import uuid

class Emote:
    """
    Represents an emote in the game.
    #### Parameters
    - `key_name` : `str`
        - The key name of the emote.
    - `tag` : `str`
        - The tag of the emote.
    - `name`: `DisplayName`
        - The name of the emote.
    - `icon_asset` : `str`
        - The icon of the emote.
    - `chatter_event` : `uuid.UUID`
        - The chatter event of the emote.
    - `always_unlocked` : `bool`
        - Whether the emote is always unlocked.
    - `looping` : `bool`
        - Whether the emote is looping.
    - `unknown_fields` : `dict`
        - The unknown fields of the emote.
    """
    def __init__(self, key_name: str, tag: str, name: 'DisplayName', icon_asset: str, chatter_event: uuid.UUID, always_unlocked: bool, looping: bool, unknown_fields: dict):
        self.key_name = key_name
        self.tag = tag
        self.name = name
        self.icon_asset = icon_asset
        self.chatter_event = chatter_event
        self.always_unlocked = always_unlocked
        self.looping = looping
        self.unknown_fields = unknown_fields

    def to_dict(self) -> dict:
        """
        Converts the emote to a dictionary.
        #### Returns
        - `dict` : The converted emote.
        """
        return {
            'key_name': self.key_name,
            'tag': self.tag,
            'name': self.name.to_dict(),
            'icon_asset': self.icon_asset,
            'chatter_event': str(self.chatter_event),
            'always_unlocked': self.always_unlocked,
            'looping': self.looping,
            'unknown_fields': self.unknown_fields
        }