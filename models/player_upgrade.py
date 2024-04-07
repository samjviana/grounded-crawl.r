    #   "Health": {
    #     "LocalizedDisplayName": {
    #       "StringTableID": 1,
    #       "StringID": 1508,
    #       "StringTableName": "None"
    #     },
    #     "Icon": {
    #       "AssetPathName": "/Game/UI/Images/System/T_UI_MM_Upgrade_Health.T_UI_MM_Upgrade_Health",
    #       "SubPathString": ""
    #     },
    #     "BaseCost": 0,
    #     "UpgradeType": "EPlayerUpgradeType::StatusEffect",
    #     "Tiers": [
    #       {
    #         "StatusEffectData": [
    #           {
    #             "DataTable": {
    #               "ObjectName": "DataTable'Table_StatusEffects'",
    #               "ObjectPath": "/Game/Blueprints/Attacks/Table_StatusEffects.0"
    #             },
    #             "RowName": "PlayerUpgradeHealth1"
    #           }
    #         ],
    #         "Value": 0
    #       },
    #       {
    #         "StatusEffectData": [
    #           {
    #             "DataTable": {
    #               "ObjectName": "DataTable'Table_StatusEffects'",
    #               "ObjectPath": "/Game/Blueprints/Attacks/Table_StatusEffects.0"
    #             },
    #             "RowName": "PlayerUpgradeHealth2"
    #           }
    #         ],
    #         "Value": 0
    #       },
    #       {
    #         "StatusEffectData": [
    #           {
    #             "DataTable": {
    #               "ObjectName": "DataTable'Table_StatusEffects'",
    #               "ObjectPath": "/Game/Blueprints/Attacks/Table_StatusEffects.0"
    #             },
    #             "RowName": "PlayerUpgradeHealth3"
    #           }
    #         ],
    #         "Value": 0
    #       },
    #       {
    #         "StatusEffectData": [
    #           {
    #             "DataTable": {
    #               "ObjectName": "DataTable'Table_StatusEffects'",
    #               "ObjectPath": "/Game/Blueprints/Attacks/Table_StatusEffects.0"
    #             },
    #             "RowName": "PlayerUpgradeHealth4"
    #           }
    #         ],
    #         "Value": 0
    #       },
    #       {
    #         "StatusEffectData": [
    #           {
    #             "DataTable": {
    #               "ObjectName": "DataTable'Table_StatusEffects'",
    #               "ObjectPath": "/Game/Blueprints/Attacks/Table_StatusEffects.0"
    #             },
    #             "RowName": "PlayerUpgradeHealth5"
    #           }
    #         ],
    #         "Value": 0
    #       },
    #       {
    #         "StatusEffectData": [
    #           {
    #             "DataTable": {
    #               "ObjectName": "DataTable'Table_StatusEffects'",
    #               "ObjectPath": "/Game/Blueprints/Attacks/Table_StatusEffects.0"
    #             },
    #             "RowName": "PlayerUpgradeHealth6"
    #           }
    #         ],
    #         "Value": 0
    #       }
    #     ]
    #   },

class PlayerUpgrade:
    """
    Represents a player upgrade in the game.
    #### Parameters
    - `name` : `str`
        - The name of the player upgrade.
    - `key_name`: `str`
        - The key name of the player upgrade.
    - `icon_asset_path` : `str`
        - The icon asset path of the player upgrade.
    - `base_cost`: `int`
        - The base cost of the player upgrade.
    - ``unknown_fields`` : `dict`
        - The unknown fields of the player upgrade.
    """
    def __init__(self, name: str, key_name: str, icon_asset_path: str, base_cost: int, unknown_fields: dict):
        self.name = name
        self.key_name = key_name
        self.icon_asset_path = icon_asset_path
        self.base_cost = base_cost
        self.unknown_fields = unknown_fields

    def to_dict(self) -> dict:
        """
        Converts the player upgrade to a dictionary.
        #### Returns
        - `dict` : The converted player upgrade.
        """
        return {
            'name': self.name.to_dict(),
            'key_name': self.key_name,
            'icon_asset_path': self.icon_asset_path,
            'base_cost': self.base_cost,
            'unknown_fields': self.unknown_fields
        }