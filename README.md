# Scrabble
This package implements the game of Scrabble and also adds features that
recover previous moves as well as determine the best next move for a given
Scrabble game.

## Installation
```
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
See [scrabble/tests/sample_input_file/](`scrabble/tests/sample_input_files/)
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
__*ScrabbleGame.place_word(word, start_location, is_vertical_move)*__

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
__*helpers.get_best_move(game=game)*__

Find the best move via brute-force search
```
>>> import helpers
>>> helpers.get_best_move(game=game)

(27, (('l', 4), 'EGOISM', True))
```

### Exchange Tiles
__*ScrabbleGame.exchange(letter_list)*__

Exchange up to all a player's rack tiles as long as the bag has at least
one entire rack of tile remaining.
```
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
[[P, E, C, V, U, R, N], [O, L, S, N, T, N, O], [L, N, N, R, G, F, T], [U, Q, R, I, E, E, W]]
Moves played: 0
Player 1's move
72 tiles remain in bag
Player 1: 0
Player 2: 0
Player 3: 0
Player 4: 0

>>> game.exchange(letter_list=['P', 'E', 'C', 'V'])
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
8 _______★_______
9 _______________
10_______________
11_______________
12_______________
13_______________
14_______________
15_______________
[[U, R, N, H, E, D, E], [O, L, S, N, T, N, O], [L, N, N, R, G, F, T], [U, Q, R, I, E, E, W]]
Moves played: 1
Player 2's move
72 tiles remain in bag
Player 1: 0
Player 2: 0
Player 3: 0
Player 4: 0
```

### Conclude Game
__*ScrabbleGame.conclude_game(empty_rack_player_number=None)*__

Calculates final scores and winner.  Awards bonuses and penalties if one player
has an empty rack (plays out) at the end of the game.
```
>>> game.conclude_game(empty_rack_player_number=1)
Game Over! Player 1 wins with a score of 39
```
