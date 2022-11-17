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

import os
import unittest
from unittest import mock


from rolegame import character


class TestHealth(unittest.TestCase):
    def test_health_init(self):
        health = character.Health()
        self.assertEqual(100, health.gauge)
        
        # we cap the health at 100
        health = character.Health(200)
        self.assertEqual(100, health.gauge)
        
        health = character.Health(50)
        self.assertEqual(50, health.gauge)
        
    def test_health_maths(self):
        health = character.Health(30)
        # just a doublecheck
        assert 30 == health.gauge
        new_health = health + 50
        self.assertIsInstance(new_health, character.Health)
        self.assertEqual(80, new_health.gauge)
        # let's do quick maths
        new_health = new_health + 30
        # we cap at 100 the max
        self.assertEqual(100, new_health.gauge)
        new_health = new_health - 120
        # we cap at 0 the min
        self.assertEqual(0, new_health.gauge)

        self.assertEqual(character.Health(0), new_health)
        self.assertTrue(new_health.dead)
        self.assertEqual('0', str(new_health))


class TestPlayer(unittest.TestCase):
    
    @unittest.skipIf(int(os.getenv('I_KNOW_WHAT_I_DO', 0)) < 1,
                     'test skipped automatically')
    def test_newPlayer_dummy(self):
        player = character.Player.newPlayer()
        self.assertIsInstance(player, character.Player)
        # you should somehow expect something, right?
        self.assertEqual("foo", player.name)
    
    def test_newPlayer_next_try(self):
        mocked_input = mock.Mock()
        mocked_input.return_value = 'foo'
        # This is a special case for mocking input()
        mock.builtins.input = mocked_input
        player = character.Player.newPlayer()
        self.assertIsInstance(player, character.Player)
        self.assertEqual("foo", player.name)
        
    def test_newPlayer_the_good_way(self):
        with mock.patch('builtins.input') as mocked_input:
            mocked_input.return_value = 'foo'
            player = character.Player.newPlayer()
        self.assertEqual('foo', player.name)
        mocked_input.assert_called_once()


class TestHealthAgain(unittest.TestCase):
    def test_eq_with_magicmock(self):
        health = character.Health(50)
        mocked_health = mock.Mock(gauge=50)
        self.assertTrue(mocked_health == health)
        try:
            mocked_health.__eq__.assert_called_once_with(health)
        except AttributeError:
            # doh, you can't because you need to redefine __eq__ too
            print(mocked_health.__eq__)
        mocked_health = mock.MagicMock(gauge=50)
        self.assertTrue(mocked_health == health)
        mocked_health.__eq__.assert_called_once_with(health)
        print(mocked_health.__eq__)
