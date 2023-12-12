"""
Motivation: Can a CNN model find a pattern in a set of seemingly random moves?
If it can, how much data is needed to achieve this for a problem
of 8x8 complexity.

Problem Statement: Train a cnn model to learn how to make valid moves
in chess. It's ok if the moves are random; ie. the model does not employ
any strategy.

Notes:
1. ONE DATA POINT IS A MATRIX OF SIZE 8 BY 8
2. LABEL IS A ONE-DIMENSIONAL MATRIX OF 4 ELEMENTS DEPICTING THE MOVE OF A PIECE. 
THE RANGE OF EACH ELEMENT IS [0, 7]. EG. [1, 1, 3, 1]
3. FOR THE ATTACKING PLAYER:
    PAWNS: 1
    ROOKS: 2
    KNIGHTS: 3
    BISHOPS: 4
    QUEEN: 5
    KING: 7
4. FOR THE DEFENDING PLAYER:
    PAWNS: 15
    ROOKS: 16
    KNIGHTS: 17
    BISHOPS: 18
    QUEEN: 19
    KING: 21
5. EMPTY SPACE IS 0.

Conclusion:
CNN model wasn't able to successfully learn to make valid moves. 

Extension:
Use an appropriate learning model to solve the problem.
"""

import random
import pickle
import numpy as np

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

transformer = {
    # Transforms board characters to numerical equivalents
    # for training
    "p": 1, "P": 15,
    "r": 2, "R": 16,
    "n": 3, "N": 17,
    "b": 4, "B": 18,
    "q": 5, "Q": 19,
    "k": 7, "K": 21,
    ".": 0
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
    
  
def labeler(move, is_white_turn):
    """Turns the move of a player into a label
    Takes a list of tuples of integers and returns a 1*4 numpy array
    """
    curr_pos, next_pos = move
    label = list(curr_pos + next_pos)
    
    if not is_white_turn:
        label = [7-ele for ele in label]
        
    return label

def get_data_point(is_white_turn):
    """Transforms the current state of the board into number
    representatives to allow for training.
    Takes nothing and returns an 8*8 numpy array
    """
    data = []
    if is_white_turn:
        for i in range(8):
            data.append([transformer[ele] for ele in board[i]])
    else:
        for i in range(8):
            data.append(list(reversed([transformer[ele.upper()] if ele.islower() else transformer[ele.lower()] for ele in board[i]])))
        data.reverse()
    
    data = np.array(data)
    return data


# Main game loop
def game(): 
    is_white_turn = True  # White starts
    running, draw = True, False
    winner = None
    no_captures_moves = 0  # Moves made without any captures or pawn movements
    size = 0 # Size of data collected

    while running:
        if no_captures_moves >= 100:  # Draw by fifty-move rule
            draw = True
            break

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
        
        for pos_move in all_moves:
            # Collect new data point into pickle file
            with open('training_data/X.pkl', 'ab') as f:  # 'ab' mode for appending in binary mode
                pickle.dump(get_data_point(is_white_turn), f)
                
            # Collect new label into pickle file
            with open('training_data/Y.pkl', 'ab') as f:  # 'ab' mode for appending in binary mode
                pickle.dump(labeler(pos_move, is_white_turn), f)
                
            size += 1 # Increase of size of collected data by 1
            
        print("WHITE plays" if is_white_turn else "BLACK plays")
        
        move = random.choice(all_moves)
        curr_pos, next_pos = move
        piece_moved = board[curr_pos[0]][curr_pos[1]]
        piece_captured = board[next_pos[0]][next_pos[1]]
        
        no_captures_moves = 0 if piece_captured != "." or piece_moved.lower() == "p" else no_captures_moves + 1

        running = make_move(curr_pos, next_pos)
        is_white_turn = not is_white_turn
        print(curr_pos, next_pos)

    display_board()

    if draw:
        print("Draw")
    else:
        if winner is None:
            winner = "BLACK" if is_white_turn else "WHITE"
        print(f"\n\n{winner} wins")

    print("SIZE OF DATA: ", size)
    return None


game()