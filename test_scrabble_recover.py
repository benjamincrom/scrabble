import scrabble_game
import helpers

def test_get_best_move():
    game = scrabble_game.ScrabbleGame(4)

    game.cheat_create_rack_word('SCRABBL', 0)
    game.cheat_create_rack_word('ODING', 1)
    game.cheat_create_rack_word('PILE', 2)

    game.place_word('SCRAB', ('h', 8), False, False)
    game.place_word('(C)ODING', ('i', 8), True, False)
    game.place_word('PILE', ('g', 5), True, False)

    best_move_tuple = helpers.get_best_move(game)
    print(game)
    print(best_move_tuple)
    print(best_move_tuple[0])
    assert best_move_tuple[0] > 0

test_get_best_move()
