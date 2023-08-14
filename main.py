import pygame

from chessGame import ChessGame

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
<2> IA x Stockfish
<3> Jogador x Jogador
<0> Sair
=> '''

def main():
    optGame = int(input(qstGame))
    if optGame == 0: exit()
    board = input("Insira o bitboard => ") if optGame == 2 else None
    optPlayers = int(input(qstPlayers))
    if optPlayers == 0: exit()
    if optPlayers == 1:
        players = ('Player', 'CPU')
    elif optPlayers == 2:
        players = ('CPU', 'Stockfish')
    elif optPlayers == 3:
        players=('Player', 'Player')

    game = ChessGame(board)
    game.play(players)

    print('Jogo encerrado')
    pygame.quit()


if __name__ == '__main__':
    main()