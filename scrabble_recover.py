import sys

import helpers
import scrabble_game

def main():
    helpers.input = lambda x: 'N'

    if len(sys.argv) == 2:
        reference_game = helpers.read_input_file(sys.argv[1])
        new_game = scrabble_game.ScrabbleGame(
            len(reference_game.player_rack_list)
        )

        move_set_generator = helpers.get_move_set_generator(new_game,
                                                            reference_game,
                                                            [])

        for move_set in move_set_generator:
            print(helpers.get_move_set_notation(move_set, reference_game))
            print()
    else:
        print('Usage: ./scrabble_recover [INPUT_FILENAME]')

if __name__ == '__main__':
    main()
