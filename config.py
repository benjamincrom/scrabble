BOARD_NUM_COLUMNS = 15
BOARD_NUM_ROWS = 15
PLAYER_RACK_SIZE = 7
BINGO_SCORE = 50

START_SQUARE_CHARACTER = '★'
BLANK_SQUARE_CHARACTER = '_'

WORD_SCORE_MULT_LOCATION_DICT = {
    ('b', 2): 2,
    ('b', 14): 2,
    ('c', 3): 2,
    ('c', 13): 2,
    ('d', 4): 2,
    ('d', 12): 2,
    ('e', 5): 2,
    ('e', 11): 2,
    ('h', 8): 2,
    ('k', 5): 2,
    ('k', 11): 2,
    ('l', 4): 2,
    ('l', 12): 2,
    ('m', 4): 2,
    ('m', 13): 2,
    ('n', 2): 2,
    ('n', 14): 2,
    ('a', 1): 3,
    ('a', 8): 3,
    ('a', 15): 3,
    ('h', 1): 3,
    ('h', 15): 3,
    ('o', 1): 3,
    ('o', 8): 3,
    ('o', 15): 3
}

LETTER_SCORE_MULT_LOCATION_DICT = {
    ('a', 4): 2,
    ('a', 12): 2,
    ('c', 7): 2,
    ('c', 9): 2,
    ('d', 1): 2,
    ('d', 8): 2,
    ('d', 15): 2,
    ('g', 3): 2,
    ('g', 7): 2,
    ('g', 9): 2,
    ('g', 13): 2,
    ('h', 4): 2,
    ('h', 12): 2,
    ('i', 3): 2,
    ('i', 7): 2,
    ('i', 9): 2,
    ('i', 13): 2,
    ('l', 1): 2,
    ('l', 8): 2,
    ('l', 15): 2,
    ('m', 7): 2,
    ('m', 9): 2,
    ('o', 4): 2,
    ('m', 12): 2,
    ('b', 6): 3,
    ('b', 10): 3,
    ('f', 2): 3,
    ('f', 6): 3,
    ('f', 10): 3,
    ('f', 14): 3,
    ('j', 2): 3,
    ('j', 6): 3,
    ('j', 10): 3,
    ('j', 14): 3,
    ('n', 6): 3,
    ('n', 10): 3  
}

# Captial letters are used to distinguish letter glyphs from locations
LETTER_POINT_VALUES_DICT = {
    '*': 0,
    'A': 1,
    'B': 3,
    'C': 3,
    'D': 2,
    'E': 1,
    'F': 4,
    'G': 2,
    'H': 4,
    'I': 1,
    'J': 8,
    'K': 5,
    'L': 1,
    'M': 3,
    'N': 1,
    'O': 1,
    'P': 3,
    'Q': 10,
    'R': 1,
    'S': 1,
    'T': 1,
    'U': 1,
    'V': 4,
    'W': 4,
    'X': 8,
    'Y': 4,
    'Z': 10
}

LETTER_DISTRIBUTION_DICT = {
    '*': 2,
    'A': 9,
    'B': 2,
    'C': 2,
    'D': 4,
    'E': 12,
    'F': 2,
    'G': 3,
    'H': 2,
    'I': 9,
    'J': 1,
    'K': 1,
    'L': 4,
    'M': 2,
    'N': 6,
    'O': 8,
    'P': 2,
    'Q': 1,
    'R': 6,
    'S': 4,
    'T': 6,
    'U': 4,
    'V': 2,
    'W': 2,
    'X': 1,
    'Y': 2,
    'Z': 1
}

LOWER_COLUMN_INT_BOUND = ord('a')
UPPER_COLUMN_INT_BOUND = LOWER_COLUMN_INT_BOUND + BOARD_NUM_COLUMNS - 1

LETTER_CODE_DICT = {
    chr(code_point): code_point
    for code_point in range(LOWER_COLUMN_INT_BOUND - 40,
                            UPPER_COLUMN_INT_BOUND + 40)
}

UPPER_COLUMN_LETTER_BOUND = max(LETTER_CODE_DICT)
LOWER_COLUMN_LETTER_BOUND = min(LETTER_CODE_DICT)
