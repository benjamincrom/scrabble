import copy
import itertools
import json

import scrabble_board
import scrabble_game

scrabble_game.input = lambda x: 'N'

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
    game.move_number = len(player_score_list_list[0])

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

def get_legal_move_set(new_game, reference_game):
    game_tile_set = get_all_board_tiles(new_game)
    reference_tile_set = get_all_board_tiles(reference_game)

    search_set = set()
    for reference_tile, reference_location in reference_tile_set:
        flag = True
        for game_tile, _ in game_tile_set:
            if game_tile.letter == reference_tile.letter:
                flag = False

        if flag:
            search_set.add((reference_tile, reference_location))

    all_possible_moves_set = find_kleene_star(search_set)

    legal_move_set = set()
    for move_set in all_possible_moves_set:
        temp_game = copy.deepcopy(new_game)
        if scrabble_game.move_is_legal(temp_game.board, new_game.move_number, move_set):
            for tile, location in move_set:
                temp_game.board[location] = tile

            legal_move_set.add(
                (scrabble_game.score_move(move_set, temp_game.board), move_set)
            )

    return legal_move_set

def find_next_move(new_game, reference_game):
    legal_move_set = get_legal_move_set(new_game, reference_game)

    player_to_move_id = new_game.move_number % len(new_game.player_rack_list)
    player_score_list = reference_game.player_score_list_list[player_to_move_id]

    player_move_number = new_game.move_number // len(new_game.player_rack_list)
    target_score = player_score_list[player_move_number]

    for score, move_set in legal_move_set:
        if score == target_score:
            return set((str(tile), location) for tile, location in move_set)

    return None

def reverse_engineer_move_list(input_filename):
    reference_game = read_input_file(input_filename)
    new_game = scrabble_game.ScrabbleGame(len(reference_game.player_rack_list))

    move_set_list = []
    while new_game.move_number <= reference_game.move_number:
        next_move_set = find_next_move(new_game, reference_game)
        move_set_list.append(next_move_set)

        player_to_move_id = new_game.move_number % len(new_game.player_rack_list)
        next_move_str = ''.join(str(tile) for tile, location in next_move_set)
        new_game.cheat_create_rack_word(next_move_str, player_to_move_id)
        new_game.next_player_move(next_move_set)

    return move_set_list

reverse_engineer_move_list('sample_input.json')
