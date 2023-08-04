import pygame
import argparse

from chessGame import ChessGame

parser = argparse.ArgumentParser("chess")
group = parser.add_mutually_exclusive_group()
group.add_argument("-d", "--dynamic", action="store_true", help="Starts the game on dynamic mode, showing an options menu for the user to choose from")
group.add_argument("-c", "--console", action="store_true", help="Starts the game immediately with the passed args (use 'console --help' for more info)")
subparsers = parser.add_subparsers()
parser_console = subparsers.add_parser("console", help="Arguments for starting the game from the console")
parser_console.add_argument("-w", "--whites", choices=["p", "c"], required=True, type=str, help="Who controls the white pieces (<p>layer or <c>PU)")
parser_console.add_argument("-b", "--blacks", choices=["p", "c"], required=True, type=str, help="Who controls the black pieces (<p>layer or <c>PU")
parser_console.add_argument("-bb", "--bitboard", type=str, required=False, help="Bitboard string defining the starting position.")

pygame.init()

qstGame = '''
███ █ █ ███ ███ ███
█   █▄█ █▄  █▄▄ █▄▄
███ █ █ █▄▄ ▄▄█ ▄▄█

<1> Novo Jogo
<2> Carregar Posição
<0> Sair
=> '''

qstPlayers = '''
<1> Jogador x IA
<2> IA x IA
<3> Jogador x Jogador
<0> Sair
=> '''

def main():
    args = parser.parse_args()
    if not args.console:
        optGame = int(input(qstGame))
        board = input("Insira o bitboard => ") if optGame == 2 else None
        optPlayers = int(input(qstPlayers))
        if optPlayers == 1:
            players = (True, False)
        elif optPlayers == 2:
            players = (False, False)
        elif optPlayers == 3:
            players=(True,True)
    else:
        
        board = args.bitboard
        players = (args.whites == "p", args.blacks == "p")


    game = ChessGame(board)
    game.play(players)

    print('Jogo encerrado')
    pygame.quit()


if __name__ == '__main__':
    main()