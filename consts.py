PLAYER = 1
AI = 2
ENGINE = 3

DEBUG = {
    'LOG': True,
    'RENDER_AI_MOVES': False
}

##### GAME RENDER #####################
COLORS = {
    'BLACK_TILE': (70, 70, 70),
    'WHITE_TILE': (150, 150, 150),
    'LAST_MOVE_TO_SQUARE': (120, 120, 190),
    'LAST_MOVE_FROM_SQUARE': (100, 100, 170),
    'SELECTED_SQUARE': (200, 200, 0),
    'POSSIBLE_MOVE': (100, 100, 100),
    'PROMOTION_MENU': (255, 255, 255)
}

SCALE = 7/9
WIDTH, HEIGHT = int(SCALE * 900), int(SCALE * 900)
BOARD_SIZE = 8
SQUARE_SIZE = WIDTH // BOARD_SIZE
POSSIBLE_MOVE_SIZE = SQUARE_SIZE / 5
POSSIBLE_CAPTURE_SIZE = SQUARE_SIZE / 2.1
POSSIBLE_CAPTURE_WIDTH = 5
#######################################

##### AI ##############################
AI_DEPTH = 8
#######################################

##### ENGINE ##########################
ENGINE_ELO = 1000
#######################################