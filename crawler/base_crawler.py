from typing import Any
from pathlib import Path

import json

class BaseCrawler:
    """
    This class is responsible for crawling the data from the game.
    #### Parameters
    - `crawler_name` : `str`
        - The name of the crawler.
    - `root_path` : `Path`
        - The path to the root directory.
    - `json_path` : `Path`
        - The path to the json data directory.
    - `media_path` : `Path`
        - The path to the media directory.
    - `hide_unknown_fields` : `bool`
        - A flag to hide the unknown fields.
    - `unknown_field_list` : `list`
        - The list of unknown fields.
    """
    root_path: Path = None

    def __init__(self, name: str, json_path: Path, hide_unknown_fields: bool = False):
        self.crawler_name = name
        self.json_path = self.root_path / 'json_data' / json_path
        self.media_path = self.root_path / 'media_data'
        self.hide_unknown_fields = hide_unknown_fields
        self.unknown_field_list = []

    @staticmethod
    def init(root_path: Path):
        """
        This method is responsible for initializing the crawler.
        #### Parameters
        - `root_path` : `Path`
            - The path to the root directory.
        """
        BaseCrawler.root_path = root_path

    def crawl(self) -> list:
        """
        This method is responsible for crawling the data from the game.
        #### Returns
        - `list` : The crawled data.
        """
        json_data = self.json_path.read_text()
        data = json.loads(json_data)
        if len(data) > 1:
            print('There are more than 1 entry in the creatures DataTable.')
            return []
        data = data[0]['Rows']

        crawled_data = []
        for key, value in data.items():
            if self.hide_unknown_fields:
                unknown_fields = None
            else:
                unknown_fields = self._get_unknown_fields(value, self.unknown_field_list)

            crawled_data.append(self._get_crawled_data(key, value, unknown_fields))
        
        self._save(crawled_data, f'{self.crawler_name}.json')

        return crawled_data

    def _get_crawled_data(self, key: str, value: dict, unknown_fields: dict[str, Any]) -> Any:
        """
        This method is responsible for getting the crawled data.
        #### Parameters
        - `key` : `str`
            - The key of the data.
        - `value` : `dict`
            - The value of the data.
        - `unknown_fields` : `dict`
            - The unknown fields of the data.
        #### Returns
        - `Any` : The crawled data.
        """
        pass

    def _get_unknown_fields(self, value: dict, fields: list[str]) -> dict[str, Any]:
        """
        This method is responsible for getting the unknown fields of the creature.
        #### Parameters
        - `value` : `dict`
            - The value of the creature.
        - `fields` : `list`
            - The fields to be extracted.
        #### Returns
        - `dict` : The unknown fields of the creature.
        """
        unknown_fields = {}
        for field in fields:
            if '>' in field:
                keys = field.split('>')
                first_key = keys[0]
                second_key = '>'.join(keys[1:])
                unknown_fields[first_key] = self._get_unknown_fields(value[first_key], [second_key])
            else:
                unknown_fields[field] = value[field]

        return unknown_fields
    
    def _get_media_path(self, value: dict) -> Path:
        """
        This method is responsible for getting the media path of the harvest node.
        #### Parameters
        - `value` : `dict`
          - The value of the harvest node.
        #### Returns
        - `Path` : The media path of the harvest node.
        """
        if value == None:
            return Path()
        icon_ingame_path = value['ObjectPath'].replace('Game/', 'Maine/Content/')
        icon_ingame_path = f'{icon_ingame_path.split('.')[0]}.png'
        icon_path = str(self.media_path) + icon_ingame_path
        return Path(icon_path)

    def _save(self, data: list, file_name: str) -> None:
        """
        This method is responsible for saving the data to a file.
        #### Parameters
        - `data` : `list`
            - The data to be saved.
        - `file_name` : `str`
            - The name of the file to save the data.
        """
        crawled_data_path = Path('data/crawled')
        if not crawled_data_path.exists():
            crawled_data_path.mkdir(parents=True)
        data_path = crawled_data_path / file_name

        json_data = [item.to_dict() for item in data]
        data_path.write_text(json.dumps(json_data, indent=4))
