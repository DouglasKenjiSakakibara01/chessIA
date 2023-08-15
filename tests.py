import chess

from chessIA import chess_ai
from chessEngine import chess_engine
from chessGame import ChessGame
from consts import *
import util

def test_elo(n=8, render=False):
    ia_whites = True
    players = (AI, ENGINE)
    wins, losses, draws = 0, 0, 0
    score = 0

    test_fun = test_on_render if render else test_on_console

    for i in range(n):
        util.logging.log(f"\nTest {i + 1}")
        result = test_fun(players)

        if result is None:
            break

        if result == "1/2-1/2":
            draws += 1
            score += 1/2
        elif (result == "1-0" and ia_whites) or (result == "0-1" and not ia_whites):
            wins += 1
            score += 1
        else:
            losses += 1
        util.logging.log(f"\nResult: {result}")
        util.logging.log(f"\nWins: {wins} | Losses: {losses} | Draws: {draws}\n")
        ia_whites = not ia_whites
        players = players[::-1]
    
    elo = ENGINE_ELO + FIDE_INITIAL_LOOKUP[score]

    util.logging.log(f"\nScore: {score}")
    util.logging.log(f"\nELO: {elo}")
    
def test_on_console(players):
    board = chess.Board()
    (whites_player, blacks_player) = (chess_ai if p == AI else chess_engine for p in players)
    
    while not board.is_game_over(claim_draw=True):
        move = whites_player.select_move(board) if board.turn else blacks_player.select_move(board)
        util.logging.log_move(board.turn, board.fullmove_number, board.san(move))
        board.push(move)

    return board.outcome(claim_draw=True).result()

def test_on_render(players):
    game = ChessGame()
    return game.play(players)
