import scrabble_game
'''
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
    game = scrabble_game.ScrabbleGame(2)
    game.place_word('BAKER', ('h', 8), False, True)
    game.place_word('AKELAKE', ('l', 9), True, True)

    assert game.player_score_list_list == [[12], [84]]
    assert game.move_number == 2
    assert len(game.tile_bag) == 86
    assert str(game.board) == ('  abcdefghijklmno\n'
                               '1 _______________\n'
                               '2 _______________\n'
                               '3 _______________\n'
                               '4 _______________\n'
                               '5 _______________\n'
                               '6 _______________\n'
                               '7 _______________\n'
                               '8 _______BAKER___\n'
                               '9 ___________A___\n'
                               '10___________K___\n'
                               '11___________E___\n'
                               '12___________L___\n'
                               '13___________A___\n'
                               '14___________K___\n'
                               '15___________E___')


def test_itersect_words_regular():
    game = scrabble_game.ScrabbleGame(3)
    game.place_word('BAKER', ('h', 8), False, True)
    game.place_word('CA(K)E', ('j', 6), True, True)

    assert game.player_score_list_list == [[12], [16], []]
    assert game.move_number == 2
    assert len(game.tile_bag) == 79
    assert str(game.board) == ('  abcdefghijklmno\n'
                               '1 _______________\n'
                               '2 _______________\n'
                               '3 _______________\n'
                               '4 _______________\n'
                               '5 _______________\n'
                               '6 _________C_____\n'
                               '7 _________A_____\n'
                               '8 _______BAKER___\n'
                               '9 _________E_____\n'
                               '10_______________\n'
                               '11_______________\n'
                               '12_______________\n'
                               '13_______________\n'
                               '14_______________\n'
                               '15_______________')

def test_intersetct_corner():
    game = scrabble_game.ScrabbleGame(3)
    game.place_word('BAKER', ('h', 8), False, True)
    game.place_word('FAKE', ('l', 4), True, True)

    assert game.player_score_list_list == [[12], [24], []]
    assert game.move_number == 2
    assert len(game.tile_bag) == 79
    assert str(game.board) == ('  abcdefghijklmno\n'
                               '1 _______________\n'
                               '2 _______________\n'
                               '3 _______________\n'
                               '4 ___________F___\n'
                               '5 ___________A___\n'
                               '6 ___________K___\n'
                               '7 ___________E___\n'
                               '8 _______BAKER___\n'
                               '9 _______________\n'
                               '10_______________\n'
                               '11_______________\n'
                               '12_______________\n'
                               '13_______________\n'
                               '14_______________\n'
                               '15_______________')


def test_intersect_words_double_points():
    game = scrabble_game.ScrabbleGame(3)
    game.place_word('BAKER', ('h', 8), False, True)
    game.place_word('FAKERS', ('m', 3), True, True)

    assert game.player_score_list_list == [[12], [40], []]
    assert game.move_number == 2
    assert len(game.tile_bag) == 79
    assert str(game.board) == ('  abcdefghijklmno\n'
                               '1 _______________\n'
                               '2 _______________\n'
                               '3 ____________F__\n'
                               '4 ____________A__\n'
                               '5 ____________K__\n'
                               '6 ____________E__\n'
                               '7 ____________R__\n'
                               '8 _______BAKERS__\n'
                               '9 _______________\n'
                               '10_______________\n'
                               '11_______________\n'
                               '12_______________\n'
                               '13_______________\n'
                               '14_______________\n'
                               '15_______________')
'''
def test_intersect_parallel():
    game = scrabble_game.ScrabbleGame(3)
    game.place_word('BAKERS', ('h', 8), False, True)
    game.place_word('ALAN', ('h', 9), False, True)

    assert game.player_score_list_list == [[13], [20], []]
    assert game.move_number == 2
    assert len(game.tile_bag) == 79
    assert str(game.board) == ('  abcdefghijklmno\n'
                               '1 _______________\n'
                               '2 _______________\n'
                               '3 _______________\n'
                               '4 _______________\n'
                               '5 _______________\n'
                               '6 _______________\n'
                               '7 _______________\n'
                               '8 _______BAKERS__\n'
                               '9 _______ALAN____\n'
                               '10_______________\n'
                               '11_______________\n'
                               '12_______________\n'
                               '13_______________\n'
                               '14_______________\n'
                               '15_______________')

'''
def test_play_too_many_tiles

def test_out_of_bounds

def test_letters_not_in_rack

def test_move_stacks_tiles

def test_tiles_disconnected

def test_tiles_out_of_alignment

def test_conclude_game


'''