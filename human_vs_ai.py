"""
Human plays an AI (Computer)
The AI plays randomly without any strategy
"""
import random

board = [
    ["R", "N", "B", "Q", "K", "B", "N", "R"],
    ["P", "P", "P", "P", "P", "P", "P", "P"],
    [".", ".", ".", ".", ".", ".", ".", "."],
    [".", ".", ".", ".", ".", ".", ".", "."],
    [".", ".", ".", ".", ".", ".", ".", "."],
    [".", ".", ".", ".", ".", ".", ".", "."],
    ["p", "p", "p", "p", "p", "p", "p", "p"],
    ["r", "n", "b", "q", "k", "b", "n", "r"],
]

coord = { # Dictionary that translates human moves to board coordinates
    "8": 0, "7": 1, "6": 2, "5": 3, "4": 4, "3": 5, "2": 6, "1": 7, # Rows
    "a": 0, "b": 1, "c": 2, "d": 3, "e": 4, "f": 5, "g": 6, "h": 7, # Columns
}

def display_board():
    """Displays the current state of the chess board.
    Takes no argument and return None.
    """
    for row in board:
        print(row)
    print("\n")
    return None

def pawn_moves(is_white_turn, curr_pos):
    """Finds and returns all possible moves a pawn can make
    Takes a tuple of integers curr_pos and a boolean is_white_turn and 
    returns a list of tuple of integers possible moves
    """
    possible_moves = []
    row, col = curr_pos
    dxn = -1 if is_white_turn else 1 
    next_row = row + dxn

    if 0 <= next_row <= 7:
        # Normal moves
        if board[next_row][col] == '.':
            possible_moves.append((next_row, col))
            if (row == 6 and is_white_turn) or (row == 1 and not is_white_turn):
                if board[next_row + dxn][col] == '.':
                    possible_moves.append((next_row + dxn, col))
                
        # Attack moves
        for attack_col in [col - 1, col + 1]:
            if 0 <= attack_col <= 7:
                if board[next_row][attack_col] != '.' and (board[next_row][attack_col].isupper() != board[row][col].isupper()):
                    possible_moves.append((next_row, attack_col))

    return possible_moves

def rook_moves(curr_pos):
    """Finds and returns all possible moves a rook can make
    Takes a tuple of integers, curr_pos returns a list of tuple of integers, possible moves
    """
    possible_moves = []
    row, col = curr_pos

    # Define directions: right, left, down, up
    directions = [(0, 1), (0, -1), (1, 0), (-1, 0)]

    for dx, dy in directions:
        temp_row, temp_col = row, col
        while 0 <= temp_row + dx <= 7 and 0 <= temp_col + dy <= 7:
            temp_row += dx
            temp_col += dy
            move = (temp_row, temp_col)
            if board[temp_row][temp_col] == ".":  # Normal move
                possible_moves.append(move)
            else:
                if board[row][col].isupper() != board[temp_row][temp_col].isupper():  # Attack move
                    possible_moves.append(move)
                break

    return possible_moves
        
def knight_moves(curr_pos):
    """Finds and returns all possible moves a knight can make
    Takes a tuple of integers, curr_pos returns a list of tuple of integers, possible moves
    """
    possible_moves = []
    row, col = curr_pos
    changes = [2, -2, 1, -1]
    for i in changes:
        for j in changes:
            if abs(i) == abs(j): # Not a valid move for knight
                continue
            if (row+i > 7 or row+i < 0) or (col+j > 7 or col+j < 0): # Out of board
                continue
            move = (row + i, col + j)
            if (board[row+i][col+j] == ".") or (board[row][col].isupper() != board[row+i][col+j].isupper()):
                possible_moves.append(move) # Normal or Attack move
    
    return possible_moves
        
def bishop_moves(curr_pos):
    """Finds and returns all possible moves a bishop can make
    Takes a tuple of integers, curr_pos returns a list of tuple of integers, possible moves
    """
    possible_moves = []
    row, col = curr_pos

    # Define diagonal directions: top-right, top-left, bottom-left, bottom-right
    directions = [(-1, 1), (-1, -1), (1, -1), (1, 1)]

    for dx, dy in directions:
        temp_row, temp_col = row, col
        while 0 <= temp_row + dx <= 7 and 0 <= temp_col + dy <= 7:
            temp_row += dx
            temp_col += dy
            move = (temp_row, temp_col)
            if board[temp_row][temp_col] == ".":  # Normal move
                possible_moves.append(move)
            else:
                if board[row][col].isupper() != board[temp_row][temp_col].isupper():  # Attack move
                    possible_moves.append(move)
                break

    return possible_moves

def queen_moves(curr_pos):
    """Finds and returns all possible moves a queen can make
    Takes a tuple of integers, curr_pos returns a list of tuple of integers, possible moves
    """
    possible_moves = bishop_moves(curr_pos) + rook_moves(curr_pos)
    return possible_moves

def get_all_chars(is_white_turn):
    """Finds and returns the positions of all characters of a player
    Takes a boolean is_white_turn and returns a list of tuple of integers, characters
    """
    characters = []
    for i in range(8):
        for j in range(8):
            curr_char = board[i][j]
            pos = (i, j)
            if curr_char == ".":
                continue
            if is_white_turn:
                if curr_char.islower():
                    characters.append(pos)
            else:
                if curr_char.isupper():
                    characters.append(pos)
    return characters

def get_all_moves(is_white_turn):
    """Gets and returns the possibles moves of all characters(except king) of a player
    Takes a boolean is_white_turn and returns a list of list of tuple of integers, all_moves
    """
    all_characters = get_all_chars(is_white_turn)
    all_moves = []
    for pos in all_characters:
        row, col = pos
        char = board[row][col]
        if char == "p" or char == "P":
            all_moves += [[pos, new_pos] for new_pos in pawn_moves(is_white_turn, pos)]
        elif char == "r" or char == "R":
            all_moves += [[pos, new_pos] for new_pos in rook_moves(pos)]
        elif char == "n" or char == "N":
            all_moves += [[pos, new_pos] for new_pos in knight_moves(pos)]
        elif char == "b" or char == "B" :
            all_moves += [[pos, new_pos] for new_pos in bishop_moves(pos)]
        elif char == "q" or char == "Q":
            all_moves += [[pos, new_pos] for new_pos in queen_moves(pos)]
                
    return all_moves

def get_king_pos(is_white_turn):
    """Get's the current positon of the king
    Takes boolean is_white_turn and returns a tuple of integers.
    """
    king_type = "k" if is_white_turn else "K"
    for i in range(8):
        for j in range(8):
            if board[i][j] == king_type:
                return (i, j)
    return (0, 0)

def is_king_in_check(is_white_turn, curr_pos):
    """Returns True if the king of the current player is in check. Else it returns False.
    Takes boolean is_white_turn and tuple of integers curr_pos
    """
    in_check = False
    for pos in get_all_moves(not is_white_turn):
        if pos[1] == curr_pos:
            in_check = True
            break
        
    if not in_check: # Check if there's an attacking enemy king
        row, col = curr_pos
        changes = [-1, 0, 1]
        for i in changes:
            for j in changes:
                if (i == 0) and (j == 0):
                    continue
                if (row+i > 7 or row+i < 0) or (col+j > 7 or col-j < 0): # Out of board
                    continue
                if board[row+i][col+j].lower() == "k":
                    in_check = True
        
    return in_check

def reverse(prev_board):
    """Reverses the board one move back
    Takes a list of list of strings prev_board"""
    for i in range(8):
        for j in range(8):
            board[i][j] = prev_board[i][j]
    return None

def king_moves(is_white_turn, curr_pos):
    """Finds and returns all possible moves a king can make
    Takes a boolean is_white_turn and a tuple of integers curr_pos.
    """
    row, col = curr_pos
    changes = [-1, 0, 1]
    possible_moves = []
    for i in changes:
        for j in changes:
            if (i == 0) and (j == 0):
                continue
            if (row+i > 7 or row+i < 0) or (col+j > 7 or col+j < 0): # Out of board
                continue
            move = (row+i, col+j)
            # Normal or Attack moves
            if (board[row+i][col+j] == ".") or (board[row][col].isupper() != board[row+i][col+j].isupper()):
                temp_board = [row.copy() for row in board] # Save a temporay version of the board
                make_move(curr_pos, move) # Make a temporary move
                if not is_king_in_check(is_white_turn, move): # Check if the king is safe after the temporary move
                    possible_moves.append([curr_pos, move])
                reverse(temp_board) # Reverse the temporary move
                    
    return possible_moves

def make_move(curr_pos, next_pos):
    """Implements a move by replacing the character in next_pos by the character in curr_pos
    If the character that is replaced is a king, the function return False. Else it returns True
    Takes a list of tuple curr_pos and another list of typle next_pos and returns a boolean
    """
    row0, col0 = curr_pos
    row1, col1 = next_pos
    char = board[row0][col0] # Get character at current position
    attacked_char = board[row1][col1] # Get character at the position being attacked
    
    if char == "p" and (row0 != 0 and row1 == 0): # White-pawn promotion
        char = random.choice(["n", "q", "b", "r"])
    elif char == "P" and (row0 != 7 and row1 == 7): # Black-pawn promotion
        char = random.choice(["N", "Q", "B", "R"])
    
    # Move character to new position
    board[row1][col1] = char 
    board[row0][col0] = "."
    
    if attacked_char.lower() == "k":
        return False
    else:
        return True
    
def get_human_move(all_moves):
    valid_move = None
    while True:
        human_move = input("Make your move. Eg. 'b2 b3': ")
        human_move = human_move.split(" ")
        curr_pos = (coord[human_move[0][1]], coord[human_move[0][0]])
        next_pos = (coord[human_move[1][1]], coord[human_move[1][0]])
        comp_equiv = [curr_pos, next_pos]
        if comp_equiv in all_moves:
            valid_move = comp_equiv
            break
        else:
            print("Invalid move. Try again")
        
    print(valid_move)
    return valid_move


# Main game loop
def game(): 
    is_white_turn = True  # White starts
    running, draw = True, False
    winner = None
    no_captures_moves = 0  # Moves made without any captures or pawn movements

    while running:
        if no_captures_moves >= 100:  # Draw by fifty-move rule
            draw = True
            break
        
        display_board()
        
        king_pos = get_king_pos(is_white_turn)
        if is_king_in_check(is_white_turn, king_pos):
            all_moves = king_moves(is_white_turn, king_pos)
            if not all_moves: # Checkmate
                winner = "BLACK" if is_white_turn else "WHITE"
                break
        else:
            all_moves = get_all_moves(is_white_turn) + king_moves(is_white_turn, king_pos)
            if not all_moves: # Stalemate
                draw = True
                break
        
        if is_white_turn: # Human plays
            move = get_human_move(all_moves)
        else: # AI players
            move = random.choice(all_moves)
            print("AI plays")
            
        curr_pos, next_pos = move
        piece_moved = board[curr_pos[0]][curr_pos[1]]
        piece_captured = board[next_pos[0]][next_pos[1]]

        no_captures_moves = 0 if piece_captured != "." or piece_moved.lower() == "p" else no_captures_moves + 1

        running = make_move(curr_pos, next_pos)
        is_white_turn = not is_white_turn

    display_board()

    if draw:
        print("Draw")
    else:
        if winner is None:
            winner = "BLACK" if is_white_turn else "WHITE"
        print(f"\n\n{winner} wins")

    return None

game()