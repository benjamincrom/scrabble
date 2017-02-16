#!/usr/bin/python
'''
scrabble_board.py -- contain classes that model scrabble board
'''
import config

def character_range(character_1, character_2):
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

    def __repr__(self):
        square_letter_gen = (
            str(square[1]) for square in sorted(self.board_square_dict.items())
        )

        board_array_first_row = [' ', ' '] + list(character_range('a', 'p'))
        board_array = [board_array_first_row]  # Column labels
        board_array.extend(
            ([' ' for _ in range(17)] for _ in range(15))
        )

        for i in range(1, 16):
            board_array[i][0] = str(i)  # Row labels
            if i > 9:
                board_array[i][1] = ''  # Shrink empty spaces to make room for
                                        # two-digit row numbers
            for j in range(2, 17):
                board_array[j-1][i+1] = next(square_letter_gen) # swap x and y

        if board_array[8][9] == config.BLANK_SQUARE_CHARACTER:
            board_array[8][9] = config.START_SQUARE_CHARACTER

        return_line_list = [''.join(row) for row in board_array]
        return_str = '\n'.join(return_line_list)

        return return_str

    @staticmethod
    def get_location_word_mutliplier(location):
        column, row = location

        if (column, row) in config.DOUBLE_WORD_SCORE_LOCATION_LIST:
            word_multiplier = 2
        elif (column, row) in config.TRIPLE_WORD_SCORE_LOCATION_LIST:
            word_multiplier = 3
        else:
            word_multiplier = 1

        return word_multiplier

    @staticmethod
    def get_location_letter_multiplier(location):
        column, row = location

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
        for column in character_range('a', 'p'):
            for row in range(1, 16):
                location = (column, row)
                word_multiplier = cls.get_location_word_mutliplier(location)
                letter_multiplier = cls.get_location_letter_multiplier(location)

                initial_board_square_dict[(column, row)] = BoardSquare(
                    location=location,
                    tile=None,
                    word_multiplier=word_multiplier,
                    letter_multiplier=letter_multiplier
                )

        return initial_board_square_dict
