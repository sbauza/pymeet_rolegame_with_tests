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

import requests

from rolegame import client


class TestClient(unittest.TestCase):

    @mock.patch('requests.get')
    def test_init(self, mock_get):
        client.Client()
        mock_get.assert_called_once_with('http://localhost:5000/')

    @mock.patch('requests.get')
    def test_init_fails(self, mock_get):
        mock_get.side_effect = requests.ConnectionError
        self.assertRaises(Exception, client.Client)
        mock_get.assert_called_once_with('http://localhost:5000/')


#Test fails exception sur le client