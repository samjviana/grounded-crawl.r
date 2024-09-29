from __future__ import annotations

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from .display_name import DisplayName
    from .ue_object import UEObject

from .status_effect import StatusEffect
from .weakpoint import Weakpoint
from pathlib import Path

class CreatureInfo:
    # TODO: Implement a class to hold the stun information
    """
    This class is responsible for representing the stats of a creature.
    #### Parameters
    - `health` : `float`
        - The health of the creature.
    - `base_damage_reduction` : `float`
        - The base damage reduction of the creature.
    - `weakpoints`: `list[Weakpoint]`
        - The weakpoints of the creature.
    - `loot`: list
        - The loot of the creature.
    - `max_stun` : `float`
        - The stun damage needed to stun the creature.
    - `stun_decay` : `float`
        - The rate at which the stun damage decays.
    - `stun_duration` : `float`
        - The duration of the stun.
    - `stun_cooldown` : `float`
        - The cooldown of the stun.
    - `status_effects` : `list[StatusEffect]`
        - The status effects of the creature.
    - `immunity_tags` : `list[str]`
        - The immunity tags of the creature.
    - `team` : `str`
        - The team of the creature.
    - `unknown_fields` : `dict`
        - The unknown fields of the creature.
    """
    def __init__(self, health: float, base_damage_reduction: float, weakpoints: list[Weakpoint], loot: list, max_stun: float, stun_decay: float, stun_duration: float, stun_cooldown: float, status_effects: list[StatusEffect], immunity_tags: list[str], team: str, unknown_fields: dict):
        self.health = health
        self.base_damage_reduction = base_damage_reduction
        self.weakpoints = weakpoints
        self.loot = loot
        self.max_stun = max_stun
        self.stun_decay = stun_decay
        self.stun_duration = stun_duration
        self.stun_cooldown = stun_cooldown
        self.status_effects = status_effects
        self.immunity_tags = immunity_tags
        self.team = team
        self.unknown_fields = unknown_fields

    def to_dict(self) -> dict:
        """
        This method is responsible for converting the creature info to a dictionary.
        #### Returns
        - `dict` : The converted creature info.
        """
        return {
            'health': self.health,
            'base_damage_reduction': self.base_damage_reduction,
            'weakpoints': [weakpoint.to_dict() for weakpoint in self.weakpoints],
            'loot': self.loot,
            'max_stun': self.max_stun,
            'stun_decay': self.stun_decay,
            'stun_duration': self.stun_duration,
            'stun_cooldown': self.stun_cooldown,
            'status_effects': [status_effect.to_dict() for status_effect in self.status_effects],
            'immunity_tags': self.immunity_tags,
            'team': self.team,
            'unknown_fields': self.unknown_fields
        }

    def from_dict(data: dict) -> 'CreatureInfo':
        """
        This method is responsible for converting the dictionary to a CreatureInfo object.
        #### Parameters
        - `data`: `dict`
            - The dictionary to convert.
        #### Returns
        - `CreatureInfo` : The converted CreatureInfo object.
        """
        return CreatureInfo(
            data['health'],
            data['base_damage_reduction'],
            [Weakpoint.from_dict(weakpoint) for weakpoint in data['weakpoints']],
            data['loot'],
            data['max_stun'],
            data['stun_decay'],
            data['stun_duration'],
            data['stun_cooldown'],
            [StatusEffect.from_dict(status_effect) for status_effect in data['status_effects']],
            data['immunity_tags'],
            data['team'],
            data['unknown_fields']
        )

    @staticmethod
    def get_unknown_fields() -> list[str]:
        """
        This method is responsible for getting the unknown fields of the creature.
        #### Returns
        - `list` : The unknown fields of the creature.
        """
        return []
        return [
            10, # AttackInfoComponent
            28, # MaineCharMovementComponent
            31, # PlayerLookTriggerComponent
            32, # PlayerScalingReceiverComponent
        ]
