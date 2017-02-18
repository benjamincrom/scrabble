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

def refill_player_rack(player_rack, tile_bag):
    while len(player_rack) < 7:
        if tile_bag:
            tile = draw_random_tile(tile_bag)
            player_rack.append(tile)
        else:
            break

def perform_bag_exchange(letter_list, player_rack, tile_bag):
    exchange_tile_list = []
    for letter in letter_list:
        for tile in player_rack:
            if tile.letter == letter:
                exchange_tile_list.append(tile)
                player_rack.remove(tile)

    for _ in range(len(letter_list)):
        new_tile = draw_random_tile(tile_bag)
        player_rack.append(new_tile)

    tile_bag.extend(exchange_tile_list)

def get_current_player_data(move_number, player_rack_list):
    num_players = len(player_rack_list)
    player_to_move_id = move_number % num_players
    player_rack = player_rack_list[player_to_move_id]

    return player_to_move_id, player_rack

def get_word_letter_location_set(word, start_location, is_vertical_move):
    letter_location_set = set([])
    next_location_func = get_next_location_function(
        use_positive_seek=True,
        use_vertical_words=is_vertical_move
    )

    current_location = start_location
    word_iterator = iter(word)
    for character in word_iterator:
        if character == '(':
            character = next(word_iterator, None)
            while character != ')':
                current_location = next_location_func(current_location)
                character = next(word_iterator, None)

            character = next(word_iterator, None)

        if character:
            letter_location_set.add((character, current_location))
            current_location = next_location_func(current_location)

    return letter_location_set

def conclude_game(player_rack_list, player_score_list_list, empty_rack_id=None):
    all_rack_points = 0

    for i, player_rack in enumerate(player_rack_list):
        rack_point_total = sum(tile.point_value for tile in player_rack)
        this_player_score_list = player_score_list_list[i]
        this_player_score_list.append(-1 * rack_point_total)
        all_rack_points += rack_point_total

    if empty_rack_id:  # Empty rack player gets all other racks' points
        empty_player_score_list = player_score_list_list[empty_rack_id]
        empty_player_score_list.append(all_rack_points)

    player_score_total_list = [
        sum(player_score_list)
        for player_score_list in player_score_list_list
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

def score_move(letter_location_set, board):
    move_location_set = set(
        (location for _, location in letter_location_set)
    )

    word_set = get_word_set(board, move_location_set)
    total_score = get_word_set_total_score(board,
                                           word_set,
                                           len(move_location_set))

    cancel_bonus_squares(move_location_set, board)

    return total_score

def cancel_bonus_squares(location_set, board):
    for location in location_set:
        square = board.board_square_dict[location]
        square.letter_multiplier = 1
        square.word_multiplier = 1

def initialize_player_rack_list(num_players, tile_bag):
    player_rack_list = []

    for _ in range(num_players):
        this_rack = []
        for _ in range(7):
            this_tile = draw_random_tile(tile_bag)
            this_rack.append(this_tile)

        player_rack_list.append(this_rack)

    return player_rack_list

def cheat_create_rack_tile(character, player_rack):
    tile = scrabble_board.ScrabbleTile(letter=character)
    player_rack.append(tile)

def cheat_create_rack_word(word, player_rack):
    for character in word:
        cheat_create_rack_tile(character, player_rack)

def draw_random_tile(tile_bag):
    random_index = random.randrange(0, len(tile_bag))
    selected_tile = tile_bag.pop(random_index)

    return selected_tile

def move_is_legal(board, move_number, letter_location_set, player_rack):
    player_rack_letter_list = [tile.letter for tile in player_rack]
    letter_list = [letter for letter, _ in letter_location_set]
    location_set = set(location for _, location in letter_location_set)

    return (
        move_is_seven_tiles_or_less(location_set) and
        move_is_not_out_of_bounds(location_set) and
        move_is_sublist(letter_list, player_rack_letter_list) and
        move_does_not_stack_tiles(letter_list, location_set) and
        move_does_not_misalign_tiles(board, location_set) and
        move_does_not_cover_tiles(board, location_set) and
        move_touches_tile(move_number, board, location_set)
    )

def move_touches_tile(move_number, board, location_set):
    if move_number == 0:
        if config.START_SQUARE in location_set:
            return True
    else:
        for this_location in location_set:
            if location_touches_tile(board, this_location):
                return True

    print('Move does not touch any existing tiles.')
    return False

def move_is_sublist(letter_list_1, letter_list_2):
    letter_counter_1 = collections.Counter(letter_list_1)
    letter_counter_2 = collections.Counter(letter_list_2)
    for letter, cardinality in letter_counter_1.items():
        if cardinality > letter_counter_2[letter]:
            print('Not enough {} tiles in rack.'.format(letter))
            return False

    return True

def move_does_not_cover_tiles(board, location_set):
    for location in location_set:
        if board[location]:
            print(
                'Move covers existing tiles at location {}'.format(location)
            )
            return False

    return True

def move_does_not_misalign_tiles(board, location_set):
    # All tiles places are in one row or one column
    column_list = [location[0] for location in location_set]
    row_list = [location[1] for location in location_set]

    if len(set(column_list)) == 1:
        is_vertical_move = True
    elif len(set(row_list)) == 1:
        is_vertical_move = False
    else:
        print('Move does not place all tiles in one row or column.')
        return False

     # All tiles must be connected
    if is_vertical_move:
        this_column = list(location_set)[0][0]
        for this_row in range(min(row_list), max(row_list) + 1):
            this_tile = board[(this_column, this_row)]
            if not (this_tile or (this_column, this_row) in location_set):
                print(
                    'Not all tiles in vertical move are connected: '
                    'location {} is empty'.format((this_column, this_row))
                )
                return False
    else:
        this_row = list(location_set)[0][1]
        for this_column_num in range(ord(min(column_list)),
                                     ord(max(column_list)) + 1):
            this_column = chr(this_column_num)
            this_tile = board[(this_column, this_row)]
            if not (this_tile or (this_column, this_row) in location_set):
                print(
                    'Not all tiles in horizontal move are connected: '
                    'location {} is empty'.format((this_column, this_row))
                )
                return False

    return True

def move_does_not_stack_tiles(letter_list, location_set):
    if len(letter_list) == len(location_set):
        return True
    else:
        print('Move stacks tiles.')
        return False

def move_is_seven_tiles_or_less(location_set):
    if len(location_set) > 7:
        print('Move places greater than seven tiles.')
        return False
    else:
        return True

def move_is_not_out_of_bounds(location_set):
    for location in location_set:
        if location_is_out_of_bounds(location):
            print('Move location {} is out of bounds'.format(location))
            return False

    return True

def move_successfully_challenged():
    response = input('Challenge successful (Y/N)')
    if response.upper() == 'Y':
        return True
    elif response.upper() == 'N':
        return False
    else:
        print('You must enter Y or N')
        return move_successfully_challenged()

def location_is_out_of_bounds(location):
    column, row = location
    return (ord(column) < ord('a') or
            ord(column) > ord('o') or
            row < 1 or
            row > 15)

def location_touches_tile(board, location):
    adjacent_location_set = get_adjacent_location_set(location)
    for adjacent_location in adjacent_location_set:
        if board[adjacent_location]:
            return True

    return False

def get_rack_tile_index(player_rack, move_letter):
    for i, rack_tile in enumerate(player_rack):
        if rack_tile.letter == move_letter:
            return i

    return None

def get_new_tile_bag():
    return [
        scrabble_board.ScrabbleTile(letter=letter)
        for letter, magnitude in config.LETTER_DISTRIBUTION_DICT.items()
        for _ in range(magnitude)
    ]

def get_next_location_function(use_positive_seek, use_vertical_words):
    if use_vertical_words and use_positive_seek:
        return lambda x: (x[0], x[1] + 1)
    elif use_vertical_words and not use_positive_seek:
        return lambda x: (x[0], x[1] - 1)
    elif not use_vertical_words and use_positive_seek:
        return lambda x: (increment_letter(x[0]), x[1])
    elif not use_vertical_words and not use_positive_seek:
        return lambda x: (decrement_letter(x[0]), x[1])

def get_adjacent_location_set(location):
    column, row = location

    adjacent_location_set = set([(increment_letter(column), row),
                                 (decrement_letter(column), row),
                                 (column, row + 1),
                                 (column, row - 1)])
    # Board boundary check
    remove_location_set = set(location for location in adjacent_location_set
                              if location_is_out_of_bounds(location))

    return adjacent_location_set - remove_location_set

def get_word_location_set(board, location, use_vertical_words):
    word_location_set = set([])

    for use_positive_seek in [True, False]:  # Search tiles in 2 directions:
        current_location = location          # either up/down or left/right
        current_tile = board[current_location]

        next_location_func = get_next_location_function(
            use_positive_seek,
            use_vertical_words
        )

        while current_tile:
            word_location_set.add(current_location)
            current_location = next_location_func(current_location)

            if location_is_out_of_bounds(current_location):
                current_tile = None
            else:
                current_tile = board[current_location]

    if len(word_location_set) > 1:           # Must be at least 2 letters to
        return frozenset(word_location_set)  # count as a word
    else:
        return frozenset([])

def get_word_set(board, move_location_set):
    word_set = set([])

    for use_vertical_words in [True, False]:  # Search for vertical words
        for location in move_location_set:    # created, then horizontal
            word_set.add(
                get_word_location_set(board,
                                      location,
                                      use_vertical_words=use_vertical_words)
            )

    return word_set

def get_word_set_total_score(board, word_set, num_move_locations):
    total_score = 0
    word_score = 0

    for word_location_set in word_set:
        word_score = 0
        word_multiplier = 1

        for location in word_location_set:
            square = board.board_square_dict[location]
            word_multiplier *= square.word_multiplier
            word_score += square.tile.point_value * square.letter_multiplier

        word_score *= word_multiplier
        total_score += word_score

    if num_move_locations == 7:
        total_score += 50  # Bingo

    return total_score


class ScrabbleGame(object):
    def __init__(self, num_players):
        self.tile_bag = get_new_tile_bag()
        self.player_rack_list = initialize_player_rack_list(num_players,
                                                            self.tile_bag)

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
        player_to_move_id, _ = get_current_player_data(self.move_number,
                                                       self.player_rack_list)

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

    def place_word(self, word, start_location, is_vertical_move):
        letter_location_set = get_word_letter_location_set(word,
                                                           start_location,
                                                           is_vertical_move)

        return self.next_player_move(letter_location_set)

    def next_player_move(self, letter_location_set):
        (player_to_move_id,
         player_rack) = get_current_player_data(self.move_number,
                                                self.player_rack_list)

        is_legal_move = move_is_legal(self.board,
                                      self.move_number,
                                      letter_location_set,
                                      player_rack)

        if is_legal_move:
            if move_successfully_challenged():
                letter_location_set = set([])

            for move_letter, board_location in letter_location_set:
                tile_index = get_rack_tile_index(player_rack, move_letter)
                tile_obj = player_rack.pop(tile_index)
                self.board[board_location] = tile_obj

            refill_player_rack(player_rack, self.tile_bag)

            move_score = score_move(letter_location_set, self.board)
            score_list = self.player_score_list_list[player_to_move_id]
            score_list.append(move_score)

            if len(player_rack) == 0 and len(self.tile_bag) == 0:
                conclude_game(
                    self.player_rack_list,
                    self.player_score_list_list,
                    player_to_move_id
                )

            self.move_number += 1
            return True
        else:
            return False

    def exchange(self, letter_list):
        if len(self.tile_bag) < 7 or len(letter_list) > 7:
            return False
        else:
            _, player_rack = get_current_player_data(
                self.move_number,
                self.player_rack_list
            )

            player_letter_list = [tile.letter for tile in player_rack]

            if move_is_sublist(letter_list, player_letter_list):
                perform_bag_exchange(letter_list, player_rack, self.tile_bag)

                self.move_number += 1
                return True
            else:
                return False

