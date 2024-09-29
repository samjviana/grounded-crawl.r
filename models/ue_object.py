class UEObject:
    """
    This class represents an Unreal Engine object.
    #### Parameters
    - `name`: `str`
        - The name of the object.
    - `path`: `str`
        - The path to the object.
    """
    def __init__(self, name: str, path: str):
        self.name = name
        self.path = path

    def to_dict(self) -> dict:
        """
        This method is responsible for converting the Unreal Engine object to a dictionary.
        #### Returns
        - `dict` : The converted Unreal Engine object.
        """
        return {
            'name': self.name,
            'path': self.path
        }
    
    def from_dict(data: dict) -> 'UEObject':
        """
        This method is responsible for converting the dictionary to a UEObject object.
        #### Parameters
        - `data` : `dict`
            - The dictionary to convert.
        #### Returns
        - `UEObject` : The converted UEObject object.
        """
        return UEObject(data['name'], data['path'])