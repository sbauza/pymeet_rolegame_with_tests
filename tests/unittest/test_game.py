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
import unittest
from unittest import mock

from rolegame import game
from tests.unittest import fake


# We use new_callable to return a StringIO instead of a MagicMock
@mock.patch('sys.stdout', new_callable=io.StringIO)
class TestGameDisplayPosition(unittest.TestCase):

    def setUp(self):
        # This is just a sentinel object
        player = mock.sentinel.Player
        # and yet another sentinel which is nested
        player.icon = mock.sentinel.icon
        with mock.patch.object(game.client, 'Client'):
            self.fake_game = game.Game(player)

    @mock.patch.object(game.Game, 'is_over')
    def test_display_position_won(self, mock_is_over, mock_stdout):
        mock_is_over.return_value = True
        self.fake_game.display_position()
        # as print returns a newline, let's just check with assertIn
        # thanks to StringIO, we can lookup the stream with getvalue()
        self.assertIn("You got the 💰", mock_stdout.getvalue())

    @mock.patch.object(game.Game, 'is_over')
    def test_display_position_notwonyet(self, mock_is_over, mock_stdout):
        mock_is_over.return_value = False
        # set the values of the game to make the test independent
        self.fake_game.rounds = 3
        self.fake_game.position = 0
        self.fake_game.display_position()
        self.assertIn(f'{mock.sentinel.icon}__💰', mock_stdout.getvalue())


class TestGameSpotted(unittest.TestCase):

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


class TestGamePropertyMock(unittest.TestCase):

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


class TestGame(unittest.TestCase):

    def setUp(self):
        # Don't patch where it's defined, rather patch where it's called !
        self.patcher_client = mock.patch.object(game, 'client', autospec=True)
        self.mock_client = self.patcher_client.start()
        # Always prefer addCleanup for stopping the patch
        self.addCleanup(self.patcher_client.stop)

        self.fake_game = game.Game(mock.sentinel.player)

    # def tearDown(self):
    #     # Don't do it, this is errorprone if the test returns an exception.
    #     self.patcher_client.stop()

    def test_get_monster_one_possibility(self):
        with mock.patch.object(game.character, 'Monster',
                               # here we duck-type with a fake object
                               new=fake.FakeIndependentMonster):
            monster = self.fake_game.get_monster()
        self.assertEqual(fake.FakeIndependentMonster.type, monster.type)
        self.assertEqual(fake.FakeIndependentMonster.name, monster.name)
        self.assertEqual(fake.FakeIndependentMonster.strength, monster.strength)
        self.assertEqual(str(fake.FakeIndependentMonster.health),
                         str(monster.health))

    def test_get_monster_another_possibility(self):
        # we need to mock the Client() instance hence the first return_value
        self.mock_client.Client.return_value.get_monster.return_value = (
            fake.fake_monster_dict
        )
        monster = self.fake_game.get_monster()
        self.assertEqual(game.character.Monster.type, monster.type)
        self.assertEqual(fake.fake_monster_dict['name'], monster.name)
        self.assertEqual(fake.fake_monster_dict['strength'], monster.strength)
        self.assertEqual(str(fake.fake_monster_dict['health']),
                         str(monster.health))

    def test_get_monster_with_a_fixture(self):
        # TODO(sbauza)
        pass

    def test_fight_player_wins(self):
        # Just a placeholder for contributors who want to try writing ;-)
        pass

    def test_fight_monster_wins(self):
        # Just a placeholder for contributors who want to try writing ;-)
        pass

    def test_flee_successful(self):
        # Just a placeholder for contributors who want to try writing ;-)
        pass

    def test_flee_fails(self):
        # Just a placeholder for contributors who want to try writing ;-)
        pass

    def test_rest_with_multiple_conditions(self):
        # Just a placeholder for contributors who want to try writing ;-)
        pass
