START_SQUARE_CHARACTER = '★'
BLANK_SQUARE_CHARACTER = '_'
BOARD_NUM_COLUMNS = 9
BOARD_NUM_ROWS = 9

DOUBLE_WORD_SCORE_LOCATION_LIST = [
    ('b', 2),
    ('b', 14),
    ('c', 3),
    ('c', 13),
    ('d', 4),
    ('d', 12),
    ('e', 5),
    ('e', 11),
    ('k', 5),
    ('k', 11),
    ('l', 4),
    ('l', 12),
    ('m', 4),
    ('m', 14),
    ('n', 2),
    ('n', 14)
]

TRIPLE_WORD_SCORE_LOCATION_LIST = [
    ('a', 1),
    ('a', 8),
    ('a', 15),
    ('h', 1),
    ('h', 15),
    ('o', 1),
    ('o', 8),
    ('o', 15)
]

DOUBLE_LETTER_SCORE_LOCATION_LIST = [
    ('a', 4),
    ('a', 12),
    ('c', 7),
    ('c', 9),
    ('d', 1),
    ('d', 8),
    ('d', 15),
    ('g', 3),
    ('g', 7),
    ('g', 9),
    ('g', 13),
    ('h', 4),
    ('h', 12),
    ('i', 3),
    ('i', 7),
    ('i', 9),
    ('i', 13),
    ('l', 1),
    ('l', 8),
    ('l', 15),
    ('m', 7),
    ('m', 9),
    ('o', 4),
    ('m', 12)
]

TRIPLE_LETTER_SCORE_LOCATION_LIST = [
    ('b', 6),
    ('b', 10),
    ('f', 2),
    ('f', 6),
    ('f', 10),
    ('f', 14),
    ('j', 2),
    ('j', 6),
    ('j', 10),
    ('j', 14),
    ('n', 6),
    ('n', 10)
]

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
