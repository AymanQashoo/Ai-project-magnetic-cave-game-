import sys
import time

# Constants
EMPTY = "_"
PLAYER1 = "■"
PLAYER2 = "□"
WINNING_LENGTH = 5
BOARD_SIZE = 8

# Create an empty game board
board = []
for _ in range(BOARD_SIZE):
    row = [EMPTY] * BOARD_SIZE
    board.append(row)

# Function to print the game board
def print_board():
    print("  " + " ".join([chr(ord('a') + i) for i in range(BOARD_SIZE)]))
    for i, row in enumerate(board):
        print(str(i + 1) + " " + " ".join(row) + " " + str(i + 1))
    print("  " + " ".join([chr(ord('a') + i) for i in range(BOARD_SIZE)]))

# Function to check if a move is valid
def is_valid_move(row, col):
    if 0 <= row < BOARD_SIZE and 0 <= col < BOARD_SIZE:
        if (col == 0 or board[row][col-1] != EMPTY) or (col == BOARD_SIZE-1 or board[row][col+1] != EMPTY):
            return board[row][col] == EMPTY
    return False

# Function to check if the game has ended
def is_game_over():
    return is_winner(PLAYER1) or is_winner(PLAYER2) or is_board_full()

# Function to check if the board is full
def is_board_full():
    for row in board:
        if EMPTY in row:
            return False
    return True

# Function to check if a player has won
def is_winner(player):
    # Check rows
    for row in board:
        count = 0
        for cell in row:
            if cell == player:
                count += 1
                if count == WINNING_LENGTH:
                    return True
            else:
                count = 0

    # Check columns
    for col in range(BOARD_SIZE):
        count = 0
        for row in range(BOARD_SIZE):
            if board[row][col] == player:
                count += 1
                if count == WINNING_LENGTH:
                    return True
            else:
                count = 0

    # Check diagonals
    for row in range(BOARD_SIZE):
        for col in range(BOARD_SIZE):
            count = 0
            for i in range(WINNING_LENGTH):
                if row + i < BOARD_SIZE and col + i < BOARD_SIZE:
                    if board[row + i][col + i] == player:
                        count += 1
                        if count == WINNING_LENGTH:
                            return True
                    else:
                        count = 0

            count = 0
            for i in range(WINNING_LENGTH):
                if row + i < BOARD_SIZE and col - i >= 0:
                    if board[row + i][col - i] == player:
                        count += 1
                        if count == WINNING_LENGTH:
                            return True
                    else:
                        count = 0

    return False

# Function to make a move
def make_move(player, row, col):
    board[row][col] = player

# Function to undo a move
def undo_move(row, col):
    board[row][col] = EMPTY

# Minimax algorithm with alpha-beta pruning
def minimax(player, depth, alpha, beta):
    if depth == 0 or is_game_over():
        return evaluate()

    if player == PLAYER1:  # Maximizer's turn
        max_eval = float('-inf')
        for row in range(BOARD_SIZE):
            for col in range(BOARD_SIZE):
                if is_valid_move(row, col):
                    make_move(PLAYER1, row, col)
                    eval = minimax(PLAYER2, depth - 1, alpha, beta)
                    undo_move(row, col)
                    max_eval = max(max_eval, eval)
                    alpha = max(alpha, eval)
                    if beta <= alpha:
                        break  # Beta cut-off
        return max_eval
    else:  # Minimizer's turn
        min_eval = float('inf')
        for row in range(BOARD_SIZE):
            for col in range(BOARD_SIZE):
                if is_valid_move(row, col):
                    make_move(PLAYER2, row, col)
                    eval = minimax(PLAYER1, depth - 1, alpha, beta)
                    undo_move(row, col)
                    min_eval = min(min_eval, eval)
                    beta = min(beta, eval)
                    if beta <= alpha:
                        break  # Alpha cut-off
        return min_eval
def get_possible_moves():
    moves = []
    for row in range(BOARD_SIZE):
        for col in range(BOARD_SIZE):
            if is_valid_move(row, col):
                moves.append((row, col))
    return moves

# Recursive function to find the best move using minimax algorithm with alpha-beta pruning
def find_best_move(player, depth, alpha=float('-inf'), beta=float('inf')):
    best_eval = float('-inf') if player == PLAYER1 else float('inf')
    best_move = None

    if depth == 0 or is_game_over():
        return evaluate(), best_move

    possible_moves = get_possible_moves()

    for move in possible_moves:
        make_move(player, move[0], move[1])
        eval = find_best_move(PLAYER2 if player == PLAYER1 else PLAYER1, depth - 1, alpha, beta)[0]
        undo_move(move[0], move[1])

        if player == PLAYER1 and eval > best_eval:
            best_eval = eval
            best_move = move
            alpha = max(alpha, best_eval)
        elif player == PLAYER2 and eval < best_eval:
            best_eval = eval
            best_move = move
            beta = min(beta, best_eval)

        if beta <= alpha:
            break

    return best_eval, best_move

# Function to get the move from the player
def get_player_move(player):
    while True:
        move = input("Enter your move (row and column): ")
        if len(move) == 2 and move[0].isdigit() and move[1].isalpha():
            row = int(move[0]) - 1
            col = ord(move[1].lower()) - ord('a')
            if is_valid_move(row, col):
                return row, col
        print("Invalid move. Try again.")

# Function to get the move from the AI player
def get_computer_move(player, depth):
    print(player + "'s turn")
    start_time = time.time()
    best_move = find_best_move(player, depth)[1]
    end_time = time.time()
    print("computer move found in {:.3f} seconds".format(end_time - start_time))
    return best_move

# Function to evaluate the current state of the board
def evaluate():
    score = 0

    def evaluate_window(window):
        score = 0
        player_count = window.count(PLAYER1)
        opponent_count = window.count(PLAYER2)

        if player_count == 0:
            if opponent_count == 1:
                score -= 1
            elif opponent_count == 2:
                score -= 10
            elif opponent_count == 3:
                score -= 100
            elif opponent_count == 4:
                score -= 1000
        elif opponent_count == 0:
            if player_count == 1:
                score += 1
            elif player_count == 2:
                score += 10
            elif player_count == 3:
                score += 100
            elif player_count == 4:
                score += 1000
        else:
            return 0  # Window contains both player's and opponent's pieces, no score

        # Give higher score for windows that have a higher number of the computer player's pieces
        if player_count > 0:
            score *= 2

        # Give even higher score if the window has a potential to win
        if player_count == WINNING_LENGTH - 1 and opponent_count == 0:
            score *= 10

        return score

    # Evaluate rows
    for row in board:
        for i in range(BOARD_SIZE - WINNING_LENGTH + 1):
            window = row[i:i+WINNING_LENGTH]
            score += evaluate_window(window)

    # Evaluate columns
    for col in range(BOARD_SIZE):
        for i in range(BOARD_SIZE - WINNING_LENGTH + 1):
            window = [board[j][col] for j in range(i, i+WINNING_LENGTH)]
            score += evaluate_window(window)

    # Evaluate diagonals (positive slope)
    for i in range(BOARD_SIZE - WINNING_LENGTH + 1):
        for j in range(BOARD_SIZE - WINNING_LENGTH + 1):
            window = [board[i+k][j+k] for k in range(WINNING_LENGTH)]
            score += evaluate_window(window)

    # Evaluate diagonals (negative slope)
    for i in range(BOARD_SIZE - WINNING_LENGTH + 1):
        for j in range(WINNING_LENGTH - 1, BOARD_SIZE):
            window = [board[i+k][j-k] for k in range(WINNING_LENGTH)]
            score += evaluate_window(window)

    return score


# Function for manual move entry
def manual_move(player):
    print(f"{player}'s turn!")
    while True:
        try:
            move = input("Enter the move (row and column): ")
            if len(move) == 2 and move[0].isdigit() and move[1].isalpha():
                row = int(move[0]) - 1
                col = ord(move[1].lower()) - ord('a')
                if is_valid_move(row, col):
                    make_move(player, row, col)
                    print_board()
                    if is_winner(player):
                        print(f"{player} wins!")
                        break
                    elif is_board_full():
                        print("It's a tie!")
                    else:
                        break
                else:
                    print("Invalid move. Try again.")
            else:
                print("Invalid input. Try again.")
        except ValueError:
            print("Invalid input. Try again.")

def manual_vs_manual():
    print("Manual vs. Manual Mode")
    while not is_game_over():
        manual_move(PLAYER1)
        if is_game_over():
            break
        manual_move(PLAYER2)

# Function to start the manual vs. computer game
def manual_vs_computer(depth):
    print("Manual vs. computer Mode")
    print_board()
    while not is_game_over():
        # Player's turn
        row, col = get_player_move(PLAYER1)
        make_move(PLAYER1, row, col)
        print_board()
        if is_game_over():
            break

        # computer's turn
        row, col = get_computer_move(PLAYER2, depth)
        make_move(PLAYER2, row, col)
        print_board()

    if is_winner(PLAYER1):
        print("You win!")
    elif is_winner(PLAYER2):
        print("computer wins!")
    else:
        print("It's a tie!")
def computer_vs_manual(depth):
    print("Computer vs. Manual Mode")
    print_board()
    while not is_game_over():
        # Computer's turn
        row, col = get_computer_move(PLAYER1, depth)
        make_move(PLAYER1, row, col)
        print("Computer played: " + str(row+1) + chr(ord('a') + col))
        print_board()
        if is_game_over():
            break

        # Player's turn
        row, col = get_player_move(PLAYER2)
        make_move(PLAYER2, row, col)
        print_board()

    if is_winner(PLAYER1):
        print("Computer wins!")
    elif is_winner(PLAYER2):
        print("You win!")
    else:
        print("It's a tie!")

# Main function
def select_play_mode():
    print("Welcome to Magnetic Cave!")
    print_board()
    print("Select play mode:")
    print("1. Manual vs. Manual")
    print("2. Manual vs. computer")
    print("3. Computer vs. Manual")
    print("4.exit")
    mode = int(input("Enter the mode number: "))
    if mode == 1:
        manual_vs_manual()
    elif mode == 2:
        depth = int(input("Enter the depth of the search for the computer : "))
        manual_vs_computer(depth)
    elif mode == 3:
        depth = int(input("Enter the depth of the search for the computer : "))
        computer_vs_manual(depth)
    elif mode == 4:
        sys.exit()
    else:
        print("Invalid mode number. Try again.")

# Start the game
select_play_mode()


