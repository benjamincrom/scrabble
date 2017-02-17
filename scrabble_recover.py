import json

import scrabble_board
import scrabble_game

def read_input_file(input_filename):
    with open(input_filename, 'r') as filehandle:
        input_str = filehandle.read()

    input_dict = json.loads(input_str)
    import pdb; pdb.set_trace()  # breakpoint e1fa573c //
