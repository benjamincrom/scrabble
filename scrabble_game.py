'''
scrabble_game.py -- contains classes that model scrabble moves
'''
import collections
import random

import config
import scrabble_board


def is_sublist(list_1, list_2):
    counter_1 = collections.Counter(list_1)
    counter_2 = collections.Counter(list_2)
    for value, cardinality in counter_1.items():
        if cardinality > counter_2[value]:
            return False

    return True


class ScrabbleGame(object):
    def __init__(self, num_players):
        self.num_players = num_players
        self.tile_bag = self.initialize_tile_bag()
        self.player_rack_list = self.initialize_player_racks()
        self.board = scrabble_board.ScrabbleBoard()
        self.player_move_score_list_list = [[] for _ in range(num_players)]
        self.move_number = 0

    def __repr__(self):
        return ('{}\n'
                '{}\n'
                'Moves played: {}\n'
                'Player {}\'s move\n'
                '{} tiles remain in bag').format(
                    str(self.board),
                    self.player_rack_list,
                    self.move_number,
                    (self.move_number % self.num_players) + 1,
                    len(self.tile_bag)
                )

    def score_move(self, letter_location_list):
        return 0

    def location_touches_tile(self, location):
        column, row = location
        adjacent_location_list = [
            (chr(ord(column) + 1), row),
            (chr(ord(column) - 1), row),
            (column, (row + 1)),
            (column, (row - 1))
        ]

        return_value = False
        for adjacent_location in adjacent_location_list:
            if self.board[adjacent_location].tile:
                return_value = True

        return return_value

    def move_touches_tile(self, location_list):
        return_value = True
        if self.move_number == 0:
            if ('h', 7) not in location_list:
                return_value = False
        else:
            for this_location in location_list:
                if not self.location_touches_tile(this_location):
                    return_value = False

        return return_value


    def move_is_legal(self, letter_location_list, player_rack):
        player_rack_letter_list = [tile.letter for tile in player_rack]
        letter_list = [letter for letter, _ in letter_location_list]
        location_list = [location for _, location in letter_location_list]

        return_value = True

        for location in location_list:
            if self.board[location].tile:
                return_value = False

        if not self.move_touches_tile(location_list):
            return_value = False

        if not is_sublist(letter_list, player_rack_letter_list):
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

            move_score = self.score_move(letter_location_list)
            self.player_move_score_list_list[player_to_move].append(move_score)
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
        self.board[board_location].tile = tile

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
                    scrabble_board.Tile(
                        letter=letter,
                        point_value=config.LETTER_POINT_VALUES_DICT[letter]
                    )
                )

        return tile_bag
