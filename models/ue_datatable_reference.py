from __future__ import annotations

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from .ue_object import UEObject

class UEDataTableReference:
    """
    This class is used to store the reference to the UEDataTable object.
    #### Parameters
    - `row_name` : `str`
        - The row name of the UEDataTable object.
    - `data_table`: `UEObject`
        - The UEDataTable object.
    """
    def __init__(self, row_name: str, data_table: 'UEObject'):
        self.row_name = row_name
        self.data_table = data_table

    def to_dict(self) -> dict:
        """
        This method is responsible for converting the UEDataTableReference to a dictionary.
        #### Returns
        - `dict` : The converted UEDataTableReference.
        """
        return {
            'row_name': self.row_name,
            'data_table': self.data_table.to_dict()
        }
    
    def from_dict(data: dict) -> UEDataTableReference:
        """
        This method is responsible for converting the dictionary to a UEDataTableReference object.
        #### Parameters
        - `data` : `dict`
            - The dictionary to convert.
        #### Returns
        - `UEDataTableReference` : The converted UEDataTableReference object.
        """
        return UEDataTableReference(data['row_name'], UEObject.from_dict(data['data_table']))