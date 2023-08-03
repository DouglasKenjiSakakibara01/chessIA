#arquivo py para testar as funcoes da biblioteca chess e do pygame
import chess 
import pygame
board=chess.Board()
WIDTH, HEIGHT = 900, 900
BOARD_SIZE = 8
SQUARE_SIZE = WIDTH // BOARD_SIZE
BLACK = (85, 107, 47)
WHITE = (107, 142, 35)
SELECT_COLOR = (255,99,71)
HIGHLIGHT=(255,99,71)
PIECE_IMAGES = {
    'N': pygame.image.load('images/wn.png'),
    'K': pygame.image.load('images/wk.png'),
    'B': pygame.image.load('images/wb.png'),
    'P': pygame.image.load('images/wp.png'),
    'Q': pygame.image.load('images/wq.png'),
    'R': pygame.image.load('images/wr.png'),
    'p': pygame.image.load('images/bp.png'),
    'k': pygame.image.load('images/bk.png'),
    'b': pygame.image.load('images/bb.png'),
    'n': pygame.image.load('images/bn.png'),
    'q': pygame.image.load('images/bq.png'),
    'r': pygame.image.load('images/br.png'),
}
piece=board.piece_at(chess.square(0,0))

print(board.legal_moves)