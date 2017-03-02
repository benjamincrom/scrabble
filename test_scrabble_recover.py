import scrabble_game
import scrabble_recover

def test_get_best_move():
    scrabble_game.input = lambda x: 'N'
    game = scrabble_game.ScrabbleGame(4)

    game.cheat_create_rack_word('SCRABBL', 0)
    game.cheat_create_rack_word('ODING', 1)
    game.cheat_create_rack_word('PILE', 2)

    game.place_word('SCRAB', ('h', 8), False)
    game.place_word('(C)ODING', ('i', 8), True)
    game.place_word('PILE', ('g', 5), True)

    print(scrabble_recover.get_best_move(game))

test_get_best_move()
