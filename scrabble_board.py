#!/usr/bin/python
'''
scrabble_board.py -- contain classes that model scrabble board
'''
import config


class Tile(object):
    def __init__(self, letter, point_value):
        self.letter = letter
        self.point_value = point_value

    def __repr__(self):
        return self.letter


class Square(object):
    def __init__(self, location, tile, letter_multiplier, word_multiplier):
        self.location = location
        self.tile = tile
        self.letter_multiplier = letter_multiplier
        self.word_multiplier = word_multiplier

    def __repr__(self):
        if self.tile:
            return_value = str(self.tile)
        else:
            return_value = '_'

        return return_value


class ScrabbleBoard(object):
    def __init__(self):
        self.square_dict = self.initialize_square_dict()

    def __getitem__(self, key):
        return self.square_dict.get(key)

    def __setitem__(self, key, val):
        self.square_dict[key] = val

    def __repr__(self):
        square_letter_gen = (str(square[1])
                             for square in sorted(self.square_dict.items()))

        board_array = [
            [' ' for _ in range(17)]
            for _ in range(17)
        ]

        board_array[0] = [
            ' ', ' ', '1', '2', '3', '4', '5', '6', '7', '8', '9', '0', '1',
            '2', '3', '4', '5'
        ]

        for i in range(2, 17):
            board_array[i][0] = chr(ord('a')-2 + i)
            for j in range(2, 17):
                board_array[j][i] = next(square_letter_gen)

        if board_array[9][9] == '_':
            board_array[9][9] = '★'

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
    def initialize_square_dict(cls):
        initial_square_dict = {}
        for column in 'abcdefghijlkmno':
            for row in range(1, 16):
                word_multiplier = cls.get_location_word_mutliplier(column, row)
                letter_multiplier = cls.get_location_letter_multiplier(column,
                                                                       row)

                initial_square_dict[(column, row)] = Square(
                    location=(column, row),
                    tile=None,
                    word_multiplier=word_multiplier,
                    letter_multiplier=letter_multiplier
                )

        return initial_square_dict
