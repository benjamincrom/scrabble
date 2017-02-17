import json

import scrabble_board
import scrabble_game

def read_input_file(input_filename):
    with open(input_filename, 'r') as filehandle:
        input_str = filehandle.read()

    input_dict = json.loads(input_str)
    board_character_list_list = input_dict['board']
    player_scores_list_list = input_dict['scores']

    return board_character_array, player_scores_list_list


board_character_array, player_scores_list_list = read_input_file(
    'sample_input.json'
)

num_players = len(player_scores_list_list)
game = scrabble_game.ScrabbleGame(num_players)

for row_number, row in enumerate(board_character_array):
    for column_number, letter in enumerate(row):
        if letter:
            column_letter = chr(ord('a') + column_number)
            game.board[column_letter, row_number] = scrabble_board.ScrabbleTile(
                letter
            )
