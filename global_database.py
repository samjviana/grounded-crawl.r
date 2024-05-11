from models import StatusEffect
from typing import Any

class GlobalDatabase:
    """
    This class is used to store the crawled data across all the crawlers.
    
    #### Attributes
    - `status_effects`: `dict[str, StatusEffect]`
        - The status effects data.
    """
    status_effects: dict[str, StatusEffect] = None

    def __init__(self):
        pass

    @staticmethod
    def add_crawled_data(crawler_name: str, crawled_data: dict[str, Any]) -> None:
        """
        This method is responsible for adding the crawled data to the global database.
        #### Parameters
        - `crawler_name` : `str`
            - The name of the crawler.
        - `crawled_data` : `dict`
            - The crawled data.
        """
        if not hasattr(GlobalDatabase, crawler_name):
            # TODO: This should be a logger. But for now, we will just skip since there are some crawlers that are not yet implemented.
            return

        setattr(GlobalDatabase, crawler_name, crawled_data)

    @staticmethod
    def get_crawled_data(crawler_name: str, key: str) -> Any:
        """
        This method is responsible for getting the crawled data from the global database.
        #### Parameters
        - `crawler_name` : `str`
            - The name of the crawler.
        - `key` : `str`
            - The key of the data.
        #### Returns
        - `Any` : The crawled data.
        """
        if not hasattr(GlobalDatabase, crawler_name):
            # TODO: Some crawlers that are not yet implemented.
            raise Exception(f'There is no data for the crawler: {crawler_name}')
        
        data = getattr(GlobalDatabase, crawler_name)
        if key not in data:
            raise Exception(f'The key: {key} does not exist in the data for the crawler: {crawler_name}')
        
        return data[key]
