# Scrabble Recover
Recover the moves of a Scrabble game given only the 
final board and the list of player scores for each move.

Usage:
```shell
python3 recover_scrabble_game.py [INPUT_FILENAME]
```

See `sample_input_files/` for examples of correctly formatted input files

# Scrabble Game
Model a Scrabble game 
```
>>> import scrabble_game
>>> game = scrabble_game.ScrabbleGame(num_players=4)
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

# Find Best Move
Find the best move via brute-force search
```
>>> import helpers
>>> helpers.get_best_move(game)
```