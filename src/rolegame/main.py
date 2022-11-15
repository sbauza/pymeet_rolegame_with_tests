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


from rolegame import character
from rolegame import game


def main():
    name = input("Enter your hero name: ")
    player = character.Player(name)
    mygame = game.Game(player, rounds=4)

    print("Here are your player initial stats:")
    player.display_characteristics()
    # Do the fucking loop
    while not mygame.is_over():
        mygame.display_position()
        if mygame.spotted:
            choice = input("[F]lee or [A]ttack ? [F,A]: ")
            fled = False
            if choice.lower() == 'f':
                fled = mygame.flee()
            if choice.lower() != 'f' or not fled:
                mygame.fight()
                player.display_characteristics()
        if player.dead:
            print("You're dead.")
            break
        choice = input("[R]est or [M]ove ? [R, M]: ")
        if choice.lower() == 'r':
            mygame.rest()
        else:
            mygame.move()
        print("\n\n")
    else:
        mygame.display_position()
        print("Congratulations. You won !")

if __name__ == "__main__":
    main()
