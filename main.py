import pygame
import sys
import chess
from chessIA import ChessIA
# Definição das constantes
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

pygame.init()

class ChessGame:
    def __init__(self):
        self.quadrado_selecionado=None
        self.situacao_jogo=True
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        self.board=chess.Board()


    #Pega a posicao da linha e da coluna do quadrado do tabuleiro que foi clicado
    '''
    def get_row_col_from_mouse(pos):
        x, y = pos
        row, col = y // SQUARE_SIZE, x // SQUARE_SIZE
        return row, col
    '''
    def draw_board(self):
     
        for row in range(BOARD_SIZE):
            for col in range(BOARD_SIZE):
                color = WHITE if (row + col) % 2 == 0 else BLACK
                pygame.draw.rect(self.screen, color, (col * SQUARE_SIZE, row * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))
                piece=self.board.piece_at(chess.square(col,BOARD_SIZE-1-row))
                if piece is not None:
                    
                    image=PIECE_IMAGES[piece.symbol()]         
                    self.screen.blit(image, (col * SQUARE_SIZE, row * SQUARE_SIZE))

                if self.quadrado_selecionado is not None and chess.square(col, 7 - row) ==  self.quadrado_selecionado:
                    pygame.draw.rect(self.screen, SELECT_COLOR, (col * SQUARE_SIZE,
                                                                    row * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))    
    
    #destaca os quadrados das possiveis jogadas da peça atual
    def draw_highlight(self,moves):
        for move in moves:
            row,col=chess.square_rank(move.to_square), chess.square_file(move.to_square)
            pygame.draw.rect(self.screen, HIGHLIGHT,(col * SQUARE_SIZE, row * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))

    def get_promotion(self):
        selecionado=input("Digite a peça que deseja promover(r,n,q,b):")
        if self.board.turn:
            image=PIECE_IMAGES[selecionado.upper().symbol()] 
        else:
            image=PIECE_IMAGES[selecionado.symbol()] 
        return image
    
         
opcao=input("Jogador x IA (Digite 1) | IA x IA (Digite 2):")
game=ChessGame()
IA=ChessIA()

if int(opcao) == 1:
 while game.situacao_jogo : 
    if game.board.turn:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                # Pega a posicao da linha e da coluna do quadrado do tabuleiro que foi clicado
                pos = pygame.mouse.get_pos()
                col = pos[0] // SQUARE_SIZE
                row = pos[1] // SQUARE_SIZE
                square = chess.square(col, 7- row)
                print('linha '+str(row)+' coluna '+str(col))
                if game.quadrado_selecionado is None:
                     if game.board.piece_at(square) is not None:
                        game.quadrado_selecionado=square
                else:
                     move=chess.Move(game.quadrado_selecionado,square)
                     if move in game.board.legal_moves:
                        if game.board.piece_type_at(
                                    game.quadrado_selecionado) == chess.PAWN and chess.square_rank(square) == 7:
                            promotion=game.get_promotion()
                            if promotion is not None:
                                game.screen.blit(promotion, (col * SQUARE_SIZE, row * SQUARE_SIZE))
                        game.board.push(move)
                        if game.board.is_game_over():
                             game.situacao_jogo=False
                        print("move")
                     game.quadrado_selecionado=None
               
    else:
        move=IA.select_move(3,game.board)
        if game.board.piece_type_at(move.to_square) == chess.PAWN and chess.square_rank(move.to_square) == 7:
                            promotion=game.get_promotion()
                            if promotion is not None:
                                game.screen.blit(promotion, ( chess.square_file(move.to_square) * SQUARE_SIZE, 7 * SQUARE_SIZE))
                            game.board.push(move)
                            
        print('vez da IA')
        game.board.push(move)
        if game.board.is_game_over():
            game.situacao_jogo=False

    game.draw_board()

    #para destacar os movimentos disponiveis para cada peça selionada
    '''
    if game.quadrado_selecionado is not None:
        moves=game.board.generate_legal_moves(from_mask=1<<game.quadrado_selecionado)    
        #game.draw_highlight(moves)                    
    '''
    pygame.display.update()
      
      
elif int(opcao) == 2:
  while game.situacao_jogo: 
    if game.board.turn:
        move=IA.select_move(3,game.board)
        if game.board.piece_type_at(move.to_square) == chess.PAWN and chess.square_rank(move.to_square) == 7:
                            promotion=game.get_promotion()
                            print("Promocao")
                            if promotion is not None:
                                game.screen.blit(promotion, ( chess.square_file(move.to_square) * SQUARE_SIZE, 7 * SQUARE_SIZE))
                            game.board.push(move)
                            
        
        game.board.push(move)
        if game.board.is_game_over():
            game.situacao_jogo=False
        

    
    else:
        move=IA.select_move(3,game.board)
        #precisa adicionar a forma que define qual peca o peao será promovido
        if game.board.piece_type_at(move.to_square) == chess.PAWN and chess.square_rank(move.to_square) == 7:
                            promotion=game.get_promotion()
                            print("IA Promocao")
                            if promotion is not None:
                                game.screen.blit(promotion, ( chess.square_file(move.to_square) * SQUARE_SIZE, 7 * SQUARE_SIZE))
                            game.board.push(move)
                            
        
        game.board.push(move)
        if game.board.is_game_over():
          game.situacao_jogo=False

    game.draw_board()

    #para destacar os movimentos disponiveis para cada peça selionada
    '''
    if game.quadrado_selecionado is not None:
        moves=game.board.generate_legal_moves(from_mask=1<<game.quadrado_selecionado)    
        #game.draw_highlight(moves)                    
    '''
    pygame.display.update()
    
          
      
else:
      print("Opcao incorreta")      

print('Jogo encerrado')
pygame.quit()


