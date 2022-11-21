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

from rolegame import character


# This is a fake class acting like a Monster class but not inherited from it.
class FakeIndependentMonster(character.Character):
    type = 'Monster'
    name = 'FakeIgor'
    icon = '🧟'
    strength = 3
    health = '100'

    def __init__(self, **kwargs):
        # we always redefine the kwargs
        super(FakeIndependentMonster, self).__init__(self.name,
                                                     health=int(self.health))
        self.strength = 3


# This is just a dict for faking an API response from the GET /monsters verb.
fake_monster_dict = {
    # Just an optimization to not duplicate testcode, we reuse the object above.
    'name': FakeIndependentMonster.name,
    'icon': FakeIndependentMonster.icon,
    'health': int(FakeIndependentMonster.health),
    'strength' : FakeIndependentMonster.strength
}
