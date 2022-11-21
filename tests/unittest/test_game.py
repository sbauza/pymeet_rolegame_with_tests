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

import unittest
from unittest import mock

from rolegame import game
from tests.unittest import fake


class TestGameSpotted(unittest.TestCase):

    def setUp(self):
        self.patcher_client = mock.patch('rolegame.client')
        self.mock_client = self.patcher_client.start()

    def tearDown(self):
        self.patcher_client.stop()

    def test_old_spotted_implementation(self):
        # let's pretend the client was having an old API named 'get_card'
        # and that the spotted property was using it, so you wrote this test.
        with mock.patch.object(game, 'client') as mock_client_notspecced:
            mock_client_notspecced.Client.get_card.return_value = 'pikachu'
            # in the old implementation, you were verifying that pikachu wasn't
            # spotting you.
            self.assertFalse(game.Game('1997_player').spotted)
        # Now, the problem is that the test is still happy while it should raise
        # some exception as we no longer use 'get_card' in 'spotted' method.

        # Now, create a new mock that has a Client spec and do the same test.
        with mock.patch.object(game, 'client', autospec=True) as mock_client:
            try:
                mock_client.Client.get_card.return_value = 'pikachu'
                self.assertFalse(game.Game('1997_player').spotted)
            except AttributeError:
                # Now the test is failing, which is normal as we removed the
                # call
                pass
        # You can see the difference between the mocks
        print(mock_client_notspecced.Client)
        print(mock_client.Client)


class TestGame(unittest.TestCase):

    def setUp(self):
        self.patcher_client = mock.patch('rolegame.client', autospec=True)
        self.mock_client = self.patcher_client.start()
        self.addCleanup(self.patcher_client.stop)

    def test_difficulty_easy(self):
        # verify the default values for the two class attributes
        self.assertEqual(5, game.Game.rounds)
        self.assertEqual(9, game.Game.fled_dice_success_min)
        # here there is a trap with classmethods changing attributes
        # let's use a PropertyMock for one of two attributes
        with mock.patch('rolegame.game.Game.rounds',
                        new_callable=mock.PropertyMock):
            game.Game.difficulty('easy')
            self.assertEqual(2, game.Game.rounds)
            self.assertEqual(1, game.Game.fled_dice_success_min)
        # fortunately, the attribute value is back the previous default
        self.assertEqual(5, game.Game.rounds)
        try:
            # but not the other attribute
            self.assertEqual(9, game.Game.fled_dice_success_min)
        except AssertionError:
            # so, let's revert it to the default since we messed up
            game.Game.fled_dice_success_min = 9


class TestGame2(unittest.TestCase):

    def setUp(self):
        # Don't patch where it's defined, rather patch where it's called !
        self.patcher_client = mock.patch.object(game, 'client', autospec=True)
        self.mock_client = self.patcher_client.start()
        # Always prefer addCleanup for stopping the patch
        self.addCleanup(self.patcher_client.stop)

    # def tearDown(self):
    #     # Don't do it, this is errorprone if the test returns an exception.
    #     self.patcher_client.stop()

    def test_get_monster_one_possibility(self):
        fake_game = game.Game('test')
        with mock.patch.object(game.character, 'Monster',
                               # here we duck-type with a fake object
                               new=fake.FakeIndependentMonster):
            monster = fake_game.get_monster()
        self.assertEqual(fake.FakeIndependentMonster.type, monster.type)
        self.assertEqual(fake.FakeIndependentMonster.name, monster.name)
        self.assertEqual(fake.FakeIndependentMonster.strength, monster.strength)
        self.assertEqual(str(fake.FakeIndependentMonster.health),
                         str(monster.health))

    def test_get_monster_another_possibility(self):
        fake_game = game.Game('test')
        # we need to mock the Client() instance hence the first return_value
        self.mock_client.Client.return_value.get_monster.return_value = (
            fake.fake_monster_dict
        )
        monster = fake_game.get_monster()
        self.assertEqual(fake.FakeIndependentMonster.type, monster.type)
        self.assertEqual(fake.FakeIndependentMonster.name, monster.name)
        self.assertEqual(fake.FakeIndependentMonster.strength, monster.strength)
        self.assertEqual(str(fake.FakeIndependentMonster.health),
                         str(monster.health))
