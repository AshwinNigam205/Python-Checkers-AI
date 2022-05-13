from copy import deepcopy
import pygame

RED = (255,0,0)
WHITE = (255, 255, 255)

def minimax(position, depth, max_player, game):
    #basically at end of tree or if a player wins, this returns the evaluation of the particular board state and also the particular board for which its returning the evaluation.
    if depth == 0 or position.winner() != None:       
        return position.evaluate(), position            
    
    if max_player:          #the max player is going to be the white pc
        maxEval = float('-inf') #inializes all max nodes as inf
        best_move = None        # stores the best move possible for max
        for move in get_all_moves(position, WHITE, game):
            evaluation = minimax(move, depth-1, False, game)[0] #for every single move, we evaluate it till we reach at end node of minimax tree
            maxEval = max(maxEval, evaluation)   #stores the node with max eval
            if maxEval == evaluation:    #if the eval for the current move is max we store it in the best_move
                best_move = move
        
        return maxEval, best_move
    else:
        minEval = float('inf')
        best_move = None
        for move in get_all_moves(position, RED, game):
            evaluation = minimax(move, depth-1, True, game)[0]
            minEval = min(minEval, evaluation)
            if minEval == evaluation:
                best_move = move
        
        return minEval, best_move


def simulate_move(piece, move, board, game, skip):
    board.move(piece, move[0], move[1])
    if skip:
        board.remove(skip)

    return board


def get_all_moves(board, color, game):
    moves = []
    #loop through all pcs in the board, get all valid moves for that pc
    for piece in board.get_all_pieces(color):
        valid_moves = board.get_valid_moves(piece)
        for move, skip in valid_moves.items():
            draw_moves(game, board, piece)
            temp_board = deepcopy(board) #makes copy of current board to test out a move on it
            temp_piece = temp_board.get_piece(piece.row, piece.col)
            new_board = simulate_move(temp_piece, move, temp_board, game, skip) #will simulate move for the pc and return the state of new board
            moves.append(new_board) #stores all potential board states so that we can choose the best one suited to us
    
    return moves


def draw_moves(game, board, piece):
    valid_moves = board.get_valid_moves(piece)
    board.draw(game.win)
    pygame.draw.circle(game.win, (0,255,0), (piece.x, piece.y), 50, 5)
    game.draw_valid_moves(valid_moves.keys())
    pygame.display.update()
    #pygame.time.delay(100)

