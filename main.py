import pygame
import sys
import chess

# Definição de constantes

#linhas=8
#quadrado_selecionado=None
WIDTH, HEIGHT = 900, 900
BOARD_SIZE = 8
SQUARE_SIZE = WIDTH // BOARD_SIZE
BLACK = (85, 107, 47)
WHITE = (107, 142, 35)
SELECT_COLOR = (255,99,71)
HIGHLIGHT=(255,99,71)
#screen = pygame.display.set_mode((WIDTH, HEIGHT))

#board=chess.Board()
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

pygame.init()

class ChessGame:
    def __init__(self):
        self.quadrado_selecionado=None
        self.linhas=8
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        self.board=chess.Board()



    def get_row_col_from_mouse(pos):
        x, y = pos
        row, col = y // SQUARE_SIZE, x // SQUARE_SIZE
        return row, col

    def draw_board(self):
     
        for row in range(BOARD_SIZE):
            for col in range(BOARD_SIZE):
                color = WHITE if (row + col) % 2 == 0 else BLACK
                pygame.draw.rect(self.screen, color, (col * SQUARE_SIZE, row * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))
                piece=self.board.piece_at(chess.square(col,BOARD_SIZE-1-row))
                if piece is not None:
                    
                    image=PIECE_IMAGES[piece.symbol()]         
                    self.screen.blit(image, (col * SQUARE_SIZE, row * SQUARE_SIZE))
                if self.quadrado_selecionado is not None and chess.square(col, self.linhas - 1 - row) ==  self.quadrado_selecionado:
                    pygame.draw.rect(self.screen, SELECT_COLOR, (col * SQUARE_SIZE,
                                                                    row * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))    
                  
    def draw_highlight(self,moves):
        for move in moves:
            row,col=chess.square_rank(move.to_square), chess.square_file(move.to_square)
            pygame.draw.rect(self.screen, HIGHLIGHT,(col*SQUARE_SIZE,row*SQUARE_SIZE, SQUARE_SIZE,SQUARE_SIZE))
game=ChessGame()
while not game.board.is_game_over():
    '''
    for row in range(BOARD_SIZE):
        for col in range(BOARD_SIZE):
            color = WHITE if (row + col) % 2 == 0 else BLACK
            pygame.draw.rect(screen, color, (col * SQUARE_SIZE, row * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))
            #square = chess.square(col, linhas - 1 - row)
            #piece = square
            piece=board.piece_at(chess.square(col,BOARD_SIZE-1-row))
            if piece is not None:
                
                image=PIECE_IMAGES[piece.symbol()]         
                screen.blit(image, (col * SQUARE_SIZE, row * SQUARE_SIZE))
            if quadrado_selecionado is not None and chess.square(col, linhas - 1 - row) ==  quadrado_selecionado:
                pygame.draw.rect(screen, SELECT_COLOR, (col * SQUARE_SIZE,
                                                                   row * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))    
    '''                
    for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                # Obtendo a posição do clique do mouse
                
                pos = pygame.mouse.get_pos()
                col = pos[0] // SQUARE_SIZE
                row = pos[1] // SQUARE_SIZE
                square = chess.square(col, game.linhas - 1 - row)
                #quadrado_selecionado=square
                print('linha '+str(row)+' coluna '+str(col))
                if game.quadrado_selecionado is None:
                     if game.board.piece_at(square) is not None:
                        game.quadrado_selecionado=square
                else:
                     move=chess.Move(game.quadrado_selecionado,square)
                     if move in game.board.legal_moves:
                          game.board.push(move)
                          print("move:"+move)
                     game.quadrado_selecionado=None
                '''
                moves = list(board.legal_moves)
                for move in moves:
                        if move.from_square == square:
                            board.push(move)
                            break

                '''
    game.draw_board()
    if game.quadrado_selecionado is not None:
        moves=game.board.generate_legal_moves(from_mask=1<<game.quadrado_selecionado)    
        game.draw_highlight(moves)                    
    # Update the display
    pygame.display.update()

# Quit the game when it's over
pygame.quit()


