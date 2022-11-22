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

from rolegame import main


# As a reminder, this is NOT an integration test, rather a whitebox
# test.
class TestMain(unittest.TestCase):

    @mock.patch('builtins.input')
    @mock.patch.object(main.game, 'Game', autospec=True)
    @mock.patch.object(main.character.Player, 'newPlayer')
    def test_main_successful(self, mock_newplayer, mock_game, mock_input):
        fake_player = mock.Mock(spec=main.character.Player)
        mock_newplayer.return_value = fake_player
        fake_game = mock_game.return_value

        fake_game.is_over.side_effect = (False, True)
        # That's unfortunately how you attach a PropertyMock as a Mock attribute
        # See https://docs.python.org/3/library/unittest.mock.html#unittest.mock.PropertyMock  # noqa: E501
        mock_spotted = mock.PropertyMock(return_value=False)
        type(fake_game).spotted = mock_spotted
        mock_dead = mock.PropertyMock(return_value=False)
        type(fake_player).dead = mock_dead

        mock_input.return_value = 'm'
        main.run_game()

        mock_newplayer.assert_called_once_with()
        mock_game.assert_called_once_with(fake_player)
        fake_game.is_over.assert_has_calls([mock.call(), mock.call()])
        mock_spotted.assert_called_once_with()
        mock_dead.assert_called_once_with()
        mock_input.assert_called_once_with("[R]est or [M]ove ? [R, M]: ")

    @mock.patch('builtins.input')
    @mock.patch.object(main.game, 'Game', autospec=True)
    @mock.patch.object(main.character.Player, 'newPlayer')
    def test_main_dead(self, mock_newplayer, mock_game, mock_input):
        fake_player = mock.Mock(spec=main.character.Player)
        mock_newplayer.return_value = fake_player
        fake_game = mock_game.return_value
        fake_game.is_over.return_value = False

        mock_spotted = mock.PropertyMock(return_value=True)
        type(fake_game).spotted = mock_spotted
        mock_input.return_value = 'a'
        mock_dead = mock.PropertyMock(return_value=True)
        type(fake_player).dead = mock_dead

        main.run_game()

        mock_newplayer.assert_called_once_with()
        mock_game.assert_called_once_with(fake_player)
        fake_game.is_over.assert_called_once_with()
        mock_spotted.assert_called_once_with()
        mock_dead.assert_called_once_with()
        mock_input.assert_called_once_with("[F]lee or [A]ttack ? [F, A]: ")
