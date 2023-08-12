import chess
import pygame
from chessIA import ChessIA
from stockfish import Stockfish
import colors

# Definição das constantes
SCALE = 9/9
WIDTH, HEIGHT = int(SCALE * 900), int(SCALE * 900)
BOARD_SIZE = 8
SQUARE_SIZE = WIDTH // BOARD_SIZE
POSSIBLE_MOVE_SIZE = SQUARE_SIZE / 5

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

PIECE_IMAGES = {k: pygame.transform.scale_by(v, SCALE) for k, v in  PIECE_IMAGES.items()}

class ChessGame:
    def __init__(self, board):
        self.selected_square = None
        self.game_situation = True
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        self.board = chess.Board(board) if board is not None else chess.Board()
        self.IA = ChessIA()
        self.winner=None
        


    def draw_board(self):
        for row in range(BOARD_SIZE):
            for col in range(BOARD_SIZE):
                color = colors.WHITE_TILE if (row + col) % 2 == 0 else colors.BLACK_TILE
                pygame.draw.rect(self.screen, color, (col * SQUARE_SIZE, row * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))
                piece = self.board.piece_at(chess.square(col, BOARD_SIZE - row - 1))

                if self.selected_square is not None and chess.square(col, 7 - row) == self.selected_square:
                    pygame.draw.rect(self.screen, colors.SELECTED_SQUARE,
                                     (col * SQUARE_SIZE, row * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))

                if piece is not None:
                    image = PIECE_IMAGES[piece.symbol()]
                    piece_x = col * SQUARE_SIZE
                    piece_y = row * SQUARE_SIZE
                    piece_x_offset = (SQUARE_SIZE - image.get_width()) // 2
                    piece_y_offset = (SQUARE_SIZE - image.get_height()) // 2
                    self.screen.blit(image, (piece_x + piece_x_offset, piece_y + piece_y_offset))

                if self.selected_square is not None:
                    moves = self.board.generate_legal_moves(chess.BB_SQUARES[self.selected_square])    
                    self.draw_possible(moves)


    def draw_possible(self, moves):
        for move in moves:
            row, col = 7 - chess.square_rank(move.to_square), chess.square_file(move.to_square)
            possible_move_x = col * SQUARE_SIZE
            possible_move_y = row * SQUARE_SIZE
            possible_move_offset = SQUARE_SIZE // 2
            pygame.draw.circle(self.screen, colors.POSSIBLE_MOVE,
                               (possible_move_x + possible_move_offset,  possible_move_y + possible_move_offset),
                               POSSIBLE_MOVE_SIZE)


    def get_promotion(self,color):
        selected=input("Digite a peça que deseja promover(r,n,q,b):")
        if selected == 'r':
            promotion= chess.Piece(chess.ROOK, color)
        elif selected == 'n':
            promotion= chess.Piece(chess.KNIGHT, color)
        elif selected == 'q':
            promotion= chess.Piece(chess.QUEEN, color)
        elif selected == 'b':
            promotion= chess.Piece(chess.BISHOP, color)
        
        return promotion
    

    def player_move(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                row, col = pos[1] // SQUARE_SIZE, pos[0] // SQUARE_SIZE
                square = chess.square(col, 7 - row)
                print('linha '+ str(row) + ' coluna ' + str(col))
                if self.selected_square is None:
                    if self.board.piece_at(square) is not None:
                        self.selected_square = square
                else:
                    move = chess.Move(self.selected_square, square)
                    if move in self.board.legal_moves:
                        print('Entrou no for do move')
                        if self.board.piece_type_at(self.selected_square) == chess.PAWN and (chess.square_rank(square) == 7 or chess.square_rank(square) == 0 ):
                            print('Promocao')
                            if self.board.turn():
                                promotion = self.get_promotion(chess.WHITE)
                            else:
                                promotion = self.get_promotion(chess.BLACK)    
                            
                            if promotion is not None:
                                self.board.push(move)
                                self.tabuleiro.set_piece_at(move.to_square, promotion)
                                promotion=None
                                self.selected_square=None
                                return move
                        elif self.board.is_castling(move):
                            self.selected_square=None
                            return move
                        elif self.board.is_en_passant(move):
                            self.selected_square=None
                            return move
                            
                        self.selected_square=None
                        return move
                    self.selected_square = None
                '''
                if self.board.piece_at(square) is not None:
                    self.selected_square = square
                elif self.selected_square is not None:
                    move = chess.Move(self.selected_square, square)
                    if move in self.board.legal_moves:
                        if self.board.piece_type_at(
                                    self.selected_square) == chess.PAWN and chess.square_rank(square) == 7:
                            promotion = self.get_promotion()
                            if promotion is not None:
                                self.screen.blit(promotion, (col * SQUARE_SIZE, row * SQUARE_SIZE))
                        self.selected_square = None
                        return move
                    
                    else:
                        self.selected_square = None
                '''                  
                    


    def cpu_move(self):
        print('vez da IA')
        move = self.IA.select_move(3, self.board)

        if self.board.piece_type_at(move.to_square) == chess.PAWN and chess.square_rank(move.to_square) == 7:
            promotion = self.get_promotion()
            if promotion is not None:
                self.screen.blit(promotion, ( chess.square_file(move.to_square) * SQUARE_SIZE, 7 * SQUARE_SIZE))
            
        return move
    
    def stockfish(self):

        print('vez stockfish')
        #caminho do arquivo executavel do stockfish
        stockfish = Stockfish("stockfish/stockfish/stockfish-ubuntu-x86-64-modern")
        stockfish.set_fen_position(self.board.fen())
        stockfish.set_depth(5)
        stockfish.set_skill_level(5) 
        move = chess.Move.from_uci(stockfish.get_best_move())#forma padrão de representar movimentos de xadrez em formato de texto.
        return move
        
        


    def play(self, players):
        while self.game_situation:
            self.draw_board()
            pygame.display.update()

            player = players[0 if self.board.turn else 1]
            move = self.player_move() if player else self.cpu_move()
            if not players[0] and not players[1]:
                move=self.cpu_move() if player else self.stockfish()

            else:
                move=self.player_move() if player else self.cpu_move()

            if move is not None:
                self.board.push(move)
                if self.board.is_game_over():
                    if self.board.turn:
                        self.winner="Preto"
                    else:
                        self.winner="White"    
                    self.game_situation = False
                    
    def test_file(self):
        file = open("teste.txt", "w")
        file.write(f" Vencedor:{self.winner}\n")
        #file.write(f"Jogadas do branco:{}\n")
        #file.write(f"Jogadas do preto:{}\n")
        file.close()
