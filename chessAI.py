import chess
import math
import random

from consts import *

class ChessAI:
    def __init__(self):
        self.transposition_table = {}

    def evaluate_board(self, board):
        if board.is_game_over():
            result = board.outcome(claim_draw=True).result()
            if result == "1-0": return math.inf if board.turn else -math.inf
            if result == "0-1": return -math.inf if board.turn else math.inf
            else: return 0

        # Avalia a quantidade de cada peça
        material = sum([MATERIAL_VALUES[piece] * (len(board.pieces(piece, chess.WHITE)) - len(board.pieces(piece, chess.BLACK))) for piece in PIECES[:-1]])
        # Avalia quão bem posicionada cada peça está
        score = sum([sum([SCORE_VALUES[piece][i] for i in board.pieces(piece, chess.WHITE)]) +
                 sum([-SCORE_VALUES[piece][chess.square_mirror(i)] for i in board.pieces(piece, chess.BLACK)]) for piece in PIECES])
        evaluation = material + score

        return evaluation if board.turn else -evaluation
    
    def quiescence_search(self, alpha: int, beta: int, board: chess.Board) -> int:
        stand_pat = self.evaluate_board(board)
        if (stand_pat >= beta): return beta
        if (stand_pat > alpha): alpha = stand_pat

        for move in board.legal_moves:
            if board.is_capture(move):
                board.push(move)
                score = -self.quiescence_search(-beta, -alpha, board)
                board.pop()
                if (score >= beta):
                    return beta
                if (score > alpha):
                    alpha = score
        return alpha
    
    def prioritize(self, move: chess.Move, board: chess.Board):
        if board.is_capture(move):
            return 100  # Prioritize captures
        if board.gives_check(move):
            return 50   # Prioritize checks
        if board.piece_at(move.from_square).piece_type == chess.PAWN:
            return 30   # Prioritize pawn moves
        if  move.to_square in (chess.E4, chess.D4, chess.E5, chess.D5):
            return 20    # Prioritize moves that control the central squares
        if [a for a in board.attacks(move.from_square) if board.piece_at(a) is not None]:
            return 10  # Prioritize attacks
        if board.piece_at(move.from_square).piece_type in (chess.KNIGHT, chess.BISHOP):
            return 10   # Prioritize knight and bishop moves for development
        if board.is_castling(move):
            return 10    # Prioritize castling
        return 0
    
    
    def negamax(self, alpha: int, beta: int, depth: int, board: chess.Board) -> int:
        alpha_orig = alpha
        hash_key = board.fen()  # Calcular um hash único para a posição do tabuleiro

        if hash_key in self.transposition_table:
            entry = self.transposition_table[hash_key]
            if entry["depth"] >= depth:
                if entry['flag'] == EXACT:
                    return entry['score']
                elif entry['flag'] == LOWERBOUND:
                    alpha = max(alpha, entry['score'])
                elif entry['flag'] == UPPERBOUND:
                    beta = min(beta, entry['score'])

                if alpha >= beta:
                    return entry['score']

        if depth <= 0: return self.quiescence_search(alpha, beta, board)

        legal_moves = list(board.legal_moves)
        sorted_moves = sorted(legal_moves, key=lambda move: self.prioritize(move, board), reverse=True)
        # move_probabilities = [(((len(sorted_moves) - i) * 4) + (1 / (depth)) / 5) for i in range(len(sorted_moves))]

        best_score = -math.inf

        # Loop para selecionar os movimentos com base nas probabilidades
        for i, move in enumerate(sorted_moves):
            # if random.random() <= move_probabilities[i] / move_probabilities[0]:
                board.push(move)
                score = -self.negamax(-beta, -alpha, depth - 1, board)
                board.pop()

                if score > best_score:
                    best_score = score
                if score > alpha:
                    alpha = score
                if alpha >= beta:
                    break

        if best_score <= alpha_orig: flag = UPPERBOUND
        elif best_score >= beta: flag = LOWERBOUND
        else: flag = EXACT
        self.update_transposition_table(hash_key, depth, best_score, flag)
        return best_score

    def update_transposition_table(self, hash_key, depth, score, flag):
        self.transposition_table[hash_key] = {'depth': depth, 'score': score, 'flag': flag}

    def select_move(self, board: chess.Board, depth: int = AI_DEPTH) -> chess.Move:
        board = board.copy()
        best_move = chess.Move.null()
        best_score = -math.inf
        alpha = -math.inf
        beta = math.inf

        for move in board.legal_moves:
            board.push(move)
            score = -self.negamax(-beta, -alpha, depth - 1, board)
            board.pop()

            if score > best_score:
                best_score = score
                best_move = move
            if score >= alpha: alpha = score
        return best_move

chess_ai = ChessAI()
