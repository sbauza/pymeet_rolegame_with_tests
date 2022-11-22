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
import pytest
from rolegame import main
from rolegame import client
from rolegame import character


@pytest.fixture
def player_inputs(monkeypatch):

    inputs = iter(["A", "M",
                   "A", "M",
                   "A", "M",
                   "A", "M",
                   "A", "M"
                   ])

    monkeypatch.setattr("builtins.input", lambda _: next(inputs))

    yield


@pytest.fixture
def external_service(monkeypatch):
    # dice sequence [spot, player, enemy, player...]
    # pity is killed with the second attack
    dices = iter([1, 12, 1, 12,
                  1, 12, 1, 12,
                  1, 12, 1, 12,
                  1, 12, 1, 12,
                  1, 12, 1, 12,
                  ])

    def fake_monster(name):
        content = {
            "name": name,
            "health": 24,
            "strength": 1,
            "icon": "🐍",
        }
        return content

    # Use the fixture instead otherwise you will have to undo mocks.
    monkeypatch.setattr(client.Client, "__init__", lambda _: None)
    monkeypatch.setattr(client.Client, "get_dice", lambda _: next(dices))
    monkeypatch.setattr(
        client.Client, "get_monster", lambda _: fake_monster("pity"))

    yield


class TestFullGame:
    def test_winning_game(
            self, monkeypatch, player_inputs, external_service, capsys
    ):
        player = character.Player('Uggla')
        player.strength = 1

        def uggla():
            return player

        monkeypatch.setattr(character.Player, "newPlayer", uggla)
        main.run_game()
        captured = capsys.readouterr()
        captured_lines = captured.out.split("\n")
        assert player.dead == 0
        assert captured_lines[-2] == "Congratulations. You won !"

    def test_lost_game(
            self, monkeypatch, player_inputs, external_service, capsys
    ):
        player = character.Player('Uggla')
        player.strength = 1
        # We should die after 3 attacks from pity
        player.health = character.Health(3)

        def uggla():
            return player

        monkeypatch.setattr(character.Player, "newPlayer", uggla)
        main.run_game()
        captured = capsys.readouterr()
        captured_lines = captured.out.split("\n")
        assert player.dead == 1
        assert captured_lines[-2] == "You're dead."
