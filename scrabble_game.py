'''
scrabble_game.py -- contains classes that model scrabble moves
'''
import collections
import operator
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
            player_to_move=(self.move_number % self.num_players) + 1,
            tiles_remaining=len(self.tile_bag),
            player_scores_str=player_scores_str
        )

    def get_current_player_data(self):
        player_to_move = self.move_number % self.num_players
        player_rack = self.player_rack_list[player_to_move]

        return player_to_move, player_rack

    def mock_place_word(self, word, start_location, is_vertical_move):
        self.tile_bag = self.initialize_tile_bag()  # Refill tile bag
        letter_location_set = set([])

        _, player_rack = self.get_current_player_data()

        next_location_function = self.get_next_location_function(
            use_positive_seek=True,
            use_vertical_words=is_vertical_move
        )

        current_location = start_location
        for character in word:
            for tile in self.tile_bag:
                if character == tile.letter:
                    player_rack.append(tile)
                    letter_location_set.add((character, current_location))
                    self.board[current_location].tile = None
                    current_location = next_location_function(current_location)
                    break

        return self.next_player_move(letter_location_set)

    def conclude_game(self, empty_rack_id=None):
        all_rack_points = 0

        for i, player_rack in enumerate(self.player_rack_list):
            rack_point_total = sum((tile.point_value for tile in player_rack))
            this_player_score_list = self.player_score_list_list[i]
            this_player_score_list.append(-1 * rack_point_total)
            all_rack_points += rack_point_total

        if empty_rack_id:  # Empty rack player gets all other racks' points
            empty_player_score_list = self.player_score_list_list[empty_rack_id]
            empty_player_score_list.append(all_rack_points)

        player_score_total_list = [
            sum(player_score_list)
            for player_score_list in self.player_score_list_list
        ]

        winning_player_id, winning_player_score = max(
            enumerate(player_score_total_list), key=operator.itemgetter(1)
        )

        print(
            'Game Over! Player {} wins with a score of {}'.format(
                winning_player_id + 1,
                winning_player_score
            )
        )

    @staticmethod
    def get_next_location_function(use_positive_seek, use_vertical_words):
        if use_vertical_words and use_positive_seek:
            return lambda x: (x[0], x[1] + 1)
        elif use_vertical_words and not use_positive_seek:
            return lambda x: (x[0], x[1] - 1)
        elif not use_vertical_words and use_positive_seek:
            return lambda x: (increment_letter(x[0]), x[1])
        elif not use_vertical_words and not use_positive_seek:
            return lambda x: (decrement_letter(x[0]), x[1])
        else:
            raise ValueError('Incorrect input.')

    def get_word_location_set(self, location, use_vertical_words):
        word_location_set = set([])

        for use_positive_seek in [True, False]:  # Search tiles in 2 directions:
            current_location = location          # either up/down or left/right
            current_tile = self.board[current_location].tile

            next_location_function = self.get_next_location_function(
                use_positive_seek,
                use_vertical_words
            )

            while current_tile:
                word_location_set.add(current_location)
                current_location = next_location_function(current_location)

                if (ord(current_location[0]) >= ord('a') and  # bounds check
                        ord(current_location[0]) <= ord('o') and
                        current_location[1] >= 1 and
                        current_location[1] <= 15):
                    current_tile = self.board[current_location].tile
                else:
                    current_tile = None

        if len(word_location_set) > 1:           # Must be at least 2 letters to
            return frozenset(word_location_set)  # count as a word
        else:
            return frozenset([])

    def get_word_set(self, move_location_set):
        word_set = set([])

        for use_vertical_words in [True, False]:  # Search for vertical words
            for location in move_location_set:    # created, then horizontal
                word_set.add(
                    self.get_word_location_set(
                        location,
                        use_vertical_words=use_vertical_words
                    )
                )

        return word_set

    def get_word_set_total_score(self, word_set, num_move_locations):
        total_score = 0
        word_score = 0

        for word_location_set in word_set:
            word_score = 0
            word_multiplier = 1

            for location in word_location_set:
                square = self.board[location]
                word_multiplier *= square.word_multiplier
                word_score += square.tile.point_value * square.letter_multiplier
                square.letter_multiplier = 1
                square.word_multiplier = 1

            word_score *= word_multiplier
            total_score += word_score

        if num_move_locations == 7:
            total_score += 50  # Bingo

        return total_score

    def score_move(self, letter_location_set):
        move_location_set = set(
            (location for _, location in letter_location_set)
        )

        word_set = self.get_word_set(move_location_set)

        total_score = self.get_word_set_total_score(
            word_set,
            len(move_location_set)
        )

        return total_score

    @staticmethod
    def get_adjacent_location_set(location):
        column, row = location

        adjacent_location_set = set(
            [
                (increment_letter(column), row),
                (decrement_letter(column), row),
                (column, row + 1),
                (column, row - 1)
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

    def location_touches_tile(self, location):
        adjacent_location_set = self.get_adjacent_location_set(location)
        for adjacent_location in adjacent_location_set:
            if self.board[adjacent_location].tile:
                return True

        return False

    def move_touches_tile(self, location_set):
        if self.move_number == 0:
            if config.START_SQUARE not in location_set:
                return False
        else:
            for this_location in location_set:
                if self.location_touches_tile(this_location):
                    return True

        return False

    @staticmethod
    def move_is_not_out_of_bounds(location_set):
        for column, row in location_set:
            if (ord(column) < ord('a') or
                    ord(column) > ord('o') or
                    row < 1 or
                    row > 15):
                return False

        return True

    @staticmethod
    def move_does_not_stack_tiles(letter_list, location_set):
        return len(letter_list) == len(location_set)

    def move_does_not_misalign_tiles(self, location_set):
        # All tiles places are in one row or one column
        column_list = [location[0] for location in location_set]
        row_list = [location[1] for location in location_set]

        if len(set(column_list)) == 1:
            is_vertical_move = True
        elif len(set(row_list)) == 1:
            is_vertical_move = False
        else:
            return False

         # All tiles must be connected
        if is_vertical_move:
            this_column = list(location_set)[0][0]
            for this_row in range(min(row_list), max(row_list) + 1):
                this_tile = self.board[(this_column, this_row)].tile
                if not (this_tile or (this_column, this_row) in location_set):
                    return False
        else:
            this_row = list(location_set)[0][1]
            for this_column_num in range(ord(min(column_list)),
                                         ord(max(column_list)) + 1):
                this_column = chr(this_column_num)
                this_tile = self.board[(this_column, this_row)].tile
                if not (this_tile or (this_column, this_row) in location_set):
                    return False

        return True

    def move_does_not_cover_tiles(self, location_set):
        for location in location_set:
            if self.board[location].tile:
                return False

        return True

    def move_is_legal(self, letter_location_set, player_rack):
        player_rack_letter_list = [tile.letter for tile in player_rack]
        letter_list = [letter for letter, _ in letter_location_set]
        location_set = set((location for _, location in letter_location_set))

        success = (
            self.move_is_not_out_of_bounds(location_set) and
            is_sublist(letter_list, player_rack_letter_list) and
            self.move_does_not_stack_tiles(letter_list, location_set) and
            self.move_does_not_misalign_tiles(location_set) and
            self.move_does_not_cover_tiles(location_set) and
            self.move_touches_tile(location_set)
        )

        return success

    def next_player_move(self, letter_location_set):
        player_to_move, player_rack = self.get_current_player_data()

        if self.move_is_legal(letter_location_set, player_rack):
            for move_letter, board_location in letter_location_set:
                tile_index = self.get_rack_tile_index(player_rack, move_letter)
                tile_obj = self.pop_player_rack_tile(player_rack, tile_index)
                self.place_tile(tile_obj, board_location)

            while len(player_rack) < 7:
                if self.tile_bag:
                    player_rack.append(self.draw_random_tile())
                else:
                    break

            move_score = self.score_move(letter_location_set)
            player_score_list = self.player_score_list_list[player_to_move]
            player_score_list.append(move_score)

            if len(player_rack) == 0 and len(self.tile_bag) == 0:
                self.conclude_game(player_to_move)

            self.move_number += 1
            success = True
        else:
            success = False

        return success

    def next_player_exchange(self, letter_list):
        if len(self.tile_bag) < 7 or len(letter_list) > 7:
            return False

        _, player_rack = self.get_current_player_data()

        exchange_tile_list = []
        for letter in letter_list:
            for tile in player_rack:
                if tile.letter == letter:
                    exchange_tile_list.append(tile)

        for _ in range(len(letter_list)):
            player_rack.append(self.draw_random_tile())

        for tile in exchange_tile_list:
            if tile not in player_rack:
                return False
            else:
                player_rack.remove(tile)

        self.tile_bag.extend(exchange_tile_list)
        self.move_number += 1

        return True

    @staticmethod
    def get_rack_tile_index(player_rack, move_letter):
        for i, rack_tile in enumerate(player_rack):
            if rack_tile.letter == move_letter:
                return i

        return None

    @staticmethod
    def pop_player_rack_tile(player_rack, rack_tile_index):
        return player_rack.pop(rack_tile_index)

    def place_tile(self, tile_obj, board_location):
        ''' Takes format of rack_tile_index, board_location '''
        self.board[board_location].tile = tile_obj

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
                    scrabble_board.ScrabbleTile(
                        letter=letter,
                        point_value=config.LETTER_POINT_VALUES_DICT[letter]
                    )
                )

        return tile_bag
