#!/usr/bin/python
'''
scrabble_board.py -- contain classes that model scrabble board
'''
import config

def character_range(character_1, character_2):
    """Generates the characters from `c1` to `c2`, inclusive."""
    for this_character_ord in range(ord(character_1), ord(character_2)):
        yield chr(this_character_ord)


class ScrabbleTile(object):
    def __init__(self, letter, point_value):
        self.letter = letter
        self.point_value = point_value

    def __repr__(self):
        return self.letter


class BoardSquare(object):
    def __init__(self, location, tile, letter_multiplier, word_multiplier):
        self.location = location
        self.tile = tile
        self.letter_multiplier = letter_multiplier
        self.word_multiplier = word_multiplier

    def __repr__(self):
        if self.tile:
            return_value = str(self.tile)
        else:
            return_value = config.BLANK_SQUARE_CHARACTER

        return return_value


class ScrabbleBoard(object):
    def __init__(self):
        self.board_square_dict = self.initialize_board_square_dict()

    def __getitem__(self, key):
        return self.board_square_dict.get(key)

    def __setitem__(self, key, val):
        self.board_square_dict[key] = val

    def __repr__(self):
        square_letter_gen = (
            str(square[1]) for square in sorted(self.board_square_dict.items())
        )

        board_array = [
            [' ' for _ in range(17)]
            for _ in range(17)
        ]

        # Column labels
        board_array[0] = [' ', ' ']
        board_array[0].extend(character_range('a', 'p'))

        # Shrink empty spaces to make room for two-digit row numbers
        for i in range(2, 17):
            board_array[i][0] = str(i - 1)
            if i - 1 > 9:
                board_array[i][1] = ''

            for j in range(2, 17):
                board_array[j][i] = next(square_letter_gen)

        if board_array[9][9] == config.BLANK_SQUARE_CHARACTER:
            board_array[9][9] = config.START_SQUARE_CHARACTER

        return_line_list = [''.join(row) for row in board_array]
        return_str = '\n'.join(return_line_list)

        return return_str

    @staticmethod
    def get_location_word_mutliplier(column, row):
        if (column, row) in config.DOUBLE_WORD_SCORE_LOCATION_LIST:
            word_multiplier = 2
        elif (column, row) in config.TRIPLE_WORD_SCORE_LOCATION_LIST:
            word_multiplier = 3
        else:
            word_multiplier = 1

        return word_multiplier

    @staticmethod
    def get_location_letter_multiplier(column, row):
        if (column, row) in config.DOUBLE_LETTER_SCORE_LOCATION_LIST:
            letter_multiplier = 2
        elif (column, row) in config.TRIPLE_LETTER_SCORE_LOCATION_LIST:
            letter_multiplier = 3
        else:
            letter_multiplier = 1

        return letter_multiplier

    @classmethod
    def initialize_board_square_dict(cls):
        initial_board_square_dict = {}
        for column in 'abcdefghijlkmno':
            for row in range(1, 16):
                word_multiplier = cls.get_location_word_mutliplier(column, row)
                letter_multiplier = cls.get_location_letter_multiplier(column,
                                                                       row)

                initial_board_square_dict[(column, row)] = BoardSquare(
                    location=(column, row),
                    tile=None,
                    word_multiplier=word_multiplier,
                    letter_multiplier=letter_multiplier
                )

        return initial_board_square_dict
