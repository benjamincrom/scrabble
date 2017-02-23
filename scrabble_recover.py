import itertools
import json

import scrabble_board
import scrabble_game

def find_kleene_star(input_iterable):
    master_set = set()
    for i in range(len(input_iterable) + 1):
        for this_set in itertools.combinations(input_iterable, i):
            master_set.add(this_set)
        
    return master_set

def load_file(input_filename):
    with open(input_filename, 'r') as filehandle:
        input_str = filehandle.read()

    input_dict = json.loads(input_str)
    board_character_array = input_dict['board']
    player_score_list_list = input_dict['scores']

    return board_character_array, player_score_list_list

def read_input_file(input_filename):
    board_character_array, player_score_list_list = load_file(input_filename)

    num_players = len(player_score_list_list)
    game = scrabble_game.ScrabbleGame(num_players)
    game.player_score_list_list = player_score_list_list
    game.player_rack_list = [[] for _ in range(num_players)]
    game.tile_bag = []

    for row_number, row in enumerate(board_character_array):
        for column_number, letter in enumerate(row):
            if letter:
                column_letter = chr(ord('a') + column_number)
                this_location = (column_letter, row_number + 1)
                game.board[this_location] = scrabble_board.ScrabbleTile(letter)

    return game

def get_all_board_tiles(game):
    return set((square_tuple[1].tile, square_tuple[0])  # tile then location
               for square_tuple in game.board.board_square_dict.items()
               if square_tuple[1].tile)

def get_legal_move_set(game):
    location_tile_set = get_all_board_tiles(game)
    all_possible_moves_set = find_kleene_star(location_tile_set)

    legal_move_set = set()
    for move_set in all_possible_moves_set:
        new_game = scrabble_game.ScrabbleGame(len(game.player_rack_list))

        if scrabble_game.move_is_legal(new_game.board, 0, move_set):
            for tile, location in move_set:
                new_game.board[location] = tile

            legal_move_set.add(
                (scrabble_game.score_move(move_set, new_game.board), move_set)
            )

    return legal_move_set

game = read_input_file('sample_input.json')
legal_move_set = get_legal_move_set(game)

