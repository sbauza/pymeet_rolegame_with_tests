#    Licensed under the Apache License, Version 2.0 (the "License"); you may
#    not use this file except in compliance with the License. You may obtain
#    a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#    WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#    License for the specific language governing permissions and limitations
#    under the License.

# This is required for type hinting a method with the enclosing class
from __future__ import annotations
from random import randint


class Health(object):
    gauge = 100

    def __init__(self, power: int = 100) -> None:
        self.gauge = min(power, 100)

    def __add__(self, power: int) -> Health:
        new_gauge = self.gauge + power
        return Health(new_gauge) if new_gauge <= 100 else Health(100)

    def __sub__(self, power: int) -> Health:
        new_gauge = self.gauge - power
        return Health(new_gauge) if new_gauge >= 0 else Health(0)

    def __str__(self) -> str:
        return str(self.gauge)

    def __eq__(self, health: Health) -> bool:  # type: ignore[override]
        return self.gauge == health.gauge

    @property
    def dead(self) -> bool:
        return self.gauge == 0


class Character(object):

    icon : str = ""
    type : str = ""
    name : str = ""

    def __init__(self, name: str, health: int = 100) -> None:
        self.health = Health(health)
        # Set character strength between 1 and 3
        self.strength = randint(1, 3)
        self.name = name

    def attack(self, damage: int, other: Character) -> None:
        print("🎲 {} hits {} on {}".format(self.name, damage, other.name))
        other.health -= damage

    @property
    def dead(self) -> bool:
        return self.health.dead

    def display_characteristics(self) -> None:
        print("{} {}: {}".format(self.type, self.icon, self.name))
        print("--------------------------------------------")
        print("Strength: {}".format(self.strength))
        print("Health: {}".format(self.health))
        print()


class Player(Character):

    icon = "🧝"
    type = 'Hero'

    def __init__(self, name: str) -> None:
        super(Player, self).__init__(name, health=100)

    @classmethod
    def newPlayer(cls) -> Player:
        name = input("Enter your hero name: ")
        return cls(name)


class Monster(Character):

    type = 'Monster'

    def __init__(self, name: str,
                 health: int, strength: int, icon: str) -> None:
        super(Monster, self).__init__(name, health)
        self.icon = icon
        self.strength = strength
