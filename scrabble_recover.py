import json

import scrabble_board
import scrabble_game

def load_file(input_filename):
    with open(input_filename, 'r') as filehandle:
        input_str = filehandle.read()

    input_dict = json.loads(input_str)
    board_character_array = input_dict['board']
    player_scores_list_list = input_dict['scores']

    return board_character_array, player_scores_list_list

def read_input_file(input_filename):
    board_character_array, player_scores_list_list = load_file(input_filename)

    num_players = len(player_scores_list_list)
    game = scrabble_game.ScrabbleGame(num_players)
    game.player_rack_list = [[] for _ in range(num_players)]
    game.tile_bag = []

    for row_number, row in enumerate(board_character_array):
        for column_number, letter in enumerate(row):
            if letter:
                column_letter = chr(ord('a') + column_number)
                this_location = (column_letter, row_number + 1)
                game.board[this_location] = scrabble_board.ScrabbleTile(letter)

    return game
