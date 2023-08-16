Trabalho de implementação de uma IA para jogar xadrez

Este é um projeto de Jogo de Xadrez em Python que inclui um motor de xadrez capaz de jogar contra jogadores humanos ou outros motores. 
O projeto oferece uma interface de linha de comando (CLI) para configurar e jogar partidas de xadrez.

Recursos

    Jogar partidas de xadrez contra o computador (IA) ou outro jogador humano.
    Testar a força da IA contra um motor de xadrez conhecido para estimar sua classificação ELO.
    Visualizar o tabuleiro de xadrez com renderização gráfica (opcional, disponível apenas para certos modos).
    Opções personalizáveis para controlar as peças brancas e pretas: jogador humano, CPU ou motor Stockfish.
    Capacidade de iniciar a partir de uma posição específica do tabuleiro usando uma representação de bitboard.

Requisitos

    Python 3
    Biblioteca pygame
    Biblioteca chess


Opções disponíveis:
    -t, --test-elo: Testar a força da IA repetidamente contra um motor de xadrez conhecido para estimar sua classificação ELO.
    -r, --render: Ativar visualização gráfica (apenas aplicável ao jogar contra o motor).
    -n, --number-of-tests: Especifique o número de rodadas de teste a serem executadas (padrão: 8).
    -o, --output: Forneça um caminho para um arquivo para armazenar o registro de teste.
    -w, --whites: Especifique quem controla as peças brancas (Opções: Jogador, IA, Motor).
    -b, --blacks: Especifique quem controla as peças pretas (Opções: Jogador, IA, Motor).
    -bb, --board: Forneça uma representação de bitboard da posição inicial do tabuleiro. Se não for fornecida, a posição inicial padrão será usada.

Exemplo(Jogador controla a peça branca e a IA controla a peça preta):
python main.py -w 1 -b 2
