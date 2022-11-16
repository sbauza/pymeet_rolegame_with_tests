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

import json
import typing

import requests

ROOT_URL = 'http://localhost:5000'

class Client(object):
    
    def __init__(self) -> None:
        try:
            requests.get(ROOT_URL + '/')
        except requests.ConnectionError:
            raise Exception("Can't access " + ROOT_URL)

    def get_dice(self) -> int:
        result = requests.get(ROOT_URL + '/dice')
        if result:
            try:
                content = json.loads(result.text)
            except json.JSONDecodeError:
                raise Exception("Can't read content of " + ROOT_URL + '/dice') 
            score = content.get('score')
            return score
        else:
            raise Exception("Can't access " + ROOT_URL)
    
    def get_monster(self) -> typing.Dict:
        result = requests.get(ROOT_URL + '/monster')
        if result:
            try:
                content = json.loads(result.text)
            except json.JSONDecodeError:
                raise Exception(
                    "Can't read content of " + ROOT_URL + '/monster') 
            return content
        else:
            raise Exception("Can't access " + ROOT_URL)
