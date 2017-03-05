"""
main.py -- contains classes that model scrabble game
"""
import random

import config
import helpers


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
        self.board_square_dict = helpers.initialize_new_board_square_dict()

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
        self.tile_bag = helpers.get_new_tile_bag()
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
