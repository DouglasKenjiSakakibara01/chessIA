import pygame
import sys
import chess

# Definição de constantes

linhas=8
quadrado_selecionado=None
WIDTH, HEIGHT = 900, 900
BOARD_SIZE = 8
SQUARE_SIZE = WIDTH // BOARD_SIZE
BLACK = (85, 107, 47)
WHITE = (107, 142, 35)
SELECT_COLOR = (0, 250, 0)
screen = pygame.display.set_mode((WIDTH, HEIGHT))
# Representação do tabuleiro (8x8) - 0 representa espaço vazio
tabuleiro= [
    [12, 10, 9, 11, 8, 9, 10, 12],
    [7, 7, 7, 7, 7, 7, 7, 7],
    [0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0],
    [4, 4, 4, 4, 4, 4, 4, 4],
    [6, 1, 3, 5, 2, 3, 1, 6],
]
# Carregar imagens das peças (coloque as imagens dos arquivos PNG na mesma pasta do script)
# Você pode usar outras imagens se preferir
PIECE_IMAGES = {
    1: pygame.image.load('images/wn.png'),
    2: pygame.image.load('images/wk.png'),
    3: pygame.image.load('images/wb.png'),
    4: pygame.image.load('images/wp.png'),
    5: pygame.image.load('images/wq.png'),
    6: pygame.image.load('images/wr.png'),
    7: pygame.image.load('images/bp.png'),
    8: pygame.image.load('images/bk.png'),
    9: pygame.image.load('images/bb.png'),
    10: pygame.image.load('images/bn.png'),
    11: pygame.image.load('images/bq.png'),
    12: pygame.image.load('images/br.png'),
}

pygame.init()

def get_row_col_from_mouse(pos):
    x, y = pos
    row, col = y // SQUARE_SIZE, x // SQUARE_SIZE
    return row, col
board=chess.Board()

while not board.is_game_over():
    for row in range(BOARD_SIZE):
        for col in range(BOARD_SIZE):
            color = WHITE if (row + col) % 2 == 0 else BLACK
            pygame.draw.rect(screen, color, (col * SQUARE_SIZE, row * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))
            piece = tabuleiro[row][col]
            if piece != 0:
                image = PIECE_IMAGES[piece]
                screen.blit(image, (col * SQUARE_SIZE, row * SQUARE_SIZE))
            if quadrado_selecionado and chess.square(col, linhas - 1 - row) ==  quadrado_selecionado:
                pygame.draw.rect(screen, SELECT_COLOR, (col * SQUARE_SIZE,
                                                                   row * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))    
                print('entrou if')
    for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                # Obtendo a posição do clique do mouse
                
                pos = pygame.mouse.get_pos()
                col = pos[0] // SQUARE_SIZE
                row = pos[1] // SQUARE_SIZE
                square = chess.square(col, linhas - 1 - row)
                print('linha '+str(row)+' coluna '+str(col))
                
                moves = list(board.legal_moves)
                for move in moves:
                        if move.from_square == square:
                            board.push(move)
                            break

    # Update the display
    pygame.display.update()

# Quit the game when it's over
pygame.quit()

'''
# Inicialização do Pygame
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Xadrez')
clock = pygame.time.Clock()
'''
