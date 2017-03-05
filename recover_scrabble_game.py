"""
Usage:
    $ python3 recover_scrabble_game.py [INPUT_FILENAME]

    See sample_input_files/ for examples of correctly formatted input files
"""
import sys
import scrabble

if __name__ == '__main__':
    if len(sys.argv) == 2:
        for move_list in scrabble.helpers.recover_game(sys.argv[1]):
            print('{}\n\n'.format(move_list))
    else:
        print('Usage: python3 recover_scrabble_game.py [INPUT_FILENAME]')
