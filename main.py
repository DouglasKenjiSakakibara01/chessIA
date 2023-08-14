import pygame
import argparse
from chessGame import ChessGame

playerOpts = {
    0: None,
    1: "Player",
    2: "CPU",
    3: "Stockfish"
}

def main():
    parser = argparse.ArgumentParser(description="Chess Game")
    parser.add_argument("-w", "--whites", required=True, type=int, choices=[1, 2, 3], help="Quem controlará as peças brancas (Player, CPU, Stockfish)")
    parser.add_argument("-b", "--blacks", required=True, type=int, choices=[1, 2, 3], help="Quem controlará as peças pretas  (Player, CPU, Stockfish)")
    parser.add_argument("-bb", "--board", required=False, type=str, help="Bitboard da posição do tabuleiro. Se nulo, começa na posição inicial padrão")
    args = parser.parse_args()

    board = args.board if args.board else None

    playerWhites = playerOpts[args.whites] if args.whites else None
    if playerWhites is None:
        print("Opção para peças brancas não fornecida.")
        exit()

    playerBlacks = playerOpts[args.blacks] if args.blacks else None
    if playerBlacks is None:
        print("Opção para peças pretas não fornecida.")
        exit()

    pygame.init()

    game = ChessGame(board)
    game.play((playerWhites, playerBlacks))

    print('Jogo encerrado')
    pygame.quit()

if __name__ == '__main__':
    main()
