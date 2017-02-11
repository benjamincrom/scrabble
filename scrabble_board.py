#!/usr/bin/python
'''
scrabble_board.py -- contain class that models scrabble board and game
'''
import collections
import random

import config

def is_sublist(list_1, list_2):
    counter_1 = collections.Counter(list_1)
    counter_2 = collections.Counter(list_2)
    for value, cardinality in counter_1.items():
        if cardinality > counter_2[value]:
            return False

    return True


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


class Tile(object):
    def __init__(self, letter, point_value):
        self.letter = letter
        self.point_value = point_value

    def __repr__(self):
        return self.letter


class Board(object):
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
            ['_' for _ in range(15)]
            for _ in range(15)
        ]

        for i in range(15):
            for j in range(15):
                board_array[j][i] = next(square_letter_gen)

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


class Game(object):
    def __init__(self, num_players):
        self.num_players = num_players
        self.tile_bag = self.initialize_tile_bag()
        self.player_rack_list = self.initialize_player_racks()
        self.board = Board()
        self.move_number = 0

    def move_is_legal(self, letter_location_list, player_rack):
        player_rack_letter_list = [tile.letter for tile in player_rack]
        move_letter_list = [letter for letter, _ in letter_location_list]
        move_location_list = [location for _, location in letter_location_list]

        return_value = True
        for location in move_location_list:
            if self.board[location].tile:
                return_value = False

        if not is_sublist(move_letter_list, player_rack_letter_list):
            return_value = False

        return return_value

    def next_player_move(self, letter_location_list):
        player_to_move = self.move_number % self.num_players
        player_rack = self.player_rack_list[player_to_move]

        if self.move_is_legal(letter_location_list, player_rack):
            for move_letter, board_location in letter_location_list:
                tile_index = self.get_rack_tile_index(player_rack, move_letter)
                self.place_tile(player_rack, tile_index, board_location)

            while len(player_rack) < 7:
                player_rack.append(self.draw_random_tile())

            self.move_number += 1
            success = True
        else:
            success = False

        return success

    @staticmethod
    def get_rack_tile_index(player_rack, move_letter):
        for i, rack_tile in enumerate(player_rack):
            if rack_tile.letter == move_letter:
                return i

        return None

    def place_tile(self, player_rack, rack_tile_index, board_location):
        ''' Takes format of rack_tile_index, board_location '''
        tile = player_rack.pop(rack_tile_index)
        self.board[board_location] = tile

    def draw_random_tile(self):
        random_index = random.randrange(0, len(self.tile_bag))
        return self.tile_bag.pop(random_index)

    def initialize_player_racks(self):
        player_rack_list = []
        for _ in range(self.num_players):
            this_rack = [self.draw_random_tile() for _ in range(7)]
            player_rack_list.append(this_rack)

        return player_rack_list

    @staticmethod
    def initialize_tile_bag():
        tile_bag = []
        for letter, magnitude in config.LETTER_DISTRIBUTION_DICT.items():
            for _ in range(magnitude):
                tile_bag.append(
                    Tile(letter=letter,
                         point_value=config.LETTER_POINT_VALUES_DICT[letter])
                )

        return tile_bag


g = Game(4)
print g.board
print g.player_rack_list
