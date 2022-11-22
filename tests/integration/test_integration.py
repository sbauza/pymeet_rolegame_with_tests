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

# THIS TEST MODULE IS NOT INTENDED TO HAVE A FULL COVERAGE. THIS IS JUST FOR
# THE MEETUP.

import io
import json
import os
import responses
import unittest
from unittest import mock

# Maybe sometimes you couldn't just import your external API but this time, meh.
from external_service.monsters import MONSTERS
# Just import the main loader.
from rolegame import main
# Remember we already created a fake monster ?
from tests.unittest import fake


class FakeApp(object):
    def __init__(self):
        # let's just add our favorite FakeIgor :-)
        # By default this fixture will return all the monsters from the API
        # one by one and then the FakeIgor one.
        monsters = [monster for monster in MONSTERS]
        monsters.append(fake.fake_monster_dict)

        # Here, we provide an iterator for that list of monsters we can return
        self._monsters = monsters
        self._monsters_iter = iter(self._monsters)
        # We persist a generator that will return the next dice from the below
        # list
        self.loaded_dice_seq = [1]
        self._dices_gen = self._loaded_dice_gen()

    def _loaded_dice_gen(self):
        for dice in self.loaded_dice_seq:
            yield dice

    # This property will return the next dice from the list using the generator.
    @property
    def loaded_dices(self):
        try:
            dice = next(self._dices_gen)
        except StopIteration:
            # We need to reset the generator as we went to the end of it.
            self._dices_gen = self._loaded_dice_gen()
            dice = next(self._dices_gen)
        return dice

    # Any test can use this setter for providing the dices list.
    @loaded_dices.setter
    def loaded_dices(self, dice_list):
        if isinstance(dice_list, int):
            dice_list = [dice_list]
        self.loaded_dice_seq = dice_list
        self._dices_gen = self._loaded_dice_gen()

    # Here, we return the next monster from the iterator.
    @property
    def monsters(self):
        try:
            return next(self._monsters_iter)
        except StopIteration:
            self._monsters_iter = iter(self._monsters)
            return next(self._monsters_iter)

    # And here, we can set the list of monsters to return.
    @monsters.setter
    def monsters(self, monsters_list):
        self._monsters = monsters_list
        self._monsters_iter = iter(self._monsters)

    def get_monster(self):
        # We return the next element in the list of monsters to show up
        return self.monsters

    def get_dice(self):
        # let's just stack the odds.
        return {'score': self.loaded_dices}


class IntegrationTestsV1(unittest.TestCase):

    # Now this is time to plumb the above so it fakes the external API
    def setUp(self):
        # We load the FakeApp now so we have a shared state between tests.
        self.fake_app = FakeApp()
        # Let's do the plumbing using the responses library
        self.mock_req = responses.RequestsMock()
        self.mock_req.start()
        self.addCleanup(self.mock_req.stop)
        self.addCleanup(self.mock_req.reset)

        def callback_get_monster(request):
            return (200, {}, json.dumps(self.fake_app.get_monster()))

        def callback_get_dice(request):
            return (200, {}, json.dumps(self.fake_app.get_dice()))

        self.mock_req.get(
            "http://localhost:5000",
            json={'Status': 'OK'}
        )
        self.mock_req.add_callback(
            responses.GET,
            "http://localhost:5000/monster",
            callback=callback_get_monster,
            content_type="application/json"
        )
        self.mock_req.add_callback(
            responses.GET,
            "http://localhost:5000/dice",
            callback=callback_get_dice,
            content_type="application/json"
        )

        patch_input = mock.patch('builtins.input')
        # We gonna make the inputs as pre-conditions for the test.
        self.mock_input = patch_input.start()
        self.addCleanup(patch_input.stop)

        # Now, eventually mock the stdout to be able to check the result.
        self.output = io.StringIO()
        self.patch_output = mock.patch('sys.stdout', new=self.output)
        self.patch_output.start()
        self.addCleanup(self.patch_output.stop)

    def tearDown(self):
        if os.environ.get('DEBUG') and os.environ['DEBUG'] == '1':
            self.patch_output.stop()
            print(self.output.getvalue())

    def test_player_wins(self):
        """ This test follows the scenario :
            - the player is named TheInvisibleMan
            - the difficulty is easy so only 2 rounds for the game
            - first round, the dice returns 2 so the player is not spotted
            - then the player moves to the next round
            - second round, the dice returns 4, no fight again.
            - then the player moves again.
            - eventually, the player wins.
        """
        # we are only spotted if the dice number is odd ;-)
        self.fake_app.loaded_dices = [2, 4]

        self.mock_input.side_effect = [
            # Name of the player
            'TheInvisibleMan',
            # No fight, we just need to move
            'M',
            # No fight again, we just have to make the last move to win.
            'M'
            # Eventually, we win.
        ]
        main.run_game('easy')
        self.assertIn('Congratulations. You won !', self.output.getvalue())

    def test_player_looses_with_a_complicated_scenario(self):
        """ This test follows the scenario :
            - the player is named PoorLonesomeCowboy
            - the player has 100XP and a strength of 1
            - the difficulty is medium so only 5 rounds for the game
            - first round, the dice returns 3 so a monster sees the player
            - the player wants to flee
            - the dice returns 12 so the player can flee
            - then the player moves to the next round
            - second round, the dice returns 3, another monster finds the player
            - the player fights the easiest monster that only has 10XP/str:3
            - the dice returns 6 so the player hits 6XP for the first monster
            - the dice returns 10 so the monster hits 30XP (10x3) the player
            (player has a health of 70XP)
            - the dice returns 6 so the player kills the monster.
            - the player decides to rest
            - the dice returns 10 so the player gains 10XP and no extra round
            (player has a health of 80XP)
            - the player decides to move
            - third round, the dice returns 5, a third monster spots the player
            (100XP, str:3)
            - the player wants to flee
            - the dice returns 1, so the player fails to flee
            - the monster then attacks first
            - the dice returns 12, so the monster takes 36 XP to the player
            - the dice returns 1, the player takes 1XP to the monster
            - the dice returns 12, so the monster takes again 36XP
            - the dice returns 1, the player takes 1XP to the monster
            - the dice returns 12, the monster takes yet again 36XP.
            - the player dies.
        """

        self.mock_input.side_effect = [
            # Name of the player
            'PoorLonesomeCowboy',
            # Spotted by a monster, we want to flee
            'F',
            # We escaped, we can move
            'M',
            # Another monster spotted us, we decide to fight
            'A',
            # We got hurt, we decide to rest
            'R',
            # We then move
            'M',
            # we try to flee
            'F',
            # eventually we die.
        ]

        self.fake_app.loaded_dices = [3, 12, 3, 6, 10, 6, 10, 5, 1, 12, 1, 12,
                                      1, 12]

        monsters_to_fight = [
            # As a reminder, the order counts
            {
                "name": "monster1",
                "health": 100,
                "strength": 1,
                "icon": '🧟',
            },
            {
                "name": "monster2",
                "health": 10,
                "strength": 3,
                "icon": '🧟',
            },
            {
                "name": "monster3",
                "health": 100,
                "strength": 3,
                "icon": '🧟',
            },
        ]
        self.fake_app.monsters = monsters_to_fight
        main.run_game('medium')
        self.assertIn("You're dead.", self.output.getvalue())
