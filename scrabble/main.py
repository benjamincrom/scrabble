"""
main.py -- contains classes that model scrabble game
"""
import itertools
import multiprocessing
import random

from . import config
from . import helpers

def get_move_set_generator(new_game, reference_game, move_list):
    legal_move_set = get_legal_move_set(new_game, reference_game)
    player_to_move_id = new_game.move_number % len(new_game.player_rack_list)
    player_score_list = reference_game.player_score_list_list[
        player_to_move_id
    ]

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
        new_game_copy.next_player_move(next_move, False)
        move_list_copy.append(next_move)

        if new_game_copy.move_number == reference_game.move_number:
            if helpers.boards_are_equivalent(reference_game.board,
                                             new_game_copy.board):
                yield move_list_copy

        else:
            yield from get_move_set_generator(new_game_copy,
                                              reference_game,
                                              move_list_copy)

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

    process_pool = multiprocessing.Pool(config.NUM_PROCESSING_CORES)
    result_list = process_pool.map(get_location_best_move_helper,
                                   input_arguments_list)

    return max(result_list)


def get_location_best_move_helper(argument_list):
    return get_location_best_move(*argument_list)

def get_location_best_move(game, location, word_list):
    player_to_move_id = game.move_number % len(game.player_rack_list)

    high_score = 0
    best_move = None
    for word in word_list:
        for is_vertical in [True, False]:
            temp_game = copy_game(game)
            if temp_game.place_word(word, location, is_vertical, False):
                letter_location_set = (
                    helpers.get_word_letter_location_set(
                        word,
                        location,
                        is_vertical
                    )
                )

                location_set = set(location
                                   for _, location in letter_location_set)

                if helpers.all_created_words_are_english(temp_game.board,
                                                         location_set):
                    player_score_list = (
                        temp_game.player_score_list_list[player_to_move_id]
                    )

                    word_score = player_score_list[-1]
                    if word_score > high_score:
                        best_move = (location, word, is_vertical)
                        high_score = word_score

    return high_score, best_move

def get_legal_move_set(new_game, reference_game):
    all_possible_moves_set = helpers.get_all_possible_moves_set(new_game,
                                                                reference_game)

    legal_move_set = set()
    for move_set in all_possible_moves_set:
        if helpers.move_is_legal(new_game.board,
                                 new_game.move_number,
                                 move_set):
            temp_board = copy_board(new_game.board)
            for tile, location in move_set:
                temp_board[location] = tile

            legal_move_set.add(
                (helpers.score_move(move_set, temp_board), move_set)
            )

    return legal_move_set

def copy_board(input_board):
    input_square_dict = input_board.board_square_dict

    new_board = ScrabbleBoard()
    new_square_dict = new_board.board_square_dict

    for location, square in input_square_dict.items():
        if square.tile:
            new_board_square = new_square_dict[location]
            new_board_square.letter_multiplier = square.letter_multiplier
            new_board_square.word_multiplier = square.word_multiplier
            new_board_square.tile = ScrabbleTile(
                square.tile.letter
            )

    return new_board

def copy_game(input_game):
    new_game = ScrabbleGame(len(input_game.player_rack_list))
    new_game.board = copy_board(input_game.board)
    new_game.move_number = input_game.move_number
    new_game.player_score_list_list = [
        input_player_score_list[:]
        for input_player_score_list in input_game.player_score_list_list
    ]

    new_player_rack_list = []
    for player_rack in input_game.player_rack_list:
        new_rack = []
        for tile in player_rack:
            new_rack.append(ScrabbleTile(tile.letter))

        new_player_rack_list.append(new_rack)

    new_game.player_rack_list = new_player_rack_list

    return new_game

def get_move_set_notation(move_set, reference_game):
    new_game = ScrabbleGame(len(reference_game.player_rack_list))
    word_notation_list_list = [
        [] for _ in range(len(reference_game.player_rack_list))
    ]

    for move in move_set:
        player_to_move_id = (
            new_game.move_number % len(new_game.player_rack_list)
        )

        move_location_set = set(location for _, location in move)
        rack_word = ''.join([letter for letter, _ in move])
        new_game.cheat_create_rack_word(rack_word, player_to_move_id)

        player_words_notation_list = (
            word_notation_list_list[player_to_move_id]
        )

        notation_word_list = []
        new_game.next_player_move(move, False)
        word_set = helpers.get_word_set(new_game.board, move_location_set)
        for word_location_set in word_set:
            if word_location_set:
                notation_word_list.append(
                    helpers.get_move_word(word_location_set,
                                          move_location_set,
                                          new_game)
                )

        player_words_notation_list.append(notation_word_list)

    return word_notation_list_list

def get_new_tile_bag():
    return [ScrabbleTile(letter=letter)
            for letter, magnitude in config.LETTER_DISTRIBUTION_DICT.items()
            for _ in range(magnitude)]

def read_input_file(input_filename):
    board_character_array, player_score_list_list = helpers.load_file(
        input_filename
    )

    num_players = len(player_score_list_list)
    game = ScrabbleGame(num_players)
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
                game.board[this_location] = ScrabbleTile(letter)

    return game

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

            initial_board_square_dict[location] = BoardSquare(
                tile=None,
                word_multiplier=word_multiplier,
                letter_multiplier=letter_multiplier
            )

    return initial_board_square_dict

def recover_game(input_filename):
    reference_game = read_input_file(input_filename)
    new_game = ScrabbleGame(
        len(reference_game.player_rack_list)
    )

    move_set_generator = get_move_set_generator(new_game,
                                                reference_game,
                                                [])

    move_set_list = list(move_set_generator)

    notated_move_set_list = [
        get_move_set_notation(move_set, reference_game)
        for move_set in move_set_list
    ]

    return notated_move_set_list


class ScrabbleTile(object):
    def __init__(self, letter):
        self.letter = letter
        self.point_value = config.LETTER_POINT_VALUES_DICT[letter]

    def __repr__(self):
        return self.letter


class BoardSquare(object):
    def __init__(self, tile, letter_multiplier, word_multiplier):
        self.tile = tile
        self.letter_multiplier = letter_multiplier
        self.word_multiplier = word_multiplier

    def __repr__(self):
        if self.tile:
            return str(self.tile)
        else:
            return config.BLANK_SQUARE_CHARACTER


class ScrabbleBoard(object):
    def __init__(self):
        self.board_square_dict = initialize_new_board_square_dict()

        center_row = (config.BOARD_NUM_ROWS // 2) + 1
        center_column = chr(
            (config.BOARD_NUM_COLUMNS // 2) + config.LOWER_COLUMN_INT_BOUND
        )

        self.start_square_location = (center_column, center_row)

    def __getitem__(self, key):
        return self.board_square_dict.get(key).tile

    def __setitem__(self, key, value):
        self.board_square_dict[key].tile = value

    def __repr__(self):
        square_letter_gen = (
            str(square)
            for location, square in sorted(self.board_square_dict.items())
        )

        board_array_first_row = (
            [' ', ' '] + sorted(list(config.BOARD_CODE_DICT.keys()))
        )

        board_array = [board_array_first_row]  # Column labels
        board_array.extend(
            [' ' for _ in range(config.BOARD_NUM_COLUMNS+1)]
            for _ in range(config.BOARD_NUM_ROWS)
        )

        for i in range(1, config.BOARD_NUM_ROWS + 1):
            board_array[i][0] = str(i)  # Row labels
            if i < 10:
                board_array[i][0] += ' '  # Pad single digit numbers with space

            for j in range(1, config.BOARD_NUM_COLUMNS + 1):
                board_array[j][i] = next(square_letter_gen)  # swap x and y

        center_row_num = (config.BOARD_NUM_ROWS // 2) + 1
        center_column_num = (config.BOARD_NUM_COLUMNS // 2) + 1
        start_char = config.START_SQUARE_CHARACTER
        blank_char = config.BLANK_SQUARE_CHARACTER

        if board_array[center_column_num][center_row_num] == blank_char:
            board_array[center_column_num][center_row_num] = start_char

        return_line_list = [''.join(row) for row in board_array]
        return_str = '\n'.join(return_line_list)

        return return_str


class ScrabbleGame(object):
    def __init__(self, num_players):
        self.tile_bag = get_new_tile_bag()
        self.player_rack_list = self._get_new_player_rack_list(num_players)
        self.board = ScrabbleBoard()
        self.player_score_list_list = [[] for _ in range(num_players)]
        self.move_number = 0

    def __repr__(self):
        player_score_str_list = []
        for i, player_score_list in enumerate(self.player_score_list_list):
            player_score_str_list.append(
                'Player {player_number}: {score}'.format(
                    player_number=(i + 1),
                    score=sum(player_score_list)
                )
            )

        player_scores_str = '\n'.join(player_score_str_list)
        player_to_move_id, _ = helpers.get_current_player_data(
            self.move_number,
            self.player_rack_list
        )

        return (
            '{board}\n'
            '{player_rack_list}\n'
            'Moves played: {move_number}\n'
            'Player {player_to_move}\'s move\n'
            '{tiles_remaining} tiles remain in bag\n'
            '{player_scores_str}'
        ).format(
            board=str(self.board),
            player_rack_list=self.player_rack_list,
            move_number=self.move_number,
            player_to_move=player_to_move_id + 1,
            tiles_remaining=len(self.tile_bag),
            player_scores_str=player_scores_str
        )

    def exchange(self, letter_list):
        if (len(self.tile_bag) < config.PLAYER_RACK_SIZE or
                len(letter_list) > config.PLAYER_RACK_SIZE):
            return False
        else:
            _, player_rack = helpers.get_current_player_data(
                self.move_number,
                self.player_rack_list
            )

            player_letter_list = [tile.letter for tile in player_rack]

            if helpers.move_is_sublist(letter_list, player_letter_list):
                self._perform_bag_exchange(letter_list, player_rack)
                self.move_number += 1
                return True
            else:
                return False

    def place_word(self, word, start_location, is_vertical_move,
                   allow_challenge=True):
        letter_location_set = helpers.get_word_letter_location_set(
            word,
            start_location,
            is_vertical_move
        )

        return self.next_player_move(letter_location_set, allow_challenge)

    def next_player_move(self, letter_location_set, allow_challenge=True):
        player_to_move_id, player_rack = helpers.get_current_player_data(
            self.move_number,
            self.player_rack_list
        )

        is_legal_move = helpers.move_is_legal(self.board,
                                              self.move_number,
                                              letter_location_set,
                                              player_rack)

        if is_legal_move:
            if allow_challenge and helpers.move_successfully_challenged():
                letter_location_set = set()

            for move_letter, board_location in letter_location_set:
                tile_index = helpers.get_rack_tile_index(player_rack,
                                                         move_letter)

                tile_obj = player_rack.pop(tile_index)
                self.board[board_location] = tile_obj

            move_score = helpers.score_move(letter_location_set, self.board)
            self.player_score_list_list[player_to_move_id].append(move_score)
            self._refill_player_rack(player_rack)
            self._cancel_bonus_squares(letter_location_set)

            if len(player_rack) == 0 and len(self.tile_bag) == 0:  # Final move
                last_move_score_list = helpers.score_end_of_game(
                    self.player_rack_list,
                    player_to_move_id
                )

                for i, last_move_score in enumerate(last_move_score_list):
                    self.player_score_list_list[i].append(last_move_score)

                helpers.conclude_game(self.player_score_list_list)

            self.move_number += 1
            return True
        else:
            return False

    def cheat_create_rack_word(self, word, player_id):
        player_rack = self.player_rack_list[player_id]
        for character in word:
            tile = ScrabbleTile(letter=character)
            player_rack.append(tile)

    def _get_new_player_rack_list(self, num_players):
        player_rack_list = []

        for _ in range(num_players):
            this_rack = []
            for _ in range(config.PLAYER_RACK_SIZE):
                this_tile = self._draw_random_tile()
                this_rack.append(this_tile)

            player_rack_list.append(this_rack)

        return player_rack_list

    def _draw_random_tile(self):
        random_index = random.randrange(0, len(self.tile_bag))
        selected_tile = self.tile_bag.pop(random_index)

        return selected_tile

    def _refill_player_rack(self, player_rack):
        while len(player_rack) < config.PLAYER_RACK_SIZE:
            if self.tile_bag:
                tile = self._draw_random_tile()
                player_rack.append(tile)
            else:
                break

    def _cancel_bonus_squares(self, letter_location_set):
        for _, location in letter_location_set:
            square = self.board.board_square_dict[location]
            square.letter_multiplier = 1
            square.word_multiplier = 1

    def _perform_bag_exchange(self, letter_list, player_rack):
        exchange_tile_list = []
        for letter in letter_list:
            for tile in player_rack:
                if tile.letter == letter:
                    exchange_tile_list.append(tile)
                    player_rack.remove(tile)

        for _ in range(len(letter_list)):
            new_tile = self._draw_random_tile()
            player_rack.append(new_tile)

        self.tile_bag.extend(exchange_tile_list)
