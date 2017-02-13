'''
scrabble_game.py -- contains classes that model scrabble moves
'''
import collections
import random

import config
import scrabble_board

def decrement_letter(character):
    return chr(ord(character) - 1)

def increment_letter(character):
    return chr(ord(character) + 1)

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
                '{} tiles remain in bag\n'
                'Player 1: {}\n'
                'Player 2: {}\n'
                'Player 3: {}\n'
                'Player 4: {}\n').format(
                    str(self.board),
                    self.player_rack_list,
                    self.move_number,
                    (self.move_number % self.num_players) + 1,
                    len(self.tile_bag),
                    sum(self.player_move_score_list_list[0]),
                    sum(self.player_move_score_list_list[1]),
                    sum(self.player_move_score_list_list[2]),
                    sum(self.player_move_score_list_list[3])
                )

    def get_horizontal_word_location_set(self, location):
        horizontal_word_location_set = set([location])

        current_location = location  # Look left
        current_tile = self.board[current_location].tile

        while current_tile:
            horizontal_word_location_set.add(current_location)

            if ord(current_location[0]) > ord('a'):
                current_location = (decrement_letter(current_location[0]),
                                    current_location[1])

                current_tile = self.board[current_location].tile
            else:
                current_tile = None

        current_location = location  # Look right
        current_tile = self.board[current_location].tile

        while current_tile:
            horizontal_word_location_set.add(current_location)

            if ord(current_location[0]) < ord('o'):
                current_location = (increment_letter(current_location[0]),
                                    current_location[1])

                current_tile = self.board[current_location].tile
            else:
                current_tile = None

        if len(horizontal_word_location_set) > 1:
            return frozenset(horizontal_word_location_set)
        else:
            return None

    def get_vertical_word_location_set(self, location):
        vertical_word_location_set = set([location])

        current_location = location  # Look up
        current_tile = self.board[current_location].tile

        while current_tile:
            vertical_word_location_set.add(current_location)

            if current_location[1] > 1:
                current_location = (current_location[0],
                                    current_location[1] - 1)

                current_tile = self.board[current_location].tile
            else:
                current_tile = None

        current_location = location  # Look down
        current_tile = self.board[current_location].tile

        while current_tile:
            vertical_word_location_set.add(current_location)

            if current_location[1] < 15:
                current_location = (current_location[0],
                                    current_location[1] + 1)

                current_tile = self.board[current_location].tile
            else:
                current_tile = None

        if len(vertical_word_location_set) > 1:
            return frozenset(vertical_word_location_set)
        else:
            return None

    def score_move(self, letter_location_set):
        move_location_set = set(
            (location for _, location in letter_location_set)
        )

        word_location_set_set = set([])
        for location in move_location_set:
            if self.board[location].tile:
                location_set = self.get_vertical_word_location_set(location)
                if location_set:
                    word_location_set_set.add(location_set)

                location_set = self.get_horizontal_word_location_set(location)
                if location_set:
                    word_location_set_set.add(location_set)

        score = sum(
            (self.board[location].tile.point_value
             for word_location_set in word_location_set_set
             for location in word_location_set)
        )

        return score

    @staticmethod
    def get_adjacent_location_set(location):
        column, row = location

        adjacent_location_set = set(
            [
                (chr(ord(column) + 1), row),
                (chr(ord(column) - 1), row),
                (column, (row + 1)),
                (column, (row - 1))
            ]
        )
        # Board boundary check
        remove_location_set = set(
            (
                (column, row) for column, row in adjacent_location_set
                if (row > 15 or
                    row < 1 or
                    ord(column) > ord('o') or
                    ord(column) < ord('a'))
            )
        )

        return adjacent_location_set - remove_location_set

    def location_touches_tile(self, location, new_tile_location_set):
        adjacent_location_set = self.get_adjacent_location_set(location)

        for adjacent_location in adjacent_location_set:
            adjacent_tile = self.board[adjacent_location].tile
            if adjacent_tile or (adjacent_location in new_tile_location_set):
                return True

        return False

    def move_touches_tile(self, location_set):
        if self.move_number == 0:
            if config.START_SQUARE not in location_set:
                return False
        else:
            new_tile_location_set = set([])
            for this_location in location_set:
                if not self.location_touches_tile(this_location,
                                                  new_tile_location_set):
                    return False
                else:
                    new_tile_location_set.add(this_location)

        return True

    def move_is_legal(self, letter_location_set, player_rack):
        player_rack_letter_list = [tile.letter for tile in player_rack]
        letter_list = [letter for letter, _ in letter_location_set]
        location_set = set((location for _, location in letter_location_set))

        for location in location_set:
            if self.board[location].tile:
                return False

        if not self.move_touches_tile(location_set):
            return False

        if not is_sublist(letter_list, player_rack_letter_list):
            return False

        return True

    def next_player_move(self, letter_location_set):
        player_to_move = self.move_number % self.num_players
        player_rack = self.player_rack_list[player_to_move]

        if self.move_is_legal(letter_location_set, player_rack):
            for move_letter, board_location in letter_location_set:
                tile_index = self.get_rack_tile_index(player_rack, move_letter)
                self.place_tile(player_rack, tile_index, board_location)

            while len(player_rack) < 7:
                player_rack.append(self.draw_random_tile())

            move_score = self.score_move(letter_location_set)
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
