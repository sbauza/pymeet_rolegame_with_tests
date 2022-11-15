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


import random

from rolegame import character
from rolegame import client

# The minimum number of the dice in order to succeed to flee a monster
FLED_DICE_SUCCESS_MIN = 11


class Game(object):

    # Position min=0(start) max=rounds(got the treasure)
    position = 0

    def __init__(self, player: character.Player, rounds: int = 4) -> None:
        self.player = player
        self.rounds = rounds
        self.client = client.Client()

    def display_position(self) -> None:
        rounds_left = self.rounds - self.position -1  # we count from 0
        if self.is_over():
            print("You got the 💰")
        else:
            print("_"*self.position + "{}".format(self.player.icon)
                  + "_"*rounds_left + "💰")

    def is_over(self) -> bool:
        return self.position == self.rounds

    def move(self) -> None:
        self.position += 1

    @property
    def spotted(self) -> bool:
        dice = self.client.get_dice()
        # odd numbers from the dice make us spotted by the monster !!!
        spotted = dice % 2
        if spotted:
            print("Argh, you have been spotted by a monster !!!")
        return spotted == True

    def _attack(
            self, attacker: character.Character, attacked: character.Character
        ) -> None:
        dice = self.client.get_dice()
        attacker.attack(attacker.strength * dice, attacked)

    def fight(self) -> None:
        monster_dict = self.client.get_monster()
        monster = character.Monster(**monster_dict)
        print("You fight the monster " + monster.name )
        monster.display_characteristics()
        while True:
            self._attack(self.player, monster)
            if monster.dead:
                print('You killed the monster.\n\n')
                break
            self._attack(monster, self.player)
            if self.player.dead:
                break

    def flee(self) -> None:
        print("You try to run away")
        dice = self.client.get_dice()
        # only numbers above 9 allow us to flee
        fled = dice > FLED_DICE_SUCCESS_MIN
        if fled:
            print("Huzzah, you were able to flee the monster !")
        else:
            dice = self.client.get_dice()
            self.player.health -= dice
            print("You're exhausted by the unsuccessful run, "
                  "your health reduces by {}.".format(dice))
        return fled
        
    def rest(self) -> None:
        print("You decide to take some rest but it takes 3 more rounds.")
        self.player.health += 10
        self.player.display_characteristics()
        self.rounds += 3
