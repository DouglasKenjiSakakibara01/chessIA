from chess import Move
from stockfish import Stockfish

from consts import ENGINE_ELO

stockfish = Stockfish("./stockfish-ubuntu-x86-64-modern")

class ChessEngine:
    def __init__(self):
        stockfish.set_elo_rating(ENGINE_ELO)

    def select_move(self, board):
        stockfish.set_fen_position(board.fen())
        return Move.from_uci(stockfish.get_best_move())
    
chess_engine = ChessEngine()