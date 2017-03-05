"""
test_scrabble.py -- contains py.test functions that test scrabble library
"""
import os

import scrabble

def test_decrement_letter():
    assert scrabble.helpers.decrement_letter('d') == 'c'

def test_increment_letter():
    assert scrabble.helpers.increment_letter('a') == 'b'

def test_game_board():
    game = scrabble.main.ScrabbleGame(4)
    assert str(game.board) == ('  abcdefghijklmno\n'
                               '1 _______________\n'
                               '2 _______________\n'
                               '3 _______________\n'
                               '4 _______________\n'
                               '5 _______________\n'
                               '6 _______________\n'
                               '7 _______________\n'
                               '8 _______★_______\n'
                               '9 _______________\n'
                               '10_______________\n'
                               '11_______________\n'
                               '12_______________\n'
                               '13_______________\n'
                               '14_______________\n'
                               '15_______________')

def test_is_sublist():
    assert scrabble.helpers.move_is_sublist([1, 2, 3], [1, 2, 3, 4])
    assert not scrabble.helpers.move_is_sublist([1, 2, 3, 5], [1, 2])

def test_challenge_fail():
    scrabble.helpers.input = lambda x: 'N'
    game = scrabble.main.ScrabbleGame(4)
    game.cheat_create_rack_word('BAKER', 0)

    success = game.place_word('BAKER', ('h', 8), False, True)
    assert success is True
    assert game.player_score_list_list == [[24], [], [], []]

def test_board_moves_score():
    game = scrabble.main.ScrabbleGame(4)

    game.cheat_create_rack_word('SCRABBL', 0)
    game.cheat_create_rack_word('ODING', 1)
    game.cheat_create_rack_word('PILE', 2)

    game.place_word('SCRAB', ('h', 8), False, False)
    game.place_word('(C)ODING', ('i', 8), True, False)
    game.place_word('PILE', ('g', 5), True, False)

    assert game.player_score_list_list == [[24], [13], [17], []]
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
            'Player 1: 24\n'
            'Player 2: 13\n'
            'Player 3: 17\n'
            'Player 4: 0') in str(game)

def test_bingo():
    game = scrabble.main.ScrabbleGame(2)
    game.cheat_create_rack_word('BAKER', 0)
    game.cheat_create_rack_word('AKELAKE', 1)

    game.place_word('BAKER', ('h', 8), False, False)
    game.place_word('(R)AKELAKE', ('l', 8), True, False)

    assert game.player_score_list_list == [[24], [84]]
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
    game = scrabble.main.ScrabbleGame(3)
    game.cheat_create_rack_word('BAKER', 0)
    game.cheat_create_rack_word('CAE', 1)

    game.place_word('BAKER', ('h', 8), False, False)
    game.place_word('CA(K)E', ('j', 6), True, False)

    assert game.player_score_list_list == [[24], [16], []]
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
    game = scrabble.main.ScrabbleGame(3)
    game.cheat_create_rack_word('BAKER', 0)
    game.cheat_create_rack_word('FAKE', 1)

    game.place_word('BAKER', ('h', 8), False, False)
    game.place_word('FAKE(R)', ('l', 4), True, False)

    assert game.player_score_list_list == [[24], [24], []]
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
    game = scrabble.main.ScrabbleGame(3)
    game.cheat_create_rack_word('BAKER', 0)
    game.cheat_create_rack_word('FAKERS', 1)

    game.place_word('BAKER', ('h', 8), False, False)
    game.place_word('FAKERS', ('m', 3), True, False)

    assert game.player_score_list_list == [[24], [40], []]
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
    game = scrabble.main.ScrabbleGame(3)
    game.cheat_create_rack_word('BAKERS', 0)
    game.cheat_create_rack_word('ALAN', 1)

    game.place_word('BAKERS', ('h', 8), False, False)
    game.place_word('ALAN', ('h', 9), False, False)

    assert game.player_score_list_list == [[26], [20], []]
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
    game = scrabble.main.ScrabbleGame(3)
    game.cheat_create_rack_word('BAKERSTO', 0)

    success = game.place_word('BAKERSTO', ('h', 8), False, False)
    assert success is False

def test_get_rack_tile_bad():
    game = scrabble.main.ScrabbleGame(3)
    assert (
        scrabble.helpers.get_rack_tile_index(game.player_rack_list[0], '&')
        is None
    )

def test_player_exchange_bad_choices():
    game = scrabble.main.ScrabbleGame(3)
    success = game.exchange(['Z', 'Z', 'Z', 'Z'])
    assert success is False

def test_player_exchange_not_enough_tiles():
    game = scrabble.main.ScrabbleGame(3)
    game.tile_bag = game.tile_bag[:4]
    player_letter_list = [tile.letter for tile in game.player_rack_list[0]]
    success = game.exchange(player_letter_list)
    assert success is False

    new_player_letter_list = [tile.letter for tile in game.player_rack_list[0]]
    assert player_letter_list == new_player_letter_list

def test_player_exchange():
    game = scrabble.main.ScrabbleGame(3)
    player_letter_list = [str(tile) for tile in game.player_rack_list[0]]
    game.exchange(player_letter_list)
    new_player_letter_list = [tile.letter for tile in game.player_rack_list[0]]
    assert player_letter_list != new_player_letter_list

def test_out_of_tiles():
    game = scrabble.main.ScrabbleGame(3)
    game.tile_bag = game.tile_bag[:4]
    game.player_rack_list[0] = []
    game.cheat_create_rack_word('BAKERS', 0)
    game.place_word('BAKERS', ('h', 8), False)

    assert len(game.player_rack_list[0]) == 4
    assert len(game.tile_bag) == 0

def test_out_of_bounds():
    game = scrabble.main.ScrabbleGame(3)
    game.cheat_create_rack_word('BAKERS', 0)
    game.cheat_create_rack_word('ERIOUS', 1)
    game.cheat_create_rack_word('TYLISH', 2)

    game.place_word('BAKERS', ('h', 8), False, False)
    game.place_word('(S)ERIOUS', ('m', 9), True, False)
    success = game.place_word('(S)TYLISH', ('n', 14), True)
    assert success is False

def test_misalign_tiles():
    game = scrabble.main.ScrabbleGame(3)
    game.cheat_create_rack_word('EAI', 0)

    success = game.next_player_move(
        [('E', ('h', 6)), ('A', ('i', 9)), ('I', ('h', 7))]
    )

    assert success is False

def test_disconnect_tiles_horizontal():
    game = scrabble.main.ScrabbleGame(3)
    game.cheat_create_rack_word('EAI', 0)

    success = game.next_player_move(
        [('E', ('h', 8)), ('A', ('h', 9)), ('I', ('h', 11))],
        False
    )

    assert success is False

def test_vertical_tiles_horizontal():
    game = scrabble.main.ScrabbleGame(3)
    game.cheat_create_rack_word('EAI', 0)

    success = game.next_player_move(
        [('E', ('h', 8)), ('A', ('i', 8)), ('I', ('k', 8))],
        False
    )

    assert success is False

def test_stack_tiles():
    game = scrabble.main.ScrabbleGame(3)
    game.cheat_create_rack_word('EAI', 0)

    success = game.next_player_move(
        [('E', ('h', 6)), ('A', ('h', 6)), ('I', ('h', 7))],
        False
    )

    assert success is False

def test_letters_not_in_rack():
    game = scrabble.main.ScrabbleGame(3)
    success = game.place_word('ZZZZZZ', ('h', 8), False, False)
    assert success is False

def test_move_touches_no_tiles():
    game = scrabble.main.ScrabbleGame(3)
    game.cheat_create_rack_word('BAKERS', 0)
    game.cheat_create_rack_word('BAKERS', 1)

    game.place_word('BAKERS', ('h', 8), False, False)
    success = game.place_word('BAKERS', ('h', 10), False, False)
    assert success is False

def test_move_covers_tiles():
    game = scrabble.main.ScrabbleGame(3)
    game.cheat_create_rack_word('BAKERS', 0)
    game.cheat_create_rack_word('LAKERS', 1)

    game.place_word('BAKERS', ('h', 8), False, False)
    success = game.place_word('LAKERS', ('h', 6), True, False)
    assert success is False

def test_conclude_game():
    game = scrabble.main.ScrabbleGame(3)

    game.cheat_create_rack_word('BAKERS', 0)
    game.place_word('BAKERS', ('h', 8), False, False)

    game.tile_bag = []
    game.player_rack_list = [[], [], []]

    game.cheat_create_rack_word('CIOOIVA', 0)
    game.cheat_create_rack_word('ABCDEFG', 1)
    game.cheat_create_rack_word('AIUWZEE', 2)
    game.place_word('ABCDEFG', ('h', 9), True, False)

    assert game.player_score_list_list == [[26, -12], [113, 31], [-19]]
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

def test_challenge_success():
    scrabble.helpers.input = lambda x: 'Y'
    game = scrabble.main.ScrabbleGame(4)
    game.cheat_create_rack_word('SCRAB', 0)
    success = game.place_word('SCRAB', ('h', 8), False, True)

    assert success
    assert game.player_score_list_list == [[0], [], [], []]

def test_challenge_neither():
    my_iter = iter(['yay'])
    def mock_input(_):
        return next(my_iter, 'Y')

    scrabble.helpers.input = mock_input
    game = scrabble.main.ScrabbleGame(4)
    game.cheat_create_rack_word('SCRAB', 0)
    success = game.place_word('SCRAB', ('h', 8), False, True)

    assert success
    assert game.player_score_list_list == [[0], [], [], []]

def test_recover_game():
    expected_notated_move_set_list = [
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
    ]

    frozen_expected_notated_move_set_list = [
        frozenset(move) for notated_move_set in expected_notated_move_set_list
                        for move_set in notated_move_set
                        for move in move_set
    ]

    current_directory = os.path.dirname(__file__)
    notated_move_set_list = scrabble.main.recover_game(
        os.path.join(current_directory,
                     'sample_input_files/sample_input30.json')
    )

    frozen_notated_move_set_list = [
        frozenset(move) for notated_move_set in notated_move_set_list
                        for move_set in notated_move_set
                        for move in move_set
    ]

    assert (
        frozen_expected_notated_move_set_list == frozen_notated_move_set_list
    )

def test_get_best_move():
    game = scrabble.main.ScrabbleGame(4)

    game.cheat_create_rack_word('SCRABBL', 0)
    game.cheat_create_rack_word('ODING', 1)
    game.cheat_create_rack_word('PILE', 2)

    game.place_word('SCRAB', ('h', 8), False, False)
    game.place_word('(C)ODING', ('i', 8), True, False)
    game.place_word('PILE', ('g', 5), True, False)

    game.player_rack_list[3] = []
    game.cheat_create_rack_word('ADPOSTN', 3)

    score, move_tuple = game.get_best_move()

    assert (score, move_tuple) == (81, (('a', 4), 'DOPANTS', False))
