import game_states_and_settings as gss
from basic_functions import *
import check_tests as ct

########################################################################################################################
########################################################################################################################
# functions to get moves

########################################################################################################################
# get moves depending on piece type


def get_moves_king(to_be_moved) -> list:
    moves = []
    start_square = (to_be_moved.row, to_be_moved.col)
    for r_ in range(to_be_moved.row - 1, to_be_moved.row + 2):
        for c_ in range(to_be_moved.col - 1, to_be_moved.col + 2):
            moving = r_ != to_be_moved.row or c_ != to_be_moved.col
            if moving and on_board(r_, c_):
                if is_empty(r_, c_) or has_enemy_piece(r_, c_, to_be_moved.color):
                    if not ct.check_test(to_be_moved.color, r_, c_):
                        new_move = (start_square, (r_, c_))
                        moves.append(new_move)
    if not gss.giving_check:
        if gss.castling_possible[to_be_moved.color]["00"]:
            if is_empty(to_be_moved.row, to_be_moved.col + 1):
                if is_empty(to_be_moved.row, to_be_moved.col + 2):
                    if not ct.check_test(to_be_moved.color, to_be_moved.row, to_be_moved.col + 1):
                        if not ct.check_test(to_be_moved.color, to_be_moved.row, to_be_moved.col + 2):
                            new_move = (start_square, (to_be_moved.row, to_be_moved.col + 2))
                            moves.append(new_move)
        if gss.castling_possible[to_be_moved.color]["000"]:
            if is_empty(to_be_moved.row, to_be_moved.col - 1):
                if is_empty(to_be_moved.row, to_be_moved.col - 2):
                    if is_empty(to_be_moved.row, to_be_moved.col - 3):
                        if not ct.check_test(to_be_moved.color, to_be_moved.row, to_be_moved.col - 1):
                            if not ct.check_test(to_be_moved.color, to_be_moved.row, to_be_moved.col - 2):
                                if not ct.check_test(to_be_moved.color, to_be_moved.row, to_be_moved.col - 3):
                                    new_move = (start_square, (to_be_moved.row, to_be_moved.col - 2))
                                    moves.append(new_move)
    return moves


def get_moves_queen(to_be_moved) -> list:
    if to_be_moved.pinned_from is not None:
        return get_moves_queen_if_pinned(to_be_moved)
    return get_moves_queen_if_not_pinned(to_be_moved)


def get_moves_rook(to_be_moved) -> list:
    if to_be_moved.pinned_from is not None:
        return get_moves_rook_if_pinned(to_be_moved)
    return get_moves_rook_if_not_pinned(to_be_moved)


def get_moves_knight(to_be_moved) -> list:
    if to_be_moved.pinned_from is not None:
        return []
    return get_moves_knight_if_not_pinned(to_be_moved)


def get_moves_bishop(to_be_moved) -> list:
    if to_be_moved.pinned_from is not None:
        return get_moves_bishop_if_pinned(to_be_moved)
    return get_moves_bishop_if_not_pinned(to_be_moved)


def get_moves_pawn(to_be_moved) -> list:
    if to_be_moved.pinned_from is not None:
        return get_moves_pawn_if_pinned(to_be_moved)
    return get_moves_pawn_if_not_pinned(to_be_moved)


########################################################################################################################
# get moves depending on piece type if pinned


def get_moves_queen_if_pinned(to_be_moved) -> list:
    match to_be_moved.pinned_from:
        case "above":
            return get_moves_if_pinned_from_above(to_be_moved)
        case "right_above":
            return get_moves_if_pinned_from_right_above(to_be_moved)
        case "right":
            return get_moves_if_pinned_from_right(to_be_moved)
        case "right_below":
            return get_moves_if_pinned_from_right_below(to_be_moved)
        case "below":
            return get_moves_if_pinned_from_below(to_be_moved)
        case "left_below":
            return get_moves_if_pinned_from_left_below(to_be_moved)
        case "left":
            return get_moves_if_pinned_from_left(to_be_moved)
        case "left_above":
            return get_moves_if_pinned_from_left_above(to_be_moved)


def get_moves_rook_if_pinned(to_be_moved) -> list:
    match to_be_moved.pinned_from:
        case "above":
            return get_moves_if_pinned_from_above(to_be_moved)
        case "right":
            return get_moves_if_pinned_from_right(to_be_moved)
        case "below":
            return get_moves_if_pinned_from_below(to_be_moved)
        case "left":
            return get_moves_if_pinned_from_left(to_be_moved)
        case _:
            return []


def get_moves_bishop_if_pinned(to_be_moved) -> list:
    match to_be_moved.pinned_from:
        case "right_above":
            return get_moves_if_pinned_from_right_above(to_be_moved)
        case "right_below":
            return get_moves_if_pinned_from_right_below(to_be_moved)
        case "left_below":
            return get_moves_if_pinned_from_left_below(to_be_moved)
        case "left_above":
            return get_moves_if_pinned_from_left_above(to_be_moved)
        case _:
            return []


def get_moves_pawn_if_pinned(to_be_moved) -> list:
    if to_be_moved.color:
        return get_moves_pawn_if_pinned_white(to_be_moved)
    return get_moves_pawn_if_pinned_black(to_be_moved)


def get_moves_pawn_if_pinned_white(to_be_moved) -> list:
    moves = []
    start = (to_be_moved.row, to_be_moved.col)
    match to_be_moved.pinned_from:
        case "above" | "below":
            if is_empty(to_be_moved.row - 1, to_be_moved.col):
                new_move = (start, (to_be_moved.row - 1, to_be_moved.col))
                moves.append(new_move)
                if not to_be_moved.has_moved and is_empty(to_be_moved.row - 2, to_be_moved.col):
                    new_move = (start, (to_be_moved.row - 2, to_be_moved.col))
                    moves.append(new_move)
        case "right_above":
            goal = (to_be_moved.row - 1, to_be_moved.col + 1)
            if (not is_empty(goal[0], goal[1])) or ((start, goal) in gss.possible_en_passant_moves):
                add_pawn_move((start, goal), moves)
        case "left_above":
            goal = (to_be_moved.row - 1, to_be_moved.col - 1)
            if (not is_empty(goal[0], goal[1])) or ((start, goal) in gss.possible_en_passant_moves):
                add_pawn_move((start, goal), moves)
    return moves


def get_moves_pawn_if_pinned_black(to_be_moved) -> list:
    moves = []
    start = (to_be_moved.row, to_be_moved.col)
    match to_be_moved.pinned_from:
        case "above" | "below":
            if is_empty(to_be_moved.row + 1, to_be_moved.col):
                new_move = (start, (to_be_moved.row + 1, to_be_moved.col))
                moves.append(new_move)
                if not to_be_moved.has_moved and is_empty(to_be_moved.row + 2, to_be_moved.col):
                    new_move = (start, (to_be_moved.row + 2, to_be_moved.col))
                    moves.append(new_move)
        case "right_below":
            goal = (to_be_moved.row + 1, to_be_moved.col + 1)
            if (not is_empty(goal[0], goal[1])) or ((start, goal) in gss.possible_en_passant_moves):
                add_pawn_move((start, goal), moves)
        case "left_below":
            goal = (to_be_moved.row + 1, to_be_moved.col - 1)
            if (not is_empty(goal[0], goal[1])) or ((start, goal) in gss.possible_en_passant_moves):
                add_pawn_move((start, goal), moves)
    return moves


def add_pawn_move(new_move: tuple, moves: list):
    if new_move[1][0] == 0 or new_move[1][0] == 7:
        if (not gss.giving_check) or new_move[1] in gss.squares_to_break_check:
            gss.possible_pawn_transformations.append(new_move)
    else:
        moves.append(new_move)


########################################################################################################################
# get general moves if piece is pinned: used for queens, rooks and bishops


def get_moves_if_pinned_from_above(to_be_moved) -> list:
    moves = []
    start_square = (to_be_moved.row, to_be_moved.col)
    r_0 = gss.pinning_candidates[not to_be_moved.color]["above"][0].row
    r_1 = gss.pieces[to_be_moved.color][0].row
    for r_ in range(r_0, r_1):
        if r_ != to_be_moved.row:
            new_move = (start_square, (r_, to_be_moved.col))
            moves.append(new_move)
    return moves


def get_moves_if_pinned_from_right_above(to_be_moved) -> list:
    moves = []
    start_square = (to_be_moved.row, to_be_moved.col)
    r_0 = gss.pinning_candidates[not to_be_moved.color]["right_above"][0].row
    c_ = gss.pinning_candidates[not to_be_moved.color]["right_above"][0].col
    r_1 = gss.pieces[to_be_moved.color][0].row
    for r_ in range(r_0, r_1):
        if r_ != to_be_moved.row:
            new_move = (start_square, (r_, c_))
            moves.append(new_move)
        c_ -= 1
    return moves


def get_moves_if_pinned_from_right(to_be_moved) -> list:
    moves = []
    start_square = (to_be_moved.row, to_be_moved.col)
    c_0 = gss.pieces[to_be_moved.color][0].col + 1
    c_1 = gss.pinning_candidates[not to_be_moved.color]["right"][0].col + 1
    for c_ in range(c_0, c_1):
        if c_ != to_be_moved.col:
            new_move = (start_square, (to_be_moved.row, c_))
            moves.append(new_move)
    return moves


def get_moves_if_pinned_from_right_below(to_be_moved) -> list:
    moves = []
    start_square = (to_be_moved.row, to_be_moved.col)
    r_0 = gss.pieces[to_be_moved.color][0].row + 1
    c_ = gss.pieces[to_be_moved.color][0].col + 1
    r_1 = gss.pinning_candidates[not to_be_moved.color]["right_below"][0].row + 1
    for r_ in range(r_0, r_1):
        if r_ != to_be_moved.row:
            new_move = (start_square, (r_, c_))
            moves.append(new_move)
        c_ += 1
    return moves


def get_moves_if_pinned_from_below(to_be_moved) -> list:
    moves = []
    start_square = (to_be_moved.row, to_be_moved.col)
    r_0 = gss.pieces[to_be_moved.color][0].row + 1
    r_1 = gss.pinning_candidates[not to_be_moved.color]["below"][0].row + 1
    for r_ in range(r_0, r_1):
        if r_ != to_be_moved.row:
            new_move = (start_square, (r_, to_be_moved.col))
            moves.append(new_move)
    return moves


def get_moves_if_pinned_from_left_below(to_be_moved) -> list:
    moves = []
    start_square = (to_be_moved.row, to_be_moved.col)
    r_0 = gss.pieces[to_be_moved.color][0].row + 1
    c_ = gss.pieces[to_be_moved.color][0].col - 1
    r_1 = gss.pinning_candidates[not to_be_moved.color]["left_below"][0].row + 1
    for r_ in range(r_0, r_1):
        if r_ != to_be_moved.row:
            new_move = (start_square, (r_, c_))
            moves.append(new_move)
        c_ -= 1
    return moves


def get_moves_if_pinned_from_left(to_be_moved) -> list:
    moves = []
    start_square = (to_be_moved.row, to_be_moved.col)
    c_0 = gss.pinning_candidates[not to_be_moved.color]["left"][0].col
    c_1 = gss.pieces[to_be_moved.color][0].col
    for c_ in range(c_0, c_1):
        if c_ != to_be_moved.col:
            new_move = (start_square, (to_be_moved.row, c_))
            moves.append(new_move)
    return moves


def get_moves_if_pinned_from_left_above(to_be_moved) -> list:
    moves = []
    start_square = (to_be_moved.row, to_be_moved.col)
    r_0 = gss.pinning_candidates[not to_be_moved.color]["left_above"][0].row
    c_ = gss.pinning_candidates[not to_be_moved.color]["left_above"][0].col
    r_1 = gss.pieces[to_be_moved.color][0].row
    for r_ in range(r_0, r_1):
        if r_ != to_be_moved.row:
            new_move = (start_square, (r_, c_))
            moves.append(new_move)
        c_ += 1
    return moves


########################################################################################################################
# get moves depending on piece type if not pinned


def get_moves_queen_if_not_pinned(to_be_moved) -> list:
    moves = get_moves_if_not_pinned_row_left(to_be_moved)
    moves += get_moves_if_not_pinned_row_right(to_be_moved)
    moves += get_moves_if_not_pinned_col_above(to_be_moved)
    moves += get_moves_if_not_pinned_col_below(to_be_moved)
    moves += get_moves_if_not_pinned_up_left(to_be_moved)
    moves += get_moves_if_not_pinned_up_right(to_be_moved)
    moves += get_moves_if_not_pinned_down_left(to_be_moved)
    moves += get_moves_if_not_pinned_down_right(to_be_moved)
    return moves


def get_moves_rook_if_not_pinned(to_be_moved) -> list:
    moves = get_moves_if_not_pinned_row_left(to_be_moved)
    moves += get_moves_if_not_pinned_row_right(to_be_moved)
    moves += get_moves_if_not_pinned_col_above(to_be_moved)
    moves += get_moves_if_not_pinned_col_below(to_be_moved)
    return moves


def get_moves_knight_if_not_pinned(to_be_moved) -> list:
    moves = []
    start_square = (to_be_moved.row, to_be_moved.col)
    for r_ in [to_be_moved.row - 1, to_be_moved.row + 1]:
        for c_ in [to_be_moved.col - 2, to_be_moved.col + 2]:
            if on_board(r_, c_) and (is_empty(r_, c_) or has_enemy_piece(r_, c_, to_be_moved.color)):
                moves.append((start_square, (r_, c_)))
    for r_ in [to_be_moved.row - 2, to_be_moved.row + 2]:
        for c_ in [to_be_moved.col - 1, to_be_moved.col + 1]:
            if on_board(r_, c_) and (is_empty(r_, c_) or has_enemy_piece(r_, c_, to_be_moved.color)):
                moves.append((start_square, (r_, c_)))
    return moves


def get_moves_bishop_if_not_pinned(to_be_moved) -> list:
    moves = get_moves_if_not_pinned_up_left(to_be_moved)
    moves += get_moves_if_not_pinned_up_right(to_be_moved)
    moves += get_moves_if_not_pinned_down_left(to_be_moved)
    moves += get_moves_if_not_pinned_down_right(to_be_moved)
    return moves


def get_moves_pawn_if_not_pinned(to_be_moved) -> list:
    if to_be_moved.color:
        return get_moves_pawn_if_not_pinned_white(to_be_moved)
    return get_moves_pawn_if_not_pinned_black(to_be_moved)


def get_moves_pawn_if_not_pinned_white(to_be_moved) -> list:
    moves = []
    start = (to_be_moved.row, to_be_moved.col)
    goal = (to_be_moved.row - 1, to_be_moved.col)
    if is_empty(goal[0], goal[1]):
        add_pawn_move((start, goal), moves)
        if not to_be_moved.has_moved:
            goal = (to_be_moved.row - 2, to_be_moved.col)
            if is_empty(goal[0], goal[1]):
                moves.append((start, goal))
    for c_ in [to_be_moved.col - 1, to_be_moved.col + 1]:
        goal = (to_be_moved.row - 1, c_)
        if on_board(goal[0], goal[1]):
            direct_capture = not is_empty(goal[0], goal[1]) and has_enemy_piece(goal[0], goal[1], True)
            en_passant = (start, goal) in gss.possible_en_passant_moves
            if direct_capture or en_passant:
                add_pawn_move((start, goal), moves)
    return moves


def get_moves_pawn_if_not_pinned_black(to_be_moved) -> list:
    moves = []
    start = (to_be_moved.row, to_be_moved.col)
    goal = (to_be_moved.row + 1, to_be_moved.col)
    if is_empty(goal[0], goal[1]):
        add_pawn_move((start, goal), moves)
        if not to_be_moved.has_moved:
            goal = (to_be_moved.row + 2, to_be_moved.col)
            if is_empty(goal[0], goal[1]):
                moves.append((start, goal))
    for c_ in [to_be_moved.col - 1, to_be_moved.col + 1]:
        goal = (to_be_moved.row + 1, c_)
        if on_board(goal[0], goal[1]):
            direct_capture = not is_empty(goal[0], goal[1]) and has_enemy_piece(goal[0], goal[1], False)
            en_passant = (start, goal) in gss.possible_en_passant_moves
            if direct_capture or en_passant:
                add_pawn_move((start, goal), moves)
    return moves


########################################################################################################################
# get general moves if piece is not pinned: used for queens, rooks and bishops


def get_moves_if_not_pinned_row_left(to_be_moved) -> list:
    moves = []
    start_square = (to_be_moved.row, to_be_moved.col)
    for c_ in range(to_be_moved.col - 1, -1, -1):
        goal = (to_be_moved.row, c_)
        if is_empty(goal[0], goal[1]):
            new_move = (start_square, goal)
            moves.append(new_move)
        elif has_enemy_piece(goal[0], goal[1], to_be_moved.color):
            new_move = (start_square, goal)
            moves.append(new_move)
            break
        else:
            break
    return moves


def get_moves_if_not_pinned_row_right(to_be_moved) -> list:
    moves = []
    start_square = (to_be_moved.row, to_be_moved.col)
    for c_ in range(to_be_moved.col + 1, 8):
        goal = (to_be_moved.row, c_)
        if is_empty(goal[0], goal[1]):
            new_move = (start_square, goal)
            moves.append(new_move)
        elif has_enemy_piece(goal[0], goal[1], to_be_moved.color):
            new_move = (start_square, goal)
            moves.append(new_move)
            break
        else:
            break
    return moves


def get_moves_if_not_pinned_col_above(to_be_moved) -> list:
    moves = []
    start_square = (to_be_moved.row, to_be_moved.col)
    for r_ in range(to_be_moved.row - 1, -1, -1):
        goal = (r_, to_be_moved.col)
        if is_empty(goal[0], goal[1]):
            new_move = (start_square, goal)
            moves.append(new_move)
        elif has_enemy_piece(goal[0], goal[1], to_be_moved.color):
            new_move = (start_square, goal)
            moves.append(new_move)
            break
        else:
            break
    return moves


def get_moves_if_not_pinned_col_below(to_be_moved) -> list:
    moves = []
    start_square = (to_be_moved.row, to_be_moved.col)
    for r_ in range(to_be_moved.row + 1, 8):
        goal = (r_, to_be_moved.col)
        if is_empty(goal[0], goal[1]):
            new_move = (start_square, goal)
            moves.append(new_move)
        elif has_enemy_piece(goal[0], goal[1], to_be_moved.color):
            new_move = (start_square, goal)
            moves.append(new_move)
            break
        else:
            break
    return moves


def get_moves_if_not_pinned_up_left(to_be_moved) -> list:
    moves = []
    start_square = (to_be_moved.row, to_be_moved.col)
    r_ = to_be_moved.row + 1
    c_ = to_be_moved.col - 1
    while on_board(r_, c_):
        if is_empty(r_, c_):
            new_move = (start_square, (r_, c_))
            moves.append(new_move)
            r_ += 1
            c_ -= 1
        elif has_enemy_piece(r_, c_, to_be_moved.color):
            new_move = (start_square, (r_, c_))
            moves.append(new_move)
            break
        else:
            break
    return moves


def get_moves_if_not_pinned_up_right(to_be_moved) -> list:
    moves = []
    start_square = (to_be_moved.row, to_be_moved.col)
    r_ = to_be_moved.row - 1
    c_ = to_be_moved.col + 1
    while on_board(r_, c_):
        if is_empty(r_, c_):
            new_move = (start_square, (r_, c_))
            moves.append(new_move)
            r_ -= 1
            c_ += 1
        elif has_enemy_piece(r_, c_, to_be_moved.color):
            new_move = (start_square, (r_, c_))
            moves.append(new_move)
            break
        else:
            break
    return moves


def get_moves_if_not_pinned_down_left(to_be_moved) -> list:
    moves = []
    start_square = (to_be_moved.row, to_be_moved.col)
    r_ = to_be_moved.row - 1
    c_ = to_be_moved.col - 1
    while on_board(r_, c_):
        if is_empty(r_, c_):
            new_move = (start_square, (r_, c_))
            moves.append(new_move)
            r_ -= 1
            c_ -= 1
        elif has_enemy_piece(r_, c_, to_be_moved.color):
            new_move = (start_square, (r_, c_))
            moves.append(new_move)
            break
        else:
            break
    return moves


def get_moves_if_not_pinned_down_right(to_be_moved) -> list:
    moves = []
    start_square = (to_be_moved.row, to_be_moved.col)
    r_ = to_be_moved.row + 1
    c_ = to_be_moved.col + 1
    while on_board(r_, c_):
        if is_empty(r_, c_):
            new_move = (start_square, (r_, c_))
            moves.append(new_move)
            r_ += 1
            c_ += 1
        elif has_enemy_piece(r_, c_, to_be_moved.color):
            new_move = (start_square, (r_, c_))
            moves.append(new_move)
            break
        else:
            break
    return moves
