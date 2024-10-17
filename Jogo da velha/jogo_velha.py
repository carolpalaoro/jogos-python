import time
import os
import random
from colorama import Fore, Back, Style, init

# Inicializa o colorama para funcionar corretamente em diferentes sistemas operacionais
init(autoreset=True)

def clear_screen():
    """Limpa a tela do console."""
    os.system('cls' if os.name == 'nt' else 'clear')

def load_animation():
    """Exibe uma animação de carregamento."""
    clear_screen()
    for i in range(101):
        print(f"\rCarregando... [{('█' * (i // 5)).ljust(20)}] {i}%", end="", flush=True)
        time.sleep(0.02)
    clear_screen()

def print_board(board, show_numbers=False):
    """Imprime o tabuleiro do jogo."""
    if show_numbers:
        print("\n" + Fore.CYAN + "   1   2   3")
    else:
        print()  # Adiciona uma linha em branco para manter o espaçamento vertical

    for i, row in enumerate(board):
        if show_numbers:
            print(Fore.CYAN + f"{i+1} ", end="")
        else:
            print("  ", end="")  # Adiciona espaço para alinhar quando não mostrar números
        print(" " + " │ ".join([cell_color(cell) for cell in row]))
        if i < 2:
            print("  " + "───┼───┼───")  # Adiciona espaços no início para alinhar

def cell_color(cell):
    """Retorna a célula colorida de acordo com seu conteúdo."""
    if cell == 'X':
        return Fore.RED + cell + Style.RESET_ALL
    elif cell == 'O':
        return Fore.GREEN + cell + Style.RESET_ALL
    else:
        return cell

def get_player_move(board):
    """Obtém a jogada do jogador humano."""
    while True:
        try:
            move = input("\nFaça sua jogada (linha coluna): ").split()
            row, col = int(move[0]) - 1, int(move[1]) - 1
            if 0 <= row <= 2 and 0 <= col <= 2 and board[row][col] == ' ':
                return row, col
            else:
                print(Fore.YELLOW + "Jogada inválida. Tente novamente.")
        except (ValueError, IndexError):
            print(Fore.YELLOW + "Entrada inválida. Use dois números separados por espaço.")

def get_computer_move(board):
    """Obtém uma jogada aleatória para o computador."""
    available_moves = [(i, j) for i in range(3) for j in range(3) if board[i][j] == ' ']
    return random.choice(available_moves)

def check_winner(board):
    """Verifica se há um vencedor."""
    # Linhas e colunas
    for i in range(3):
        if board[i][0] == board[i][1] == board[i][2] != ' ':
            return board[i][0]
        if board[0][i] == board[1][i] == board[2][i] != ' ':
            return board[0][i]
    # Diagonais
    if board[0][0] == board[1][1] == board[2][2] != ' ':
        return board[0][0]
    if board[0][2] == board[1][1] == board[2][0] != ' ':
        return board[0][2]
    return None

def is_board_full(board):
    """Verifica se o tabuleiro está cheio."""
    return all(cell != ' ' for row in board for cell in row)

def print_winner(winner):
    """Imprime a mensagem de vitória."""
    color = Fore.RED if winner == 'X' else Fore.GREEN
    print(color + f"\n{winner} GANHOU!" + Style.RESET_ALL)
    print(color + """
     ___________
    '._==_==_=_.'
    .-\\:      /-.
   | (|:.     |) |
    '-|:.     |-'
      \\::.    /
       '::. .'
         ) (
       _.' '._
      `"""""""`
    """)

def print_draw():
    """Imprime a mensagem de empate."""
    print(Fore.YELLOW + "\nEMPATE!" + Style.RESET_ALL)
    print(Fore.YELLOW + """
       ___________
      /           \\
     /   EMPATE!   \\
    |   ┏━━━┓ ┏━━━┓ |
    |   ┃┏━┓┃ ┃┏━┓┃ |
    |   ┗┛ ┃┃ ┗┛ ┃┃ |
    |      ┃┃    ┃┃ |
    |   ┏━━┛┃ ┏━━┛┃ |
    |   ┗━━━┛ ┗━━━┛ |
     \\             /
      \\___________/
    """)

def play_game():
    """Função principal do jogo."""
    board = [[' ' for _ in range(3)] for _ in range(3)]
    current_player = 'X'  # O jogador humano (X) sempre começa
    show_numbers = input("Deseja ver os números das linhas e colunas? (S/N): ").lower() == 's'

    while True:
        clear_screen()
        print_board(board, show_numbers)

        if current_player == 'X':
            row, col = get_player_move(board)
        else:
            print("\nComputador está jogando...")
            time.sleep(1)  # Pequena pausa para simular o "pensamento" do computador
            row, col = get_computer_move(board)

        board[row][col] = current_player

        winner = check_winner(board)
        if winner:
            clear_screen()
            print_board(board, show_numbers)
            print_winner(winner)
            return winner
        elif is_board_full(board):
            clear_screen()
            print_board(board, show_numbers)
            print_draw()
            return None

        current_player = 'O' if current_player == 'X' else 'X'

def main():
    """Função principal do programa."""
    load_animation()
    print(Fore.CYAN + Style.BRIGHT + "Bem-vindo ao Jogo da Velha!" + Style.RESET_ALL)
    print("Você jogará como 'X' e sempre começará o jogo. O computador jogará como 'O'.")

    scores = {'X': 0, 'O': 0, 'Empates': 0}
    total_games = 0

    while True:
        winner = play_game()
        total_games += 1

        if winner:
            scores[winner] += 1
        else:
            scores['Empates'] += 1

        print(f"\n{Fore.CYAN}Placar:")
        print(f"{Fore.RED}Você (X): {scores['X']}")
        print(f"{Fore.GREEN}Computador (O): {scores['O']}")
        print(f"{Fore.YELLOW}Empates: {scores['Empates']}")
        print(f"{Fore.CYAN}Total de partidas: {total_games}")

        play_again = input("\nDeseja jogar novamente? (S/N): ").lower()
        if play_again != 's':
            print(Fore.CYAN + "Obrigado por jogar! Até a próxima!")
            break

if __name__ == "__main__":
    main()