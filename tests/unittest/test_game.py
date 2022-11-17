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

from rolegame import game


class TestGameSpotted(unittest.TestCase):

    def setUp(self):
        self.patcher_client = mock.patch('rolegame.client')
        self.mock_client = self.patcher_client.start()

    def tearDown(self):
        self.patcher_client.stop()

    def test_old_spotted_implementation(self):
        # let's pretend the client was having an old API named 'get_card'
        # and that the spotted property was using it, so you wrote this test.
        with mock.patch.object(game, 'client') as mock_client_notspecced:
            mock_client_notspecced.Client.get_card.return_value = 'pikachu'
            # in the old implementation, you were verifying that pikachu wasn't
            # spotting you.
            self.assertFalse(game.Game('1995_player').spotted)
        # Now, the problem is that the test is still happy while it should raise
        # some exception as we no longer use 'get_card' in 'spotted' method.

        # Now, create a new mock that has a Client spec and do the same test.
        with mock.patch.object(game, 'client', autospec=True) as mock_client:
            try:
                mock_client.Client.get_card.return_value = 'pikachu'
                self.assertFalse(game.Game('1995_player').spotted)
            except AttributeError:
                # Now the test is failing, which is normal as we removed the
                # call
                pass
        # You can see the difference between the mocks
        print(mock_client_notspecced.Client)
        print(mock_client.Client)


class TestGame(unittest.TestCase):

    def setUp(self):
        self.patcher_client = mock.patch('rolegame.client', autospec=True)
        self.mock_client = self.patcher_client.start()
        self.addCleanup(self.patcher_client.stop)

    def test_e(self):
        pass
