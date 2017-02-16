import scrabble_game

def test_decrement_letter():
    assert scrabble_game.decrement_letter('d') == 'c'

def test_increment_letter():
    assert scrabble_game.increment_letter('a') == 'b'

def test_is_sublist():
    game = scrabble_game.ScrabbleGame(4)
    assert game.move_is_sublist([1, 2, 3], [1, 2, 3, 4])
    assert not game.move_is_sublist([1, 2, 3, 5], [1, 2])

def test_board_moves_score():
    game = scrabble_game.ScrabbleGame(4)
    game.place_word('SCRAB', ('h', 8), False, True)
    game.place_word('(C)ODING', ('i', 8), True, True)
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

    assert ('Moves played: 3\n'
            'Player 4\'s move\n'
            '72 tiles remain in bag\n'
            'Player 1: 12\n'
            'Player 2: 13\n'
            'Player 3: 17\n'
            'Player 4: 0') in str(game)

def test_bingo():
    game = scrabble_game.ScrabbleGame(2)
    game.place_word('BAKER', ('h', 8), False, True)
    game.place_word('(R)AKELAKE', ('l', 8), True, True)

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

def test_intersect_corner():
    game = scrabble_game.ScrabbleGame(3)
    game.place_word('BAKER', ('h', 8), False, True)
    game.place_word('FAKE(R)', ('l', 4), True, True)

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

def test_play_too_many_tiles():
    game = scrabble_game.ScrabbleGame(3)
    assert(
        game.place_word('BAKERSTO', ('h', 8), False, True) is False
    )

def test_get_rack_tile_bad():
    game = scrabble_game.ScrabbleGame(3)
    assert game.get_rack_tile_index(game.player_rack_list[0], '&') is None

def test_player_exchange_bad_choices():
    game = scrabble_game.ScrabbleGame(3)
    assert game.next_player_exchange(['Z', 'Z', 'Z', 'Z']) is False

def test_player_exchange_not_enough_tiles():
    game = scrabble_game.ScrabbleGame(3)
    game.tile_bag = game.tile_bag[:4]
    player_letter_list = [tile.letter for tile in game.player_rack_list[0]]
    assert game.next_player_exchange(player_letter_list) is False

    new_player_letter_list = [tile.letter for tile in game.player_rack_list[0]]
    assert player_letter_list == new_player_letter_list

def test_player_exchange():
    game = scrabble_game.ScrabbleGame(3)
    player_letter_list = [str(tile) for tile in game.player_rack_list[0]]
    game.next_player_exchange(player_letter_list)
    new_player_letter_list = [tile.letter for tile in game.player_rack_list[0]]
    assert player_letter_list != new_player_letter_list

def test_out_of_tiles():
    game = scrabble_game.ScrabbleGame(3)
    game.tile_bag = game.tile_bag[:4]
    game.player_rack_list[0] = []
    game.place_word('BAKERS', ('h', 8), False, True)

def test_out_of_bounds():
    game = scrabble_game.ScrabbleGame(3)
    game.place_word('BAKERS', ('h', 8), False, True)
    game.place_word('(S)ERIOUS', ('m', 9), True, True)
    assert game.place_word('(S)TYLISH', ('n', 14), True, True) is False

def test_misalign_tiles():
    game = scrabble_game.ScrabbleGame(3)
    game.cheat_add_rack_tile('E', game.player_rack_list[0])
    game.cheat_add_rack_tile('A', game.player_rack_list[0])
    game.cheat_add_rack_tile('I', game.player_rack_list[0])
    game.next_player_move([('E', ('h', 6)), ('A', ('i', 9)), ('I', ('h', 7))])

def test_disconnect_tiles_horizontal():
    game = scrabble_game.ScrabbleGame(3)
    game.cheat_add_rack_tile('E', game.player_rack_list[0])
    game.cheat_add_rack_tile('A', game.player_rack_list[0])
    game.cheat_add_rack_tile('I', game.player_rack_list[0])
    game.next_player_move([('E', ('h', 8)), ('A', ('h', 9)), ('I', ('h', 11))])

def test_vertical_tiles_horizontal():
    game = scrabble_game.ScrabbleGame(3)
    game.cheat_add_rack_tile('E', game.player_rack_list[0])
    game.cheat_add_rack_tile('A', game.player_rack_list[0])
    game.cheat_add_rack_tile('I', game.player_rack_list[0])
    game.next_player_move([('E', ('h', 8)), ('A', ('i', 8)), ('I', ('k', 8))])

def test_stack_tiles():
    game = scrabble_game.ScrabbleGame(3)
    game.cheat_add_rack_tile('E', game.player_rack_list[0])
    game.cheat_add_rack_tile('A', game.player_rack_list[0])
    game.cheat_add_rack_tile('I', game.player_rack_list[0])
    game.next_player_move([('E', ('h', 6)), ('A', ('h', 6)), ('I', ('h', 7))])

def test_letters_not_in_rack():
    game = scrabble_game.ScrabbleGame(3)
    assert game.place_word('ZZZZZZ', ('h', 8), False, False) is False

def test_move_touches_no_tiles():
    game = scrabble_game.ScrabbleGame(3)
    game.place_word('BAKERS', ('h', 8), False, True)
    assert game.place_word('BAKERS', ('h', 10), False, True) is False

def test_move_covers_tiles():
    game = scrabble_game.ScrabbleGame(3)
    game.place_word('BAKERS', ('h', 8), False, True)
    assert game.place_word('LAKERS', ('h', 6), True, True) is False

def test_conclude_game():
    game = scrabble_game.ScrabbleGame(3)
    game.place_word('BAKERS', ('h', 8), False, True)

    game.tile_bag = []
    game.player_rack_list = [[], [], []]

    for c in 'CIOOIVA':
        game.cheat_add_rack_tile(c, game.player_rack_list[0])

    for c in 'ABCDEFG':
        game.cheat_add_rack_tile(c, game.player_rack_list[1])

    for c in 'AIUWZEE':
        game.cheat_add_rack_tile(c, game.player_rack_list[2])

    game.next_player_move([('A', ('h', 9)),
                           ('B', ('h', 10)),
                           ('C', ('h', 11)),
                           ('D', ('h', 12)),
                           ('E', ('h', 13)),
                           ('F', ('h', 14)),
                           ('G', ('h', 15))])

    assert game.player_score_list_list == [[13, -12], [113, 0, 31], [-19]]
    assert game.move_number == 2
    assert len(game.tile_bag) == 0
    assert str(game.board) == ('  abcdefghijklmno\n'
                               '1 _______________\n'
                               '2 _______________\n'
                               '3 _______________\n'
                               '4 _______________\n'
                               '5 _______________\n'
                               '6 _______________\n'
                               '7 _______________\n'
                               '8 _______BAKERS__\n'
                               '9 _______A_______\n'
                               '10_______B_______\n'
                               '11_______C_______\n'
                               '12_______D_______\n'
                               '13_______E_______\n'
                               '14_______F_______\n'
                               '15_______G_______')
