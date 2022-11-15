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

from random import randint


class Health(object):
    gauge = 100

    def __init__(self, power=100):
        self.gauge = min(power, 100)

    def __add__(self, power):
        new_gauge = self.gauge + power
        return Health(new_gauge) if new_gauge <= 100 else Health(100)

    def __sub__(self, power):
        new_gauge = self.gauge - power
        return Health(new_gauge) if new_gauge >= 0 else Health(0)

    def __repr__(self):
        return str(self.gauge)

    def __eq__(self, health):
        return self.gauge == health.gauge

    @property
    def dead(self):
        return self.gauge == 0


class Character(object):

    name = None
    multiplier = 1

    def __init__(self, name=None, gauge=100):
        self.health = Health(gauge)
        # Set character strength between 1 and 3
        self.strength = randint(1,3)

    def attack(self, other):
        damage = randint(0, self.multiplier*10)
        other.health -= damage

class Player(Character):

    multiplier = 10
    # Position 0(start) 4(got the treasure)
    position = 0
    icon = "🧝"

    def __init__(self, name):
        super(Player, self).__init__(name, gauge=100)
        self.name = name

    def display_position(self):
        if self.position == 0:
            print("{}___💰".format(self.icon))
        if self.position == 1:
            print("_{}__💰".format(self.icon))
        if self.position == 2:
            print("__{}_💰".format(self.icon))
        if self.position == 3:
            print("___{}💰".format(self.icon))
        if self.position == 4:
            print("You got the 💰")
        print()

    def display_characteristics(self):
        print("Hero {}: {}".format(self.icon, self.name))
        print("--------------------------------------------------".format(self.icon))
        print("Strength: {}".format(self.strength))
        print("Health: {}".format(self.health))
        print()


class Monster(Character):
    pass
