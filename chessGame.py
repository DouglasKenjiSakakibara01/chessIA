import chess
import pygame
import threading
import time
import queue
from stockfish import Stockfish

from chessIA import ChessIA

DEBUG = {
    'LOG': True,
    'RENDER_AI_MOVES': False
}

def log(str):
    if DEBUG['LOG']: print(str)

COLORS = {
    'BLACK_TILE': (70, 70, 70),
    'WHITE_TILE': (150, 150, 150),
    'LAST_MOVE_TO_SQUARE': (120, 120, 190),
    'LAST_MOVE_FROM_SQUARE': (100, 100, 170),
    'SELECTED_SQUARE': (200, 200, 0),
    'POSSIBLE_MOVE': (100, 100, 100),
    'PROMOTION_MENU': (255, 255, 255)
}

# Definição das constantes
SCALE = 7/9
WIDTH, HEIGHT = int(SCALE * 900), int(SCALE * 900)
BOARD_SIZE = 8
SQUARE_SIZE = WIDTH // BOARD_SIZE
POSSIBLE_MOVE_SIZE = SQUARE_SIZE / 5
POSSIBLE_CAPTURE_SIZE = SQUARE_SIZE / 2.1

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

PIECE_IMAGES = { k: pygame.transform.scale_by(v, SCALE) for k, v in  PIECE_IMAGES.items() }

class PromotionMenu:
    def __init__(self, screen, col, turn):
        log(col)
        self.screen = screen
        self.menu_rect = pygame.Rect(col * SQUARE_SIZE, 0 if turn else HEIGHT - (SQUARE_SIZE * 4), SQUARE_SIZE, (SQUARE_SIZE * 4) + 10)
        possible_pieces = ['Q', 'N', 'R', 'B'] if turn else ['q', 'n', 'r', 'b']
        self.piece_images = dict((key, PIECE_IMAGES[key]) for key in possible_pieces)
        self.selected_piece = None

    def draw(self):
        pygame.draw.rect(self.screen, COLORS['PROMOTION_MENU'], self.menu_rect)
        for idx, (_, image) in enumerate(self.piece_images.items()):
            x = self.menu_rect.centerx - image.get_width() // 2
            y = self.menu_rect.y + idx * SQUARE_SIZE
            self.screen.blit(image, (x, y))

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            log('event 2')
            for idx, (piece, image) in enumerate(self.piece_images.items()):
                x = self.menu_rect.centerx - image.get_width() // 2
                y = self.menu_rect.y + idx * (image.get_height() + 10) + 20
                piece_rect = pygame.Rect(x, y, image.get_width(), image.get_height())
                if piece_rect.collidepoint(event.pos):
                    self.selected_piece = piece
            return True

    def get_selected_piece(self):
        return self.selected_piece


class ChessGame:
    def __init__(self, board):
        self.selected_square = None
        self.game_situation = True
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        self.board = chess.Board(board) if board is not None else chess.Board()
        self.IA = ChessIA()
        self.winner = None
        self.last_move = None
        self.legal_moves = []
        self.cpu_move_queue = queue.Queue()
        self.play_functions = {
            'Player': self.player_move,
            'CPU': self.cpu_move,
            'Stockfish': self.stockfish_move,
        }

    def draw(self):
        for row in range(BOARD_SIZE):
            for col in range(BOARD_SIZE):
                square = self.coord_to_square(col, row)
                piece = self.board.piece_at(square)

                if self.last_move is not None and square == self.last_move.to_square:
                    self.draw_square(col, row, COLORS['LAST_MOVE_TO_SQUARE'])
                elif self.last_move is not None and square == self.last_move.from_square:
                    self.draw_square(col, row, COLORS['LAST_MOVE_FROM_SQUARE'])
                elif square == self.selected_square:
                    self.draw_square(col, row, COLORS['SELECTED_SQUARE'])
                else:
                    self.draw_square(col, row, COLORS['WHITE_TILE'] if (row + col) % 2 == 0 else COLORS['BLACK_TILE'])
                
                if square in self.legal_moves:
                    self.draw_legal_move(square)

                if piece is not None:
                    image = PIECE_IMAGES[piece.symbol()]
                    piece_x = col * SQUARE_SIZE
                    piece_y = row * SQUARE_SIZE
                    piece_x_offset = (SQUARE_SIZE - image.get_width()) // 2
                    piece_y_offset = (SQUARE_SIZE - image.get_height()) // 2
                    self.screen.blit(image, (piece_x + piece_x_offset, piece_y + piece_y_offset))

    def draw_square(self, col, row, color):
        pygame.draw.rect(self.screen, color,
                (col * SQUARE_SIZE, row * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))
        
    def square_to_coord(self, square):
        chessSquare = chess.Square(square)
        return chess.square_file(chessSquare), 7 - chess.square_rank(chessSquare)

    def coord_to_square(self, col, row):
        return chess.square(col, 7 - row)

    def draw_legal_move(self, square):
        col, row = self.square_to_coord(square)
        legal_move_x = col * SQUARE_SIZE
        legal_move_y = row * SQUARE_SIZE
        legal_move_offset = SQUARE_SIZE // 2
        capture = self.board.piece_at(square)
        pygame.draw.circle(self.screen, COLORS['POSSIBLE_MOVE'],
                        (legal_move_x + legal_move_offset, legal_move_y + legal_move_offset),
                        POSSIBLE_CAPTURE_SIZE if capture else POSSIBLE_MOVE_SIZE,
                        5 if capture else 0)

    def get_promotion(self, col, turn):
        promotion_menu = PromotionMenu(self.screen, col, turn)
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                if promotion_menu.handle_event(event):
                    selected_piece = promotion_menu.get_selected_piece()
                    if selected_piece is not None:
                        return selected_piece.lower()
                    return None

            self.draw()
            promotion_menu.draw()
            pygame.display.flip()

    def player_move(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                col, row = pos[0] // SQUARE_SIZE, pos[1] // SQUARE_SIZE
                square = self.coord_to_square(col, row)
                log('linha '+ str(row) + ' coluna ' + str(col))
                if self.selected_square is None:
                    if self.board.piece_at(square) is not None:
                        self.selected_square = square
                        self.legal_moves = [move.to_square for move in self.board.generate_legal_moves(chess.BB_SQUARES[self.selected_square])]
                else:
                    move = chess.Move(self.selected_square, square)
                    if self.board.piece_type_at(self.selected_square) == chess.PAWN \
                      and row in [0, 7] \
                      and chess.Move.from_uci(str(move) + "q") in self.board.legal_moves:
                        log('Promocao')
                        promotion = self.get_promotion(col, self.board.turn)
                        if promotion is not None:
                            move = chess.Move.from_uci(str(move) + promotion)
                    self.selected_square = None
                    self.legal_moves = []
                    if move in self.board.legal_moves:
                        log('Movimento válido')
                        return move

    def cpu_move(self):
        log('vez da IA')

        def perform_cpu_move():
            move = self.IA.select_move(3, self.board)
            self.cpu_move_queue.put(move)

        ai_thread = threading.Thread(target=perform_cpu_move)
        ai_thread.start()

        while ai_thread.is_alive():
            if DEBUG['RENDER_AI_MOVES']: self.draw() # Se descomentar, os movimentos sendo analisados pela IA serão renderizados
            pygame.display.update()
            time.sleep(0.1)  # Pequeno atraso para evitar alta utilização da CPU

        return self.cpu_move_queue.get()


    def stockfish_move(self):
        log('vez stockfish')
        #caminho do arquivo executavel do stockfish
        stockfish = Stockfish("./stockfish-ubuntu-x86-64-modern")
        stockfish.set_fen_position(self.board.fen())
        stockfish.set_depth(5)
        stockfish.set_skill_level(5) 
        move = chess.Move.from_uci(stockfish.get_best_move())#forma padrão de representar movimentos de xadrez em formato de texto.
        return move

    def play(self, players):
        while self.game_situation:
            self.draw()
            pygame.display.update()

            player = players[0 if self.board.turn else 1]
            move = self.play_functions[player]()

            if move is not None:
                self.board.push(move)
                self.last_move = move
                if self.board.is_game_over():
                    if self.board.turn:
                        self.winner="Preto"
                    else:
                        self.winner="White"
                    

    def test_file(self):
        file = open("teste.txt", "w")
        file.write(f" Vencedor:{self.winner}\n")
        #file.write(f"Jogadas do branco:{}\n")
        #file.write(f"Jogadas do preto:{}\n")
        file.close()
