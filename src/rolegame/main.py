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

import argparse

from rolegame import character
from rolegame import game


def run_game(difficulty: str = 'medium'):
    print("⚔️ ⚔️ ⚔️ ⚔️ ⚔️  Welcome into the *Q*uest "
          "*T*o *T*he *F*ake *O*bject  ⚔️ ⚔️ ⚔️ ⚔️ ⚔️\n\n")
    player = character.Player.newPlayer()
    print("Here are your player initial stats:")
    player.display_characteristics()

    mygame = game.Game(player)
    game.Game.difficulty(difficulty)

    # Do the fucking loop
    while not mygame.is_over():
        mygame.display_position()
        if mygame.spotted:
            monster = mygame.get_monster()
            choice = input("[F]lee or [A]ttack ? [F,A]: ")
            fled = False
            if choice.lower() == 'f':
                fled = mygame.flee()
            if choice.lower() != 'f' or not fled:
                mygame.fight(monster)
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


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-d", "--difficulty",
                        choices=['easy', 'medium', 'hard'],
                        help='Set the difficulty of the game')
    args = parser.parse_args()
    difficulty = args.difficulty if args.difficulty else 'medium'
    run_game(difficulty)


if __name__ == "__main__":
    main()
