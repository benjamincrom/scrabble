import scrabble_game

def test_board_moves_score():
    game = scrabble_game.ScrabbleGame(4)
    game.place_word('SCRABBLE', ('h', 8), False, True)
    game.place_word('ODING', ('i', 9), True, True)
    game.place_word('PILE', ('g', 5), True, True)

    assert game.player_score_list_list == [[51], [13], [22], []]
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
                               '8 ______ESCRABBLE\n'
                               '9 ________O______\n'
                               '10________D______\n'
                               '11________I______\n'
                               '12________N______\n'
                               '13________G______\n'
                               '14_______________\n'
                               '15_______________')
