import scrabble_game

def test_decrement_letter():
    assert (scrabble_game.decrement_letter('d') == 'c')

def test_increment_letter():
    assert (scrabble_game.increment_letter('a') == 'b')

def test_is_sublist():
    assert(scrabble_game.is_sublist([1, 2, 3], [1, 2, 3, 4]))
    assert(not scrabble_game.is_sublist([1, 2, 3, 5], [1, 2]))


def test_board_moves_score():
    game = scrabble_game.ScrabbleGame(4)
    game.place_word('SCRAB', ('h', 8), False, True)
    game.place_word('ODING', ('i', 9), True, True)
    game.place_word('PILE', ('g', 5), True, True)

    assert game.player_score_list_list == [[12], [13], [17], []]
    assert game.move_number == 3
    assert len(game.tile_bag) == 72
    assert str(game.board) == ('  abcdefghijklmno\n'
                               '1 _______________\n'
                               '2 _______________\n'
                               '3 _______________\n'
                               '4 _______________\n'
                               '5 ______P________\n'
                               '6 ______I________\n'
                               '7 ______L________\n'
                               '8 ______ESCRAB___\n'
                               '9 ________O______\n'
                               '10________D______\n'
                               '11________I______\n'
                               '12________N______\n'
                               '13________G______\n'
                               '14_______________\n'
                               '15_______________')


def test_bingo():
    game = scrabble_game.ScrabbleGame(4)
    game.place_word('BAKER', ('h', 8), False, True)
    game.place_word('AKELAKE', ('l', 9), True, True)

    import pdb; pdb.set_trace()  # breakpoint 8e011190 //
    assert game.player_score_list_list == [[12], [13], [17], []]
    assert game.move_number == 3
    assert len(game.tile_bag) == 72
    assert str(game.board) == ('  abcdefghijklmno\n'
                               '1 _______________\n'
                               '2 _______________\n'
                               '3 _______________\n'
                               '4 _______________\n'
                               '5 ______P________\n'
                               '6 ______I________\n'
                               '7 ______L________\n'
                               '8 ______ESCRAB___\n'
                               '9 ________O______\n'
                               '10________D______\n'
                               '11________I______\n'
                               '12________N______\n'
                               '13________G______\n'
                               '14_______________\n'
                               '15_______________')

'''
def test_itersect_words_regular

def test_intersetct_corner

def test_intersect_words_double_points

def test_intersect_parallel

def test_play_too_many_tiles

def test_out_of_bounds

def test_letters_not_in_rack

def test_move_stacks_tiles

def test_tiles_disconnected

def test_tiles_out_of_alignment

def test_conclude_game


'''