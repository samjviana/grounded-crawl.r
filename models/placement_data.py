class PlacementData:
    """
    Represents the placement data of a placeable static mesh.
    #### Parameters
    - `subcategory_tag` : `str`
        - The subcategory tag of the placement object.
    - `max_slope`: `float`
        - The max slope of the placement object.
    - `scale` : `float`
        - The scale of the placement object.
    - `unknown_fields` : `dict`
        - The unknown fields of the placement object.
    """
    def __init__(self, subcategory_tag: str, max_slope: float, scale: float, unknown_fields: dict):
        self.subcategory_tag = subcategory_tag
        self.max_slope = max_slope
        self.scale = scale
        self.unknown_fields = unknown_fields

    def to_dict(self) -> dict:
        return {
            'subcategory_tag': self.subcategory_tag,
            'max_slope': self.max_slope,
            'scale': self.scale,
            'unknown_fields': self.unknown_fields
        }

    @staticmethod
    def get_unknown_fields() -> dict:
        return [
            'bPermitForUGC',
            'bHasUGCInteractions',
            'Actor',
            'ActorFlipped',
            'ActorWall',
            'ActorCeiling',
            'SlotType',
            'bUseAlternateSlotType',
            'AlternateSlotType',
            'EmbedMode',
            'bPlaceAtPlayerRotation',
            'bPermitExtraRotationAxes',
            'bPermitRescaling',
            'bAllowPlaceInWater',
            'RandomRotateIncrement',
            'BuoyantPlacement',
            'TerrainConform',
            'OverridePlacementDistance',
            'PlacementOriginOffset',
            'AttachedPlacementOffset',
            'OverrideAllowedWallNormal'
        ]