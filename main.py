import pygame
import argparse

from chessGame import ChessGame
from tests import test_engine
from consts import PLAYER, AI, ENGINE
import util

def main():
    parser = argparse.ArgumentParser(description="Chess Game")
    parser.add_argument("-t", "--test-vs-engine", required=False, action="store_true", help="Executar a IA contra o Stockfish alternadamente")
    parser.add_argument("-r", "--render", required=False, action="store_true", help="Ativar visualização gráfica (apenas se test-vs-engine for passada)")
    parser.add_argument("-n", "--number-of-tests", required=False, type=int, help="Quantas rodadas de testes devem ser executadas")
    parser.add_argument("-o", "--output", required=False, type=str, help="Caminho para o arquivo que conterá o log dos testes")
    parser.add_argument("-w", "--whites", required=False, type=int, choices=[PLAYER, AI, ENGINE], help="Quem controlará as peças brancas (Player, CPU, Stockfish)")
    parser.add_argument("-b", "--blacks", required=False, type=int, choices=[PLAYER, AI, ENGINE], help="Quem controlará as peças pretas (Player, CPU, Stockfish)")
    parser.add_argument("-bb", "--board", required=False, type=str, help="Bitboard da posição do tabuleiro. Se nulo, começa na posição inicial padrão")
    args = parser.parse_args()

    if args.output is not None:
        f = open(args.output, "w")
        util.logging.set_out_file(f)

    if args.test_vs_engine:
        test_engine(args.number_of_tests, args.render)
    else:
        board = args.board if args.board else None

        if not args.whites:
            print("Opção para peças brancas não fornecida.")
            exit()
        playerWhites = args.whites

        if args.blacks is None:
            print("Opção para peças pretas não fornecida.")
            exit()
        playerBlacks = args.blacks

        game = ChessGame(board)
        result = game.play((playerWhites, playerBlacks))
        if result is not None: print(result)

        print('\nJogo encerrado')
        pygame.quit()

    if f is not None:
        f.close()
        util.logging.set_out_file(None)

if __name__ == '__main__':
    main()
