import sys
import chess

class ChessIA:
    def __init__(self):
        #tabelas de pontuacao de cada posicao da peça do jogo
        self.pawn = [
        0, 0, 0, 0, 0, 0, 0, 0,
        5, 10, 10, -20, -20, 10, 10, 5,
        5, -5, -10, 0, 0, -10, -5, 5,
        0, 0, 0, 20, 20, 0, 0, 0,
        5, 5, 10, 25, 25, 10, 5, 5,
        10, 10, 20, 30, 30, 20, 10, 10,
        50, 50, 50, 50, 50, 50, 50, 50,
        0, 0, 0, 0, 0, 0, 0, 0]

        self.knight = [
        -50, -40, -30, -30, -30, -30, -40, -50,
        -40, -20, 0, 5, 5, 0, -20, -40,
        -30, 5, 10, 15, 15, 10, 5, -30,
        -30, 0, 15, 20, 20, 15, 0, -30,
        -30, 5, 15, 20, 20, 15, 5, -30,
        -30, 0, 10, 15, 15, 10, 0, -30,
        -40, -20, 0, 0, 0, 0, -20, -40,
        -50, -40, -30, -30, -30, -30, -40, -50]
        
        self.bishop = [
        -20, -10, -10, -10, -10, -10, -10, -20,
        -10, 5, 0, 0, 0, 0, 5, -10,
        -10, 10, 10, 10, 10, 10, 10, -10,
        -10, 0, 10, 10, 10, 10, 0, -10,
        -10, 5, 5, 10, 10, 5, 5, -10,
        -10, 0, 5, 10, 10, 5, 0, -10,
        -10, 0, 0, 0, 0, 0, 0, -10,
        -20, -10, -10, -10, -10, -10, -10, -20]
        
        self.rook = [
        0, 0, 0, 5, 5, 0, 0, 0,
        -5, 0, 0, 0, 0, 0, 0, -5,
        -5, 0, 0, 0, 0, 0, 0, -5,
        -5, 0, 0, 0, 0, 0, 0, -5,
        -5, 0, 0, 0, 0, 0, 0, -5,
        -5, 0, 0, 0, 0, 0, 0, -5,
        5, 10, 10, 10, 10, 10, 10, 5,
        0, 0, 0, 0, 0, 0, 0, 0]
        
        self.queen = [
        -20, -10, -10, -5, -5, -10, -10, -20,
        -10, 0, 0, 0, 0, 0, 0, -10,
        -10, 5, 5, 5, 5, 5, 0, -10,
        0, 0, 5, 5, 5, 5, 0, -5,
        -5, 0, 5, 5, 5, 5, 0, -5,
        -10, 0, 5, 5, 5, 5, 0, -10,
        -10, 0, 0, 0, 0, 0, 0, -10,
        -20, -10, -10, -5, -5, -10, -10, -20]
        
        self.king = [
        20, 30, 10, 0, 0, 10, 30, 20,
        20, 20, 0, 0, 0, 0, 20, 20,
        -10, -20, -20, -20, -20, -20, -20, -10,
        -20, -30, -30, -40, -40, -30, -30, -20,
        -30, -40, -40, -50, -50, -40, -40, -30,
        -30, -40, -40, -50, -50, -40, -40, -30,
        -30, -40, -40, -50, -50, -40, -40, -30,
        -30, -40, -40, -50, -50, -40, -40, -30]
       
        

    def evaluate_board(self,board):
        if board.is_checkmate():
                if board.turn:
                    return -9999
                else:
                    return 9999
        if board.is_stalemate():
                return 0
        if board.is_insufficient_material():
                return 0

        wp = len(board.pieces(chess.PAWN, chess.WHITE))
        bp = len(board.pieces(chess.PAWN, chess.BLACK))
        wn = len(board.pieces(chess.KNIGHT, chess.WHITE))
        bn = len(board.pieces(chess.KNIGHT, chess.BLACK))
        wb = len(board.pieces(chess.BISHOP, chess.WHITE))
        bb = len(board.pieces(chess.BISHOP, chess.BLACK))
        wr = len(board.pieces(chess.ROOK, chess.WHITE))
        br = len(board.pieces(chess.ROOK, chess.BLACK))
        wq = len(board.pieces(chess.QUEEN, chess.WHITE))
        bq = len(board.pieces(chess.QUEEN, chess.BLACK))

        material = 100 * (wp - bp) + 320 * (wn - bn) + 330 * (wb - bb) + 500 * (wr - br) + 900 * (wq - bq)

        pawnsq = sum([self.pawn[i] for i in board.pieces(chess.PAWN, chess.WHITE)])
        pawnsq = pawnsq + sum([-self.pawn[chess.square_mirror(i)]
                                for i in board.pieces(chess.PAWN, chess.BLACK)])
        knightsq = sum([self.knight[i] for i in board.pieces(chess.KNIGHT, chess.WHITE)])
        knightsq = knightsq + sum([-self.knight[chess.square_mirror(i)]
                                    for i in board.pieces(chess.KNIGHT, chess.BLACK)])
        bishopsq = sum([self.bishop[i] for i in board.pieces(chess.BISHOP, chess.WHITE)])
        bishopsq = bishopsq + sum([-self.bishop[chess.square_mirror(i)]
                                    for i in board.pieces(chess.BISHOP, chess.BLACK)])
        rooksq = sum([self.rook[i] for i in board.pieces(chess.ROOK, chess.WHITE)])
        rooksq = rooksq + sum([-self.rook[chess.square_mirror(i)]
                                for i in board.pieces(chess.ROOK, chess.BLACK)])
        queensq = sum([self.queen[i] for i in board.pieces(chess.QUEEN, chess.WHITE)])
        queensq = queensq + sum([-self.queen[chess.square_mirror(i)]
                                for i in board.pieces(chess.QUEEN, chess.BLACK)])
        kingsq = sum([self.king[i] for i in board.pieces(chess.KING, chess.WHITE)])
        kingsq = kingsq + sum([-self.king[chess.square_mirror(i)]
                                for i in board.pieces(chess.KING, chess.BLACK)])
        
        score = material + pawnsq + knightsq + bishopsq + rooksq + queensq + kingsq
        if board.turn:
            return score
        else:
            return -score
    #melhora a avaliacao dos movimentos no tabuleiro
    def quiesce(self,alpha, beta,board):
        stand_pat = self.evaluate_board(board)
        if (stand_pat >= beta):
            return beta
        if (stand_pat > alpha):
            alpha = stand_pat

        for move in board.legal_moves:
            #se o movimento gerar uma captura da peça, deve simular essa captura
            if board.is_capture(move):
                board.push(move)
                score = -self.quiesce(-beta, -alpha,board)
                board.pop()
                if (score >= beta):
                    return beta
                if (score > alpha):
                    alpha = score
        return alpha        
    #otimiza a eficienca da busca pelos melhores movimentos e reduz o numero de posicoes explorados
    def alpha_beta(self,alpha, beta, depthleft,board):
        bestscore = -9999
        if (depthleft == 0):
            return self.quiesce(alpha, beta,board)
        
        for move in board.legal_moves:
            board.push(move)
            score = -self.alpha_beta(-beta, -alpha, depthleft - 1, board)
            board.pop()
            if (score >= beta):
                return score
            if (score > bestscore):
                bestscore = score
            if (score > alpha):
                alpha = score
        return bestscore
     
#escolhe o melhor movimento posssivel para o jogador
    def select_move(self,depth,board):
        bestMove = chess.Move.null()
        bestValue = -99999
        alpha = -100000
        beta = 100000#score maximo
        #testa todos os movimentos possiveis do jogador
        for move in board.legal_moves:
            board.push(move)
            boardValue = -self.alpha_beta(-beta, -alpha, depth - 1,board)
            if boardValue > bestValue:
                bestValue = boardValue
                bestMove = move
            if boardValue > alpha:
                alpha = boardValue
            board.pop()
        return bestMove
     

    

