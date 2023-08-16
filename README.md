# Trabalho de implementação de uma IA para jogar xadrez

Este é um projeto de Jogo de Xadrez em Python que inclui uma IA de xadrez capaz de jogar contra jogadores humanos ou outros motores. 
O projeto oferece uma interface de linha de comando (CLI) para configurar e jogar partidas de xadrez.

## Recursos

- Jogar partidas de xadrez contra o computador (IA) ou outro jogador humano.
- Testar a força da IA contra um motor de xadrez conhecido para estimar sua classificação ELO.
- Visualizar o tabuleiro de xadrez com renderização gráfica (opcional, disponível apenas para certos modos).
- Opções personalizáveis para controlar as peças brancas e pretas: jogador humano, CPU ou motor Stockfish.
- Capacidade de iniciar a partir de uma posição específica do tabuleiro usando uma representação de bitboard.

## Requisitos

O programa foi desenvolvido para Linux com python 3.9. São necessárias as bibliotecas pygame e chess, ambas disponíveis para instalação por pip. Para windows, os testes foram executados apenas com WSL, mas deve ser possível executar o programa substituindo o binário do stockfish pela versão para Windows.

## Uso

    python3 main.py [ -t [-r] [-n N] | -w WHITES -b BLACKS [ -bb BITBOARD ] ] [-o OUTPUT]

#### Para testes:
    -t, --test-elo: Testar a força da IA repetidamente contra um motor de xadrez conhecido para estimar sua classificação ELO.
    -r, --render: Ativar visualização gráfica enquanto executa os testes.
    -n, --number-of-tests: Especifique o número de rodadas de teste a serem executadas (ATUALMENTE SUPORTE APENAS PARA n=8).
#### Para uma partida isolada:
    -w, --whites: Especifique quem controla as peças brancas (Opções: Jogador (1), IA (2), Motor (3)).
    -b, --blacks: Especifique quem controla as peças pretas (Opções: Jogador (1), IA (2), Motor (3)).
    -bb, --board: Forneça uma representação de bitboard da posição inicial do tabuleiro. Se não for fornecida, a posição inicial padrão será usada.

#### Outros:
    -o, --output: Forneça um caminho para um arquivo para armazenar o registro de teste.

## Configuração

Os parâmetros de configuração podem ser alterados modificando o arquivo [consts.py](https://github.com/DouglasKenjiSakakibara01/chessIA/blob/master/consts.py). Os principais parâmetros são `AI_DEPTH`, que define a profundidade da busca para a IA, e `ENGINE_ELO`, que define o ELO do motor contra qual a IA será testada. Outros parâmetros incluem configurações gráficas e de algumas das heurísticas.

## Exemplos:

#### Para uma partida entre jogador (brancas) contra IA (pretas)
    python main.py -w 1 -b 2

#### Para visualizar como a IA procede como ela mesma a partir de uma posição:
    python main.py -w 2 -b 2 -bb "rn1qk2b/ppppp1Pp/8/5p1n/8/3b4/1P1Q4/1RB1KBNR w Kq - 0 1"

#### Para estimar o ELO da IA mostrando graficamente e salvando o log em um arquivo
    python main.py -t -r -o test.txt

## Autores

Desenvolvido durante a matéria de Introdução a Inteligência Artificial do Prof. Wagner Igarashi no curso de Ciência da Computação pela UEM.

RA117306
Felipe Gabriel Comin Scheffel


RA117741
Douglas Kenji Sakakibara
