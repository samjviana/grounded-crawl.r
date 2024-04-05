class DisplayName:
    """
    This class represents a display name in the game.
    """
    def __init__(self, table_id: int, string_id: int, string_table_name: str):
        self.table_id = table_id
        self.string_id = string_id
        self.string_table_name = string_table_name
    
    def to_dict(self) -> dict:
        """
        This method is responsible for converting the display name to a dictionary.
        #### Returns
        - `dict` : The converted display name.
        """
        return {
            'table_id': self.table_id,
            'string_id': self.string_id,
            'string_table_name': self.string_table_name
        }