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

import requests
import pytest

from rolegame import client


class MockResponse:

    # mock json() method always returns a specific testing dictionary
    @staticmethod
    def json():
        return {"Status": "Ok"}


class TestClient():

    def test_init(self, monkeypatch):
        # Mock the requests.get method always returning True despite we
        # don't care about what is returned in this case
        monkeypatch.setattr(requests, "get", lambda _: True)
        client.Client()

    def test_init_fails(self):
        # This is how we raise an exception with pytest
        with pytest.raises(Exception):
            client.Client()


class TestClientDiceOnly():
    def test_get_dice_works_fine(self, monkeypatch):
        def mock_request_for_fake_dice():
            resp = requests.Response()
            resp.status_code = 200
            resp._content = b'{ "score" : 12 }'
            return resp
        # Mock the __init__ method of client to avoid the connection check
        monkeypatch.setattr(client.Client, "__init__", lambda _: None)
        # Mock request.get for get_dice method returning a request.Response
        # object containing an expected json.
        monkeypatch.setattr(
            requests, "get", lambda fake_url: mock_request_for_fake_dice())

        cl = client.Client()
        dice = cl.get_dice()
        assert dice == 12


@pytest.fixture
def mock_monster_rest_api():
    def fake_monster(name):
        resp = requests.Response()
        resp.status_code = 200
        content = "".join(
            [
                '{"name": "',
                  name,
                  '", "health": 100, "strength": 1, "icon": "🐍"}'
            ]
        )
        resp._content = content.encode()
        return resp

    def mock(name):
        mock = pytest.MonkeyPatch()
        mock.setattr(requests, "get", lambda _: fake_monster(name))

    return mock


class TestClientMonster():
    # We use the above fixture here ---------------------v
    def test_get_monster(self, monkeypatch, mock_monster_rest_api):
        # Mock the __init__ method of client to avoid the connection check
        monkeypatch.setattr(client.Client, "__init__", lambda _: None)

        # Use the fixture to mock different monsters
        mock_monster_rest_api("pity")
        cl = client.Client()
        monster = cl.get_monster()
        assert monster == (
            {"name": "pity", "health": 100, "strength": 1, "icon": "🐍"}
        )

        mock_monster_rest_api("spider")
        monster = cl.get_monster()
        assert monster == (
            {"name": "spider", "health": 100, "strength": 1, "icon": "🐍"}
        )

        # Next one is a little 🤯
        with pytest.raises(AssertionError):
            assert monster == (
                {"name": "pity", "health": 100, "strength": 1, "icon": "🐍"}
            )