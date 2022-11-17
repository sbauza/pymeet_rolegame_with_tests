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

#This is required for type hinting a method with the enclosing class
from __future__ import annotations
import random

from rolegame import character
from rolegame import client


class Game(object):

    # The minimum number of the dice in order to succeed to flee a monster
    fled_dice_success_min = 9

    # The number of turns
    rounds = 5

    @staticmethod
    def get_difficulties():
        return ['easy', 'medium', 'hard']

    @classmethod
    def difficulty(cls, difficulty: str = 'medium') -> None:
        if difficulty == 'easy':
            cls.rounds = 2
            cls.fled_dice_success_min = 1
        elif difficulty == 'medium':
            cls.rounds = 5
            cls.fled_dice_success_min = 9
        elif difficulty == 'hard':
            cls.rounds = 10
            cls.fled_dice_success_min = 11

    def __init__(self, player: character.Player) -> None:
        self.player = player
        self.position = 0
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
            print("🧌  Argh, you have been spotted by a monster !!!")
        return spotted == True

    def get_monster(self) -> character.Monster:
        monster_dict = self.client.get_monster()
        monster = character.Monster(**monster_dict)
        monster.display_characteristics()
        return monster

    def _attack(
            self, attacker: character.Character, attacked: character.Character
        ) -> None:
        dice = self.client.get_dice()
        attacker.attack(attacker.strength * dice, attacked)

    def fight(self, monster: character.Monster) -> None:
        print("⚔️  You decided to fight to death " + monster.name)
        while True:
            self._attack(self.player, monster)
            if monster.dead:
                print('You killed the monster.\n\n')
                break
            self._attack(monster, self.player)
            if self.player.dead:
                break

    def flee(self) -> bool:
        print("🏃 You try to run away")
        dice = self.client.get_dice()
        # only numbers above FLED_DICE_SUCCESS_MIN allow us to flee
        fled = dice > self.fled_dice_success_min
        if fled:
            print("Huzzah, you were able to flee the monster !")
        else:
            dice = self.client.get_dice()
            self.player.health -= dice
            print("You're exhausted by the unsuccessful run, "
                  "your health reduces by {}.".format(dice))
        return fled

    def rest(self) -> None:
        print("💤 You decide to take some rest: ")
        dice = self.client.get_dice()
        # if you're fortunate, you can get 100 more XPs but in average, you will
        # only get around 25 XPs, mwahahaha
        added_health = round(100 / dice)
        print("You're fortunate to gain {} XPs".format(added_health))
        self.player.health += added_health
        self.player.display_characteristics()
        # dice numbers above 6 don't give you extra rounds, but if less than 6,
        # you'll get more XP with a tradeoff of up to 6 extra rounds.
        added_rounds = int(added_health / 15)
        if added_rounds:
            s = 's' if added_rounds > 1 else ''
            print("... but it takes {} more round{}.".format(added_rounds, s))
            self.rounds += added_rounds
