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
import sys

import requests
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


# Do not do that
@pytest.fixture
def mock_monster_rest_api_bad():

    def mock(name):
        # Use the fixture instead otherwise you will have to undo mocks.
        mock = pytest.MonkeyPatch()
        mock.setattr(requests, "get", lambda _: fake_monster(name))
        return mock

    yield mock
    print("Clean fixture")


class TestClientMonsterBad():
    # We use the above fixture here ---------------------v
    def test_get_monster(self, monkeypatch, mock_monster_rest_api_bad):
        # Mock the __init__ method of client to avoid the connection check
        monkeypatch.setattr(client.Client, "__init__", lambda _: None)

        # Use the fixture to mock different monsters
        m1 = mock_monster_rest_api_bad("pity")
        cl = client.Client()
        monster = cl.get_monster()
        assert monster == (
            {"name": "pity", "health": 100, "strength": 1, "icon": "🐍"}
        )
        # Undo needed to not leak mock to other tests
        m1.undo()

        m2 = mock_monster_rest_api_bad("spider")
        monster = cl.get_monster()
        assert monster == (
            {"name": "spider", "health": 100, "strength": 1, "icon": "🐍"}
        )

        # Next one is a little 🤯
        with pytest.raises(AssertionError):
            assert monster == (
                {"name": "pity", "health": 100, "strength": 1, "icon": "🐍"}
            )
        # Undo needed to not leak mock
        m2.undo()


# Do that
@pytest.fixture
def mock_monster_rest_api_good(monkeypatch):

    def mock(name):
        # Use the fixture instead otherwise you will have to undo mocks.
        monkeypatch.setattr(requests, "get", lambda _: fake_monster(name))

    yield mock
    print("Clean fixture")


class TestClientMonsterGood():
    # We use the above fixture here ---------------------v
    def test_get_monster(self, monkeypatch, mock_monster_rest_api_good):
        # Mock the __init__ method of client to avoid the connection check
        monkeypatch.setattr(client.Client, "__init__", lambda _: None)

        # Use the fixture to mock different monsters
        mock_monster_rest_api_good("pity")
        cl = client.Client()
        monster = cl.get_monster()
        assert monster == (
            {"name": "pity", "health": 100, "strength": 1, "icon": "🐍"}
        )

        mock_monster_rest_api_good("spider")
        monster = cl.get_monster()
        assert monster == (
            {"name": "spider", "health": 100, "strength": 1, "icon": "🐍"}
        )

        # Next one is a little 🤯
        with pytest.raises(AssertionError):
            assert monster == (
                {"name": "pity", "health": 100, "strength": 1, "icon": "🐍"}
            )


# Or
@pytest.fixture()
def mock_monster_rest_api_mark(request, monkeypatch):

    marker = request.node.get_closest_marker("monster_name")
    monkeypatch.setattr(requests, "get", lambda _: fake_monster(marker.args[0]))
    yield
    print("Clean fixture")

class TestClientMonsterMarker():
    # Use a marker
    @pytest.mark.monster_name("pity")
    def test_get_monster_pity(self, monkeypatch, mock_monster_rest_api_mark):
        # Mock the __init__ method of client to avoid the connection check
        monkeypatch.setattr(client.Client, "__init__", lambda _: None)

        # Use the fixture to mock different monsters
        cl = client.Client()
        monster = cl.get_monster()
        assert monster == (
            {"name": "pity", "health": 100, "strength": 1, "icon": "🐍"}
        )

    @pytest.mark.monster_name("spider")
    def test_get_monster_spider(self, monkeypatch, mock_monster_rest_api_mark):
        # Mock the __init__ method of client to avoid the connection check
        monkeypatch.setattr(client.Client, "__init__", lambda _: None)

        # Use the fixture to mock different monsters
        cl = client.Client()
        monster = cl.get_monster()
        assert monster == (
            {"name": "spider", "health": 100, "strength": 1, "icon": "🐍"}
        )


# Or with parameters
@pytest.fixture(params=["pity", "spider"])
def mock_monster_rest_api_param(request, monkeypatch):

    monkeypatch.setattr(requests, "get", lambda _: fake_monster(request.param))
    # yield the value to check
    yield request.param
    print("Clean fixture")

class TestClientMonsterParam():
    # We use the above fixture here ---------------------v
    def test_get_monsters(self, monkeypatch, mock_monster_rest_api_param):
        # Mock the __init__ method of client to avoid the connection check
        monkeypatch.setattr(client.Client, "__init__", lambda _: None)

        # Use the fixture to mock different monsters
        cl = client.Client()
        monster = cl.get_monster()
        if mock_monster_rest_api_param == "pity":
            assert monster == (
                {"name": "pity", "health": 100, "strength": 1, "icon": "🐍"}
            )
        else:
            assert monster == (
                {"name": "spider", "health": 100, "strength": 1, "icon": "🐍"}
            )


# Or more powerful using the requests-mock module
class TestClientMonsterRequestsMock():
    # We use the request_mock fixture here --------v
    def test_get_monster(self, monkeypatch, requests_mock):
        # Mock the __init__ method of client to avoid the connection check
        monkeypatch.setattr(client.Client, "__init__", lambda _: None)

        # Here we use requests_mock which allows to mock on sharp requests
        # You can defined matching on url, path, regexp
        # It can easily manage responses, headers...
        requests_mock.get(
            'http://localhost:5000/monster', json=fake_monster("pity").json()
        )

        cl = client.Client()
        monster = cl.get_monster()
        assert monster == (
            {"name": "pity", "health": 100, "strength": 1, "icon": "🐍"}
        )
