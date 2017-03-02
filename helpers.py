'''
scrabble_recover.py -- contains functions that recover a game's moves given
                       final board and score list

Usage:
    ./scrabble_recover [INPUT_FILENAME]

    See sample_input_files/ for examples of correctly formatted input files
'''
import collections
import datetime
import itertools
import json
import multiprocessing
import operator
import random
import sys

import config
import scrabble_game

with open(config.DICTIONARY_FILENAME) as filehandle:
    english_dictionary_set = set(word.strip()
                                 for word in filehandle.readlines())

def initialize_new_board_square_dict():
    initial_board_square_dict = {}
    for column in config.BOARD_CODE_DICT:
        for row in range(1, config.BOARD_NUM_ROWS + 1):
            location = (column, row)

            word_multiplier = config.WORD_SCORE_MULT_LOCATION_DICT.get(
                location,
                1
            )

            letter_multiplier = config.LETTER_SCORE_MULT_LOCATION_DICT.get(
                location,
                1
            )

            initial_board_square_dict[location] = scrabble_game.BoardSquare(
                tile=None,
                word_multiplier=word_multiplier,
                letter_multiplier=letter_multiplier
            )

    return initial_board_square_dict

def get_combinations(input_iterable):
    combination_set = set()

    for column_letter in config.BOARD_CODE_DICT:
        column_tile_set = frozenset((tile, location)
                                    for tile, location in input_iterable
                                    if location[0] == column_letter)

        for i in range(1, config.PLAYER_RACK_SIZE + 1):
            for this_set in itertools.combinations(column_tile_set, i):
                combination_set.add(this_set)

    for row_number in range(1, config.BOARD_NUM_ROWS + 1):
        row_tile_set = frozenset((tile, location)
                                 for tile, location in input_iterable
                                 if location[1] == row_number)

        for i in range(1, config.PLAYER_RACK_SIZE + 1):
            for this_set in itertools.combinations(row_tile_set, i):
                combination_set.add(this_set)

    return combination_set

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
    game.move_number = sum(1 for player_score_list in player_score_list_list
                             for _ in player_score_list)

    for row_number, row in enumerate(board_character_array):
        for column_number, letter in enumerate(row):
            if letter:
                column_letter = chr(ord('a') + column_number)
                this_location = (column_letter, row_number + 1)
                game.board[this_location] = scrabble_game.ScrabbleTile(letter)

    return game

def get_all_board_tiles(game):
    return set((square_tuple[1].tile, square_tuple[0])  # tile then location
               for square_tuple in game.board.board_square_dict.items()
               if square_tuple[1].tile)

def move_is_board_subset(move_set, board):
    for tile, location in move_set:
        move_letter = tile.letter
        board_tile = board[location]
        if not board_tile or board_tile.letter != move_letter:
            return False

    return True

def boards_are_equivalent(board_1, board_2):
    return str(board_1) == str(board_2)

def get_all_possible_moves_set(new_game, reference_game):
    game_tile_location_set = get_all_board_tiles(new_game)
    reference_tile_location_set = get_all_board_tiles(reference_game)

    search_set = set()
    for reference_tile, reference_location in reference_tile_location_set:
        flag = True
        for game_tile, game_location in game_tile_location_set:
            if (game_tile.letter == reference_tile.letter and
                    game_location == reference_location):
                flag = False

        if flag:
            search_set.add((reference_tile, reference_location))

    return get_combinations(search_set)

def copy_board(input_board):
    input_square_dict = input_board.board_square_dict

    new_board = scrabble_game.ScrabbleBoard()
    new_square_dict = new_board.board_square_dict

    for location, square in input_square_dict.items():
        if square.tile:
            new_board_square = new_square_dict[location]
            new_board_square.letter_multiplier = square.letter_multiplier
            new_board_square.word_multiplier = square.word_multiplier
            new_board_square.tile = scrabble_game.ScrabbleTile(
                square.tile.letter
            )

    return new_board

def copy_game(input_game):
    new_game = scrabble_game.ScrabbleGame(len(input_game.player_rack_list))
    new_game.board = copy_board(input_game.board)
    new_game.move_number = input_game.move_number
    new_game.player_score_list_list = [
        input_player_score_list[:]
        for input_player_score_list in input_game.player_score_list_list
    ]

    return new_game

def get_legal_move_set(new_game, reference_game):
    all_possible_moves_set = get_all_possible_moves_set(new_game,
                                                        reference_game)

    legal_move_set = set()
    for move_set in all_possible_moves_set:
        if (move_is_board_subset(move_set, reference_game.board) and
                move_is_legal(new_game.board, new_game.move_number, move_set)):
            temp_board = copy_board(new_game.board)
            for tile, location in move_set:
                temp_board[location] = tile

            legal_move_set.add(
                (score_move(move_set, temp_board), move_set)
            )

    return legal_move_set

def all_created_words_are_english(board, letter_location_set):
    word_set = get_word_set(board, letter_location_set)

    for word_location_set in word_set:
        if word_location_set:
            this_word_str = ''
            for location in sorted(word_location_set):
                square = board.board_square_dict[location]
                this_word_str += str(square.tile.letter)

            if this_word_str.lower() not in english_dictionary_set:
                return False

    return True

def get_location_best_move(game, location, word_list):
    player_to_move_id = game.move_number % len(game.player_rack_list)

    high_score = 0
    best_move = None
    print(str(location) + '\t \t \t' + str(datetime.datetime.now()))
    for word in word_list:
        for is_vertical in [True, False]:
            temp_game = copy_game(game)
            if temp_game.place_word(word, location, is_vertical):
                letter_location_set = (
                    get_word_letter_location_set(word, location, is_vertical)
                )

                location_set = set(location
                                   for _, location in letter_location_set)

                if all_created_words_are_english(temp_game.board,
                                                 location_set):
                    player_score_list = (
                        temp_game.player_score_list_list[player_to_move_id]
                    )

                    word_score = player_score_list[-1]
                    if word_score > high_score:
                        best_move = (location, word, is_vertical)
                        high_score = word_score

    return high_score, best_move

def get_location_best_move_helper(argument_list):
    return get_location_best_move(*argument_list)

def get_best_move(game):
    player_to_move_id = game.move_number % len(game.player_rack_list)
    player_rack = game.player_rack_list[player_to_move_id]
    player_letter_list = [tile.letter for tile in player_rack]

    word_list = []
    for i in range(1, config.PLAYER_RACK_SIZE + 1):
        for this_list in itertools.permutations(player_letter_list, i):
            this_word = ''.join(this_list)
            word_list.append(this_word)

    input_arguments_list = [
        (game, location, word_list)
        for location in sorted(game.board.board_square_dict)
    ]

    process_pool = multiprocessing.Pool(8)
    result_list = process_pool.map(get_location_best_move_helper,
                                   input_arguments_list)

    return max(result_list)

def get_move_set_generator(new_game, reference_game, move_list):
    legal_move_set = get_legal_move_set(new_game, reference_game)

    player_to_move_id = new_game.move_number % len(new_game.player_rack_list)
    player_score_list = reference_game.player_score_list_list[player_to_move_id]
    player_move_number = new_game.move_number // len(new_game.player_rack_list)
    target_score = player_score_list[player_move_number]

    next_move_set = set(
        frozenset((tile.letter, location) for tile, location in move_set)
        for score, move_set in legal_move_set
        if score == target_score
    )

    for next_move in next_move_set:
        new_game_copy = copy_game(new_game)
        move_list_copy = move_list[:]

        player_to_move_id = (
            new_game_copy.move_number % len(new_game_copy.player_rack_list)
        )

        next_move_str = ''.join(letter for letter, location in next_move)
        new_game_copy.cheat_create_rack_word(next_move_str, player_to_move_id)
        new_game_copy.next_player_move(next_move)
        move_list_copy.append(next_move)

        if new_game_copy.move_number == reference_game.move_number:
            if boards_are_equivalent(reference_game.board, new_game_copy.board):
                yield move_list_copy

        else:
            yield from get_move_set_generator(new_game_copy,
                                              reference_game,
                                              move_list_copy)

def get_move_set_notation(move_set, reference_game):
    new_game = scrabble_game.ScrabbleGame(len(reference_game.player_rack_list))
    word_notation_list_list = [
        [] for _ in range(len(reference_game.player_rack_list))
    ]

    for move in move_set:
        player_to_move_id = new_game.move_number % len(new_game.player_rack_list)
        move_location_set = set(location for _, location in move)
        rack_word = ''.join([letter for letter, _ in move])
        new_game.cheat_create_rack_word(rack_word, player_to_move_id)

        player_words_notation_list = (
            word_notation_list_list[player_to_move_id]
        )

        notation_word_list = []
        new_game.next_player_move(move)
        word_set = get_word_set(new_game.board, move_location_set)
        for word_location_set in word_set:
            if word_location_set:
                move_word = ''
                word_location_list = sorted(word_location_set)
                notation_location = word_location_list[0]
                parens_flag = False

                for location in word_location_list:
                    tile = new_game.board[location]
                    if tile:
                        if location not in move_location_set:
                            if not parens_flag:
                                move_word += '('
                                parens_flag = True
                        else:
                            if parens_flag:
                                move_word += ')'
                                parens_flag = False

                        move_word += tile.letter

                if parens_flag:
                    move_word += ')'

                notation_word_list.append((notation_location, move_word))

        player_words_notation_list.append(notation_word_list)

    return word_notation_list_list

def conclude_game(player_score_list_list):
    player_score_total_list = [sum(player_score_list)
                               for player_score_list in player_score_list_list]

    winning_player_id, winning_player_score = max(
        enumerate(player_score_total_list),
        key=operator.itemgetter(1)
    )

    print(
        'Game Over! Player {} wins with a score of {}'.format(
            winning_player_id + 1,
            winning_player_score
        )
    )

def score_end_of_game(player_rack_list, empty_rack_id=None):
    final_move_score_list = [0 for _ in range(len(player_rack_list))]
    all_rack_points = 0

    for i, player_rack in enumerate(player_rack_list):
        rack_point_total = sum(tile.point_value for tile in player_rack)
        final_move_score_list[i] += (-1 * rack_point_total)
        all_rack_points += rack_point_total

    if empty_rack_id:  # Empty rack player gets all other racks' points
        final_move_score_list[empty_rack_id] += all_rack_points

    return final_move_score_list

def score_move(letter_location_set, board):
    move_location_set = set(location for _, location in letter_location_set)
    word_set = get_word_set(board, move_location_set)
    total_score = get_word_set_total_score(board,
                                           word_set,
                                           len(move_location_set))

    return total_score

def decrement_letter(character):
    return chr(config.LETTER_CODE_DICT[character] - 1)

def increment_letter(character):
    return chr(config.LETTER_CODE_DICT[character] + 1)

def get_current_player_data(move_number, player_rack_list):
    num_players = len(player_rack_list)
    player_to_move_id = move_number % num_players
    player_rack = player_rack_list[player_to_move_id]

    return player_to_move_id, player_rack

def get_word_letter_location_set(word, start_location, is_vertical_move):
    letter_location_set = set()
    next_location_func = get_next_location_function(
        use_positive_seek=True,
        use_vertical_words=is_vertical_move
    )

    current_location = start_location
    word_iterator = iter(word)
    for character in word_iterator:
        if character == '(':  # characters in parenthesis are existing tiles
            character = next(word_iterator, None)
            while character != ')':
                current_location = next_location_func(current_location)
                character = next(word_iterator, None)

            character = next(word_iterator, None)

        if character:
            letter_location_set.add((character, current_location))
            current_location = next_location_func(current_location)

    return letter_location_set

def move_is_legal(board, move_number, letter_location_set, player_rack=None):
    letter_list = [letter for letter, _ in letter_location_set]
    location_set = set(location for _, location in letter_location_set)

    return_bool = (
        move_is_rack_size_or_less(location_set) and
        move_does_not_misalign_tiles(location_set) and
        move_is_not_out_of_bounds(location_set) and
        all_move_tiles_connected(board, location_set) and
        move_does_not_stack_tiles(letter_list, location_set) and
        move_does_not_cover_tiles(board, location_set) and
        move_touches_tile(move_number, board, location_set)
    )

    if player_rack:
        player_rack_letter_list = [tile.letter for tile in player_rack]
        return_bool = return_bool and move_is_sublist(letter_list,
                                                      player_rack_letter_list)

    return return_bool

def move_touches_tile(move_number, board, location_set):
    if move_number == 0:
        if board.start_square_location in location_set:
            return True
    else:
        for this_location in location_set:
            if location_touches_tile(board, this_location):
                return True

    return False

def move_is_sublist(letter_list_1, letter_list_2):
    letter_counter_1 = collections.Counter(letter_list_1)
    letter_counter_2 = collections.Counter(letter_list_2)
    for letter, cardinality in letter_counter_1.items():
        if cardinality > letter_counter_2[letter]:
            return False

    return True

def move_does_not_cover_tiles(board, location_set):
    for location in location_set:
        if board[location]:
            return False

    return True

def all_move_tiles_connected(board, location_set):
    column_list = [column for column, _ in location_set]
    row_list = [row for _, row in location_set]
    move_is_vertical = (len(set(column_list)) == 1)

    if move_is_vertical:
        this_column = column_list[0]
        for this_row in range(min(row_list), max(row_list) + 1):
            this_tile = board[(this_column, this_row)]
            if not (this_tile or (this_column, this_row) in location_set):
                return False
    else:
        column_range = range(
            config.LETTER_CODE_DICT[min(column_list)],
            config.LETTER_CODE_DICT[max(column_list)] + 1
        )

        this_row = row_list[0]
        for this_column_num in column_range:
            this_column = chr(this_column_num)
            this_tile = board[(this_column, this_row)]
            if not (this_tile or (this_column, this_row) in location_set):
                return False

    return True

def move_does_not_misalign_tiles(location_set):
    column_set = set(column for column, _ in location_set)
    row_set = set(row for _, row in location_set)

    return len(column_set) == 1 or len(row_set) == 1

def move_does_not_stack_tiles(letter_list, location_set):
    return len(letter_list) == len(location_set)

def move_is_rack_size_or_less(location_set):
    return len(location_set) <= config.PLAYER_RACK_SIZE

def move_is_not_out_of_bounds(location_set):
    for location in location_set:
        if location_is_out_of_bounds(location):
            return False

    return True

def move_successfully_challenged():
    response = input('Challenge successful (Y/N)')
    if response.upper() == 'Y':
        return True
    elif response.upper() == 'N':
        return False
    else:
        return move_successfully_challenged()

def location_is_out_of_bounds(location):
    column, row = location
    return (
        config.LETTER_CODE_DICT[column] < config.LOWER_COLUMN_INT_BOUND or
        config.LETTER_CODE_DICT[column] > config.UPPER_COLUMN_INT_BOUND or
        row < 1 or
        row > config.BOARD_NUM_ROWS
    )

def location_touches_tile(board, location):
    adjacent_location_set = get_adjacent_location_set(location)
    for adjacent_location in adjacent_location_set:
        if board[adjacent_location]:
            return True

    return False

def get_rack_tile_index(player_rack, move_letter):
    for i, rack_tile in enumerate(player_rack):
        if rack_tile.letter == move_letter:
            return i

    return None

def get_new_tile_bag():
    return [scrabble_game.ScrabbleTile(letter=letter)
            for letter, magnitude in config.LETTER_DISTRIBUTION_DICT.items()
            for _ in range(magnitude)]

def get_next_location_function(use_positive_seek, use_vertical_words):
    if use_vertical_words and use_positive_seek:
        return lambda x: (x[0], x[1] + 1)
    elif use_vertical_words and not use_positive_seek:
        return lambda x: (x[0], x[1] - 1)
    elif not use_vertical_words and use_positive_seek:
        return lambda x: (increment_letter(x[0]), x[1])
    elif not use_vertical_words and not use_positive_seek:
        return lambda x: (decrement_letter(x[0]), x[1])

def get_adjacent_location_set(location):
    column, row = location

    adjacent_location_set = set([(increment_letter(column), row),
                                 (decrement_letter(column), row),
                                 (column, row + 1),
                                 (column, row - 1)])
    # Board boundary check
    bad_location_set = set(location for location in adjacent_location_set
                           if location_is_out_of_bounds(location))

    return adjacent_location_set - bad_location_set

def get_word_location_set(board, initial_location, use_vertical_words):
    word_location_set = set()

    for use_positive_seek in [True, False]:  # Search tiles in 2 directions:
        current_location = initial_location  # either up/down or left/right
        current_tile = board[current_location]
        next_location_func = get_next_location_function(use_positive_seek,
                                                        use_vertical_words)

        while current_tile:
            word_location_set.add(current_location)
            current_location = next_location_func(current_location)
            if location_is_out_of_bounds(current_location):
                current_tile = None
            else:
                current_tile = board[current_location]

    if len(word_location_set) > 1:  # Must be at least 2 letters to be a word
        return frozenset(word_location_set)  # Must be hashable so we can have
    else:                                    # a set of frozensets
        return frozenset()

def get_word_set(board, move_location_set):
    return set(
        get_word_location_set(board, location, use_vertical_words=vertical_bool)
        for vertical_bool in [True, False]  # Search for vertical words created
        for location in move_location_set   # then for horizontal words
    )

def get_word_set_total_score(board, word_set, num_move_locations):
    total_score = 0
    word_score = 0

    for word_location_set in word_set:
        word_score = 0
        word_multiplier = 1
        this_word_str = ''

        for location in word_location_set:
            square = board.board_square_dict[location]
            word_multiplier *= square.word_multiplier
            word_score += square.tile.point_value * square.letter_multiplier
            this_word_str += square.tile.letter

        word_score *= word_multiplier
        total_score += word_score

    if num_move_locations == config.PLAYER_RACK_SIZE:
        total_score += config.BINGO_SCORE

    return total_score
