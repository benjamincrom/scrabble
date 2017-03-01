'''
scrabble_board.py -- contain classes that model scrabble board
'''
import config

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
