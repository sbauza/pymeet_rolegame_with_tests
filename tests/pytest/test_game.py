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
from rolegame import game
from rolegame import client
from rolegame import character


class TestGame():
    def test_display_position(self, monkeypatch, capsys):
        # Mock the __init__ method of client to avoid the connection check
        monkeypatch.setattr(client.Client, "__init__", lambda _: None)


        # Is it a UT or a IT ? Border becomes foggy
        hero = character.Player("Uggla")
        mygame = game.Game(hero)
        mygame.rounds = 2
        mygame.display_position()
        captured = capsys.readouterr()
        assert captured.out == "🧝_💰\n"
        mygame.rounds = 5
        mygame.display_position()
        captured = capsys.readouterr()
        assert captured.out == "🧝____💰\n"
        mygame.position = 5
        mygame.display_position()
        captured = capsys.readouterr()
        assert captured.out == "You got the 💰\n"

    def test_spotted(self, monkeypatch):
        # Mock the __init__ method of client to avoid the connection check
        monkeypatch.setattr(client.Client, "__init__", lambda _: None)
        monkeypatch.setattr(client.Client, "get_dice", lambda _: 3)


        # Is it a UT or a IT ? Border becomes foggy
        hero = character.Player("Uggla")
        mygame = game.Game(hero)
        output = mygame.spotted
        assert output == True

        monkeypatch.setattr(client.Client, "get_dice", lambda _: 6)
        output = mygame.spotted
        assert output == False

    def test_rest(self, monkeypatch, capsys):
        # Mock the __init__ method of client to avoid the connection check
        monkeypatch.setattr(client.Client, "__init__", lambda _: None)
        monkeypatch.setattr(client.Client, "get_dice", lambda _: 3)


        # Is it a UT or a IT ? Border becomes foggy
        hero = character.Player("Uggla")
        mygame = game.Game(hero)
        mygame.rounds = 5
        mygame.player.health = 50
        mygame.rest()
        captured = capsys.readouterr()
        captured_lines = captured.out.split("\n")
        assert captured_lines[0] == "💤 You decide to take some rest: "
        assert captured_lines[1] == "You're fortunate to gain 33 XPs"
        assert captured_lines[-2] == "... but it takes 2 more rounds."
        assert mygame.rounds == 7
        assert mygame.player.health == 50 + 33

        monkeypatch.setattr(client.Client, "get_dice", lambda _: 12)
        mygame.rest()
        captured = capsys.readouterr()
        captured_lines = captured.out.split("\n")
        assert captured_lines[0] == "💤 You decide to take some rest: "
        assert captured_lines[1] == "You're fortunate to gain 8 XPs"
        assert mygame.rounds == 7
        assert mygame.player.health == 50 + 33 + 8
