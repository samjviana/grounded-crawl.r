import json

from pathlib import Path

class DisplayName:
    """
    This class represents a display name in the game.
    #### Parameters
    - `localization_json` : `dict`
        - The localization JSON. This needs to be initialized before using the class.
    - `string_table_names` : `dict`
        - The string table names.
    """
    localization_json: dict = None
    # TODO: Add more string table names.
    string_table_names = {
        1: 'game/gui',
        2: 'game/items',
        9: 'game/characters',
        22: 'game/buildings',
        33: 'game/statuseffects',
        56: 'game/pointsofinterest',
        75: 'game/harvestnodes',
        144: 'game/chatwheel',
        197: 'game/petpersonalities',
        342: 'game/props'
    }
    
    def __init__(self, table_id: int, string_id: int, string_table_name: str, text: str = None):
        self.table_id = table_id
        self.string_id = string_id
        self.string_table_name = string_table_name
        self.text = text if text else self.get_string()
    
    @staticmethod
    def init(lang_path: Path):
        """
        This method is responsible for initializing the DisplayName localization.
        #### Parameters
        - `lang_path` : `Path`
            - The path to the language file.
        """
        buffer = []
        with open(lang_path, 'r', encoding='utf-8') as file:
            buffer = json.load(file)[0]['Properties']['StringTables']
        
        DisplayName.localization_json = {}
        for string_table in buffer:
            key = next(iter(string_table))
            DisplayName.localization_json[key] = string_table[key]

    def get_string(self) -> str:
        """
        This method is responsible for getting the string of the display name.
        #### Returns
        - `str` : The string of the display name.
        """
        if self.table_id <= 0:
            return 'UNKNOWN'
        string_table_name = DisplayName.string_table_names[self.table_id]
        entries = DisplayName.localization_json[string_table_name]['Entries']
        for entry in entries:
            entry = list(entry.values())[0]
            if entry['ID'] == self.string_id:
                return entry['DefaultText']
            
        return 'UNKNOWN'

    def to_dict(self) -> dict:
        """
        This method is responsible for converting the display name to a dictionary.
        #### Returns
        - `dict` : The converted display name.
        """
        return {
            'table_id': self.table_id,
            'string_id': self.string_id,
            'string_table_name': self.string_table_name,
            'text': self.text
        }
    
    def from_dict(data: dict):
        """
        This method is responsible for creating a display name from a dictionary.
        #### Parameters
        - `data` : `dict`
            - The dictionary data.
        #### Returns
        - `DisplayName` : The created display name.
        """
        return DisplayName(
            data['table_id'],
            data['string_id'],
            data['string_table_name'],
            data['text']
        )