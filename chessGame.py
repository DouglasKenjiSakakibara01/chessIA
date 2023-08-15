import chess
import pygame
import threading

from chessEngine import chess_engine
from chessIA import chess_ai
from consts import *
import util

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
        util.logging.log_debug(col)
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
    def __init__(self, board=None):
        if not pygame.get_init(): pygame.init()

        self.game_situation = False
        self.selected_square = None
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        self.board = chess.Board(board) if board is not None else chess.Board()
        self.last_move = None
        self.legal_moves = []
        self.next_move = None
        self.curr_player = None
        self.computer_move_thread = None
        self.computer_running = False

    def draw(self):
        for row in range(BOARD_SIZE):
            for col in range(BOARD_SIZE):
                square = self.coord_to_square(col, row)
                piece = self.board.piece_at(square)
                if square == self.selected_square:
                    self.draw_square(col, row, COLORS['SELECTED_SQUARE'])
                elif self.last_move is not None and square == self.last_move.to_square:
                    self.draw_square(col, row, COLORS['LAST_MOVE_TO_SQUARE'])
                elif self.last_move is not None and square == self.last_move.from_square:
                    self.draw_square(col, row, COLORS['LAST_MOVE_FROM_SQUARE'])
                else:
                    self.draw_square(col, row, COLORS['WHITE_TILE'] if (row + col) % 2 == 0 else COLORS['BLACK_TILE'])
                
                if square in self.legal_moves and self.curr_player == PLAYER:
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
        chess_square = chess.Square(square)
        return chess.square_file(chess_square), BOARD_SIZE - 1 - chess.square_rank(chess_square)

    def coord_to_square(self, col, row):
        return chess.square(col, BOARD_SIZE - 1 - row)

    def draw_legal_move(self, square):
        col, row = self.square_to_coord(square)
        legal_move_x = col * SQUARE_SIZE
        legal_move_y = row * SQUARE_SIZE
        legal_move_offset = SQUARE_SIZE // 2
        capture = self.board.piece_at(square)
        pygame.draw.circle(self.screen, COLORS['POSSIBLE_MOVE'],
                        (legal_move_x + legal_move_offset, legal_move_y + legal_move_offset),
                        POSSIBLE_CAPTURE_SIZE if capture else POSSIBLE_MOVE_SIZE,
                        POSSIBLE_CAPTURE_WIDTH if capture else 0)

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

    def handle_event(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.game_situation = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                col, row = pos[0] // SQUARE_SIZE, pos[1] // SQUARE_SIZE
                square = self.coord_to_square(col, row)
                util.logging.log_debug(f"Row: {row} | Col: {col}")
                if self.selected_square is not None and self.curr_player == PLAYER:
                    self.next_move = self.player_move(col, row, square)
                if self.next_move is None and self.board.piece_at(square) is not None:
                    self.selected_square = square
                    self.legal_moves = [move.to_square for move in self.board.generate_legal_moves(chess.BB_SQUARES[self.selected_square])]

    def play(self, players):
        self.game_situation = True
        while self.game_situation and not self.board.is_game_over(claim_draw=True):
            self.draw()
            pygame.display.update()

            self.handle_event()

            self.curr_player = players[0 if self.board.turn else 1]
            
            if self.curr_player != PLAYER and not self.computer_running:
                self.computer_running = True
                self.computer_move_thread = threading.Thread(target=lambda: setattr(self, 'next_move', self.ai_move() if self.curr_player == AI else self.engine_move()))
                self.computer_move_thread.start()

            if self.next_move is not None:
                util.logging.log_move(self.board.turn, self.board.fullmove_number, self.board.san(self.next_move))
                self.board.push(self.next_move)
                self.last_move = self.next_move
                self.selected_square = None
                self.legal_moves = []
                self.computer_running = False
                self.next_move = None

        return self.board.outcome(claim_draw=True).result() if self.game_situation else None

    def player_move(self, col, row, square):
        move = chess.Move(self.selected_square, square)
        if self.board.piece_type_at(self.selected_square) == chess.PAWN \
            and row in [0, BOARD_SIZE - 1] \
            and chess.Move.from_uci(str(move) + "q") in self.board.legal_moves:
            util.logging.log_debug('Promotion')
            promotion = self.get_promotion(col, self.board.turn)
            if promotion is not None:
                move = chess.Move.from_uci(str(move) + promotion)
        self.legal_moves = []
        self.selected_square = None
        if move in self.board.legal_moves:
            util.logging.log_debug("Valid move")
            return move

    def ai_move(self):
        util.logging.log_debug("AI turn")
        return chess_ai.select_move(self.board)

    def engine_move(self):
        util.logging.log_debug("Engine turn")
        return chess_engine.select_move(self.board)
