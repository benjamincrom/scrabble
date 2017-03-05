**Table of Contents**

- [Scrabble](#scrabble)
    - [Installing from pypi](#installing-from-pypi)
    - [Installing from source](#installing-from-source)
    - [Testing](#testing)
    - [Recover Scrabble Game](#recover-scrabble-game)
    - [Play Scrabble Game](#play-scrabble-game)
        - [Create a new Scrabble game object](#create-a-new-scrabble-game-object)
        - [Make Move](#make-move)
        - [Find Best Move (Brute Force)](#find-best-move-brute-force)
        - [Exchange Tiles](#exchange-tiles)
        - [Conclude Game](#conclude-game)

# Scrabble
This package implements the game of Scrabble and also adds features that
recover previous moves as well as determine the best next move for a given
Scrabble game.

## Installing from pypi
```
pip3 install scrabble
```
## Installing from source
```
git clone git@github.com:benjamincrom/scrabble.git
cd scrabble/
python3 setup.py install
```

## Testing
Tests take about two hours to run on an average machine.

```
python3 setup.py test
```

## Recover Scrabble Game
Recover the moves of a Scrabble game given only the 
final board and the list of player scores for each move.

Usage:
```shell
./bin/recover_scrabble_game [INPUT_FILENAME]
```
See [scrabble/tests/sample_input_files](scrabble/tests/sample_input_files)
for examples of correctly formatted input files

## Play Scrabble Game
### Create a new Scrabble game object

__*ScrabbleGame(num_players)*__

```
>>> from scrabble.main import ScrabbleGame
>>> game = ScrabbleGame(num_players=4)
>>> game
  abcdefghijklmno
1 _______________
2 _______________
3 _______________
4 _______________
5 _______________
6 _______________
7 _______________
8 _______★_______
9 _______________
10_______________
11_______________
12_______________
13_______________
14_______________
15_______________
[[G, T, E, A, D, P, C], [E, I, S, O, N, G, M], [M, S, T, U, R, O, J], [E, *, L, A, R, I, A]]
Moves played: 0
Player 1's move
72 tiles remain in bag
Player 1: 0
Player 2: 0
Player 3: 0
Player 4: 0
```

### Make Move
__ScrabbleGame.place\_word__*(word, start_location, is_vertical_move)*

Place a word from the rack of the next player onto the board.  You will be
prompted as to whether or not the move was successfully challenged.  If the
move is successful the method will return `True`.
```
>>> game.place_word(word='GATE', start_location=('h', 8), is_vertical_move=False)
Challenge successful (Y/N)N
True

>>> game
  abcdefghijklmno
1 _______________
2 _______________
3 _______________
4 _______________
5 _______________
6 _______________
7 _______________
8 _______GATE____
9 _______________
10_______________
11_______________
12_______________
13_______________
14_______________
15_______________
[[D, P, C, O, E, F, N], [E, I, S, O, N, G, M], [M, S, T, U, R, O, J], [E, *, L, A, R, I, A]]
Moves played: 1
Player 2's move
68 tiles remain in bag
Player 1: 10
Player 2: 0
Player 3: 0
Player 4: 0
```

### Find Best Move (Brute Force)
**ScrabbleGame.get_best_move()**

Find the best move via brute-force search
```
>>> game.get_best_move()

(27, (('l', 4), 'EGOISM', True))
```

### Exchange Tiles
__ScrabbleGame.exchange__*(letter_list)*

Exchange up to all a player's rack tiles as long as the bag has at least
one entire rack of tiles remaining.
```
>>> game.exchange(letter_list=['E', 'I', 'S', 'O'])
True

>>> game
  abcdefghijklmno
1 _______________
2 _______________
3 _______________
4 _______________
5 _______________
6 _______________
7 _______________
8 _______GATE____
9 _______________
10_______________
11_______________
12_______________
13_______________
14_______________
15_______________
[[D, P, C, O, E, F, N], [A, P, R, M, N, G, M], [M, S, T, U, R, O, J], [E, *, L, A, R, I, A]]
Moves played: 1
Player 3's move
68 tiles remain in bag
Player 1: 10
Player 2: 0
Player 3: 0
Player 4: 0
```

### Conclude Game
__ScrabbleGame.conclude\_game__*(empty_rack_player_number=None)*

Calculates final scores and declares a winner.  This method will automatically
be called and bonuses automatically awared if one player has an empty rack
(plays out) when the tile bag is empty.
```
>>> game.conclude_game()
Game Over! Player 1 wins with a score of 10
```
