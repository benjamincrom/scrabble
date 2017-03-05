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

Example:
```
./bin/recover_scrabble_game ./tests/sample_input_files/sample_input30.json

[
    [
        [(('h', 8), '*OWDY')],
        [(('e', 10), 'R(A)ZE')],
        [(('h', 12), '(Y)IP')],
        [(('b', 13), 'MOV(E)')],
        [(('c', 6), 'GU(Y)')],
        [(('l', 10), '(D)OTE')],
        [(('e', 3), '(G)UILE')],
        [(('i', 2), 'B(E)ER')],
        [(('i', 5), '(R)IP')],
        [(('g', 2), 'H(I)NT')],
        [(('l', 2), '(D)UNE')],
        [(('j', 12), '(PI)TA')],
        [(('h', 9), '(O)R*')],
        [(('o', 13), 'LI(T)')],
        [(('e', 15), 'BANAN(A)')]
    ], [
        [(('d', 11), 'FAME(D)')],
        [(('d', 8), 'CRIE(*)')],
        [
            (('i', 12), '(I)T'),
            (('j', 12), '(P)I'),
            (('i', 13), 'TIGHT')
        ],
        [(('e', 3), 'GRAYE(R)')],
        [(('l', 10), 'DAS(H)')],
        [(('o', 8), 'OV(E)N')],
        [(('c', 4), 'JA(R)')],
        [(('c', 4), '(J)I(G)')],
        [(('b', 10), 'LOO(M)S')],
        [
            (('l', 2), 'DOWEL'),
            (('i', 5), '(RIP)E')
        ],
        [(('o', 1), 'R(E)ASON')],
        [(('m', 13), '(T)AX')],
        [(('l', 15), 'E(X)IT')],
        [
            (('a', 14), 'I(S)'),
            (('a', 14), 'ID')
        ],
        [(('j', 7), 'SE(*)K')]
    ]
]
```

## Play Scrabble Game
### Create a new Scrabble game object

* __scrabble.main.ScrabbleGame(__*num_players*__)__

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
* __scrabble.main.ScrabbleGame.place\_word(__*word, start_location, is_vertical_move*__)__

Place a word from the rack of the next player onto the board.  If the
move is legal you will be prompted as to whether or not the move was
successfully challenged.  If the move goes through through then the method will
return `True`.  If the move is illegal you will not receive a challenge prompt
and the method will return `False`.
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
* **scrabble.main.ScrabbleGame.get_best_move()**

Find the best move via brute-force search.  Returns the move score and move
tuple of the form *(location, word, is_vertical_move)*.
```
>>> game.get_best_move()

(27, (('l', 4), 'EGOISM', True))
```

### Exchange Tiles
* __scrabble.main.ScrabbleGame.exchange(__*letter_list*__)__

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
* __scrabble.main.ScrabbleGame.conclude\_game(__*empty_rack_player_number=None*__)__

Calculates final scores and declares a winner.  This method will automatically
be called and bonuses automatically awarded if one player has an empty rack
(plays out) when the tile bag is empty.
```
>>> game.conclude_game()
Game Over! Player 1 wins with a score of 10
```
