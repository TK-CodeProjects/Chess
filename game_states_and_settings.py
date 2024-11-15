import board
from basic_functions import on_board, is_empty

########################################################################################################################
# settings

white_human = True
black_human = True

########################################################################################################################
# states

whites_turn = True
legal_moves = []
giving_check = False
squares_to_break_check = []
castling_possible = {
    True: {
        "00": True,     # white hasn't lost the right to castle king's side yet
        "000": True     # white hasn't lost the right to castle queen's side yet
    },
    False: {
        "00": True,     # black hasn't lost the right to castle king's side yet
        "000": True     # black hasn't lost the right to castle queen's side yet
    }
}
pieces = {
    True: [],           # white pieces
    False: []           # black pieces
}
pinning_candidates = {
    True: {
        "above": [],
        "right_above": [],
        "right": [],
        "right_below": [],
        "below": [],
        "left_below": [],
        "left": [],
        "left_above": []
    },
    False: {
        "above": [],
        "right_above": [],
        "right": [],
        "right_below": [],
        "below": [],
        "left_below": [],
        "left": [],
        "left_above": []
    }
}
possible_en_passant_moves = []
possible_pawn_transformations = []

########################################################################################################################
# update functions


def update_castling_right(square_where_rook_starts_game: tuple):
    match square_where_rook_starts_game:
        case (0, 0):
            castling_possible[False]["000"] = False
        case (0, 7):
            castling_possible[False]["00"] = False
        case (7, 0):
            castling_possible[True]["000"] = False
        case (7, 7):
            castling_possible[True]["00"] = False


def update_giving_check_and_squares_to_break_check_by_deduction(squares_to_break_deduction_check: list):
    global giving_check
    global squares_to_break_check
    if giving_check:
        squares_to_break_check = []
    else:
        giving_check = True
        squares_to_break_check = squares_to_break_deduction_check


def update_possible_en_passant_moves(start_square: tuple, goal: tuple):
    if start_square[0] == goal[0] - 2:      # black pawn moves to squares
        en_passant_r = goal[0]              # relevant row for enemy pawns
        en_passant_c = goal[1] - 1          # relevant col for enemy pawns
        update_possible_en_passant_moves_black_pawn_moved(en_passant_r, en_passant_c, goal)
        en_passant_c = goal[1] + 1          # relevant col for enemy pawns
        update_possible_en_passant_moves_black_pawn_moved(en_passant_r, en_passant_c, goal)
    elif start_square[0] == goal[0] + 2:    # white pawn moves to squares
        en_passant_r = goal[0]              # relevant row for enemy pawns
        en_passant_c = goal[1] - 1          # relevant col for enemy pawns
        update_possible_en_passant_moves_white_pawn_moved(en_passant_r, en_passant_c, goal)
        en_passant_c = goal[1] + 1          # relevant col for enemy pawns
        update_possible_en_passant_moves_white_pawn_moved(en_passant_r, en_passant_c, goal)


def update_possible_en_passant_moves_black_pawn_moved(en_passant_r: int, en_passant_c: int, goal: tuple):
    if on_board(en_passant_r, en_passant_c) and not is_empty(en_passant_r, en_passant_c):
        en_passant_piece = board.squares[en_passant_r][en_passant_c].piece
        if en_passant_piece.color and en_passant_piece.get_type() == "Pawn":
            possible_en_passant_moves.append(((en_passant_r, en_passant_c), (goal[0] - 1, goal[1])))


def update_possible_en_passant_moves_white_pawn_moved(en_passant_r: int, en_passant_c: int, goal: tuple):
    if on_board(en_passant_r, en_passant_c) and not is_empty(en_passant_r, en_passant_c):
        en_passant_piece = board.squares[en_passant_r][en_passant_c].piece
        if (not en_passant_piece.color) and en_passant_piece.get_type() == "Pawn":
            possible_en_passant_moves.append(((en_passant_r, en_passant_c), (goal[0] + 1, goal[1])))


def new_game():
    global whites_turn
    global legal_moves
    global giving_check
    global squares_to_break_check
    global possible_en_passant_moves
    global possible_pawn_transformations
    whites_turn = True
    reset_legal_moves()
    giving_check = False
    squares_to_break_check = []
    possible_en_passant_moves = []
    possible_pawn_transformations = []
    castling_possible[True]["00"] = True
    castling_possible[True]["000"] = True
    castling_possible[False]["00"] = True
    castling_possible[False]["000"] = True
    for key in pinning_candidates[True]:
        pinning_candidates[True][key] = []
        pinning_candidates[False][key] = []


def reset_legal_moves():
    global legal_moves
    global possible_pawn_transformations
    legal_moves = []
    possible_pawn_transformations = []
    if giving_check:
        legal_moves = pieces[whites_turn][0].get_legal_moves()
        if len(squares_to_break_check) > 0:
            for movable_piece in pieces[whites_turn]:
                for move in movable_piece.get_legal_moves():
                    if move[1] in squares_to_break_check:
                        legal_moves.append(move)
    else:
        for movable_piece in pieces[whites_turn]:
            legal_moves += movable_piece.get_legal_moves()

