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

import json
import unittest
from unittest import mock

import requests

from rolegame import client


class TestClient(unittest.TestCase):

    @mock.patch('requests.get')
    def test_init(self, mock_get):
        client.Client()
        mock_get.assert_called_once_with('http://localhost:5000/')

    @mock.patch('requests.get')
    def test_init_fails(self, mock_get):
        # This is how we raise an exception by the mock call
        mock_get.side_effect = requests.ConnectionError
        self.assertRaises(Exception, client.Client)
        mock_get.assert_called_once_with('http://localhost:5000/')


@mock.patch.object(requests, 'get')
class TestClientDiceOnly(unittest.TestCase):

    def setUp(self):
        self.fake_dice_api_result = mock.Mock(text=json.dumps({'score': 9}))
        # note that setUp runs before patch()
        self.assertRaises(Exception, client.Client)

    def test_get_dice_works_fine(self, mock_get):
        the_client = client.Client()
        mock_get.return_value = self.fake_dice_api_result
        dice = the_client.get_dice()
        self.assertEqual(9, dice)
        # yeah, we have two calls to the API, one for getting the client and
        # the other one for getting the dice result.
        mock_get.assert_has_calls(
            [mock.call('http://localhost:5000/'),
             mock.call('http://localhost:5000/dice')]
        )

    def test_get_dice_fails(self, mock_get):
        the_client = client.Client()
        mock_get.return_value = mock.Mock(text='boom')
        self.assertRaises(Exception, the_client.get_dice)

    def _fake_get(self, url):
        if url.endswith('/dice'):
            # this is a dice API resource call
            response = {'score': 9}
        elif url.endswith('/monster'):
            # this is a monster API endpoint call
            response = {
               "name": "pity",
               "health": 100,
               "strength": 1,
               "icon": "🐍",}
        else:
            # this can be a connection check or whatever else
            response = {}
        return mock.Mock(text=json.dumps(response))

    def test_get_monster(self, mock_get):
        mock_get.side_effect = self._fake_get
        the_client = client.Client()
        expected = {"name": "pity", "health": 100, "strength": 1, "icon": "🐍",}
        self.assertEqual(expected, the_client.get_monster())
        # crazypants and useless assertion but just for the demo need...
        self.assertEqual(mock.call('http://localhost:5000/monster'),
                         mock_get.mock_calls[1])
        # ... because actually we can just verify one call
        mock_get.assert_any_call('http://localhost:5000/monster')