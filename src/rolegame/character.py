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
        
    def attack(self, other):
        damage = randint(0, self.multiplier*10)
        other.health -= damage

class Player(Character):
    
    multiplier = 10

    def __init__(self, name):
        super(Player, self).__init__(name, gauge=100)

        
class Monster(Character):
    pass

