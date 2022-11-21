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
import pytest

from rolegame import character


class TestHealth:
    def test_health_init(self):
        health = character.Health()
        assert 100 == health.gauge

        # we cap the health at 100
        health = character.Health(200)
        assert 100 == health.gauge

        health = character.Health(50)
        assert 50 == health.gauge

    def test_health_maths(self):
        health = character.Health(30)
        # just a doublecheck
        assert 30 == health.gauge
        new_health = health + 50
        assert isinstance(new_health, character.Health)
        assert 80 == new_health.gauge
        # let's do quick maths
        new_health = new_health + 30
        # we cap at 100 the max
        assert 100 == new_health.gauge
        new_health = new_health - 120
        # we cap at 0 the min
        assert 0 == new_health.gauge

        assert character.Health(0) == new_health
        assert new_health.dead
        assert '0' == str(new_health)


class TestPlayer:

    @pytest.mark.skipif(
        int(os.getenv('I_KNOW_WHAT_I_DO', 0)) < 1,
        reason="test skipped automatically"
    )
    def test_newPlayer_dummy(self):
        player = character.Player.newPlayer()
        assert isinstance(player, character.Player)
        # you should somehow expect something, right?
        assert "foo" == player.name

    def test_newPlayer_next_try(self):
        mocked_input = pytest.MonkeyPatch()
        #  setattr(target: object, --> object and name can be grouped in a str
        #          name: str,          look at sources to show the "trick"
        #          value: object,  --> ⚠️  need a callable object with
        #                                 one argument in that case
        #                                 because we "swap":
        #                                 name = input("Enter your hero name:")
        #                                                 ^- arg1
        #          raising: bool = True) → None
        mocked_input.setattr("builtins.input", lambda _: "foo")
        player = character.Player.newPlayer()
        assert isinstance(player, character.Player)
        assert "foo" == player.name

    def test_newPlayer_the_good_way(self):
        with pytest.MonkeyPatch().context() as mocked_input:
            mocked_input.setattr("builtins.input", lambda _: "foo")
            player = character.Player.newPlayer()
        assert 'foo' == player.name
        # mocked_input.assert_called_once()  <-- this can not be done with
        #                                        "native" pytest
        #                                        we can either use
        #                                        unittest.mock or pytest-mock
        #                                        plugin (see next test)

    # pytest-mock is a unittest.mock wrapper
    # and comes as a pytest fixture.
    # fixtures can be used as test function parameters
    #                                        |
    #                                        v
    def test_newPlayer_the_good_way_2(self, mocker):
        mock = mocker.patch("builtins.input")
        mock.return_value = "foo"
        player = character.Player.newPlayer()
        mocker.stop(mock)

        mock.assert_called_once()
        assert isinstance(player, character.Player)
        assert "foo" == player.name
