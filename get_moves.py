import game_states_and_settings as gss
import check_tests as ct
from board import on_board, is_empty, has_enemy_piece

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
                empty_square = is_empty(r_, c_)
                if empty_square or has_enemy_piece(r_, c_, to_be_moved.color):
                    if not ct.check_test(to_be_moved.color, r_, c_):
                        new_move = (start_square, (r_, c_))
                        moves.append(new_move)
                        if empty_square:
                            gss.move_to_notation[new_move] = ["K" + gss.file[c_] + gss.rank[r_]]
                        else:
                            gss.move_to_notation[new_move] = ["Kx" + gss.file[c_] + gss.rank[r_]]
    if not gss.giving_check:
        if gss.castling_possible[to_be_moved.color]["00"]:
            if is_empty(to_be_moved.row, to_be_moved.col + 1):
                if is_empty(to_be_moved.row, to_be_moved.col + 2):
                    if not ct.check_test(to_be_moved.color, to_be_moved.row, to_be_moved.col + 1):
                        if not ct.check_test(to_be_moved.color, to_be_moved.row, to_be_moved.col + 2):
                            new_move = (start_square, (to_be_moved.row, to_be_moved.col + 2))
                            moves.append(new_move)
                            gss.move_to_notation[new_move] = ["0-0"]
        if gss.castling_possible[to_be_moved.color]["000"]:
            if is_empty(to_be_moved.row, to_be_moved.col - 1):
                if is_empty(to_be_moved.row, to_be_moved.col - 2):
                    if is_empty(to_be_moved.row, to_be_moved.col - 3):
                        if not ct.check_test(to_be_moved.color, to_be_moved.row, to_be_moved.col - 1):
                            if not ct.check_test(to_be_moved.color, to_be_moved.row, to_be_moved.col - 2):
                                if not ct.check_test(to_be_moved.color, to_be_moved.row, to_be_moved.col - 3):
                                    new_move = (start_square, (to_be_moved.row, to_be_moved.col - 2))
                                    moves.append(new_move)
                                    gss.move_to_notation[new_move] = ["0-0-0"]
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
            return get_moves_if_pinned_from_above(to_be_moved, "Q")
        case "right_above":
            return get_moves_if_pinned_from_right_above(to_be_moved, "Q")
        case "right":
            return get_moves_if_pinned_from_right(to_be_moved, "Q")
        case "right_below":
            return get_moves_if_pinned_from_right_below(to_be_moved, "Q")
        case "below":
            return get_moves_if_pinned_from_below(to_be_moved, "Q")
        case "left_below":
            return get_moves_if_pinned_from_left_below(to_be_moved, "Q")
        case "left":
            return get_moves_if_pinned_from_left(to_be_moved, "Q")
        case "left_above":
            return get_moves_if_pinned_from_left_above(to_be_moved, "Q")


def get_moves_rook_if_pinned(to_be_moved) -> list:
    match to_be_moved.pinned_from:
        case "above":
            return get_moves_if_pinned_from_above(to_be_moved, "R")
        case "right":
            return get_moves_if_pinned_from_right(to_be_moved, "R")
        case "below":
            return get_moves_if_pinned_from_below(to_be_moved, "R")
        case "left":
            return get_moves_if_pinned_from_left(to_be_moved, "R")
        case _:
            return []


def get_moves_bishop_if_pinned(to_be_moved) -> list:
    match to_be_moved.pinned_from:
        case "right_above":
            return get_moves_if_pinned_from_right_above(to_be_moved, "B")
        case "right_below":
            return get_moves_if_pinned_from_right_below(to_be_moved, "B")
        case "left_below":
            return get_moves_if_pinned_from_left_below(to_be_moved, "B")
        case "left_above":
            return get_moves_if_pinned_from_left_above(to_be_moved, "B")
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
                goal = (to_be_moved.row - 1, to_be_moved.col)
                add_new_pawn_move(start, goal, moves)
                if not to_be_moved.has_moved and is_empty(to_be_moved.row - 2, to_be_moved.col):
                    goal = (to_be_moved.row - 2, to_be_moved.col)
                    add_new_pawn_move(start, goal, moves)
        case "right_above":
            goal = (to_be_moved.row - 1, to_be_moved.col + 1)
            if (not is_empty(goal[0], goal[1])) or ((start, goal) in gss.possible_en_passant_moves):
                add_new_pawn_move_if_transformation_is_possible(start, goal, moves)
        case "left_above":
            goal = (to_be_moved.row - 1, to_be_moved.col - 1)
            if (not is_empty(goal[0], goal[1])) or ((start, goal) in gss.possible_en_passant_moves):
                add_new_pawn_move_if_transformation_is_possible(start, goal, moves)
    return moves


def get_moves_pawn_if_pinned_black(to_be_moved) -> list:
    moves = []
    start = (to_be_moved.row, to_be_moved.col)
    match to_be_moved.pinned_from:
        case "above" | "below":
            if is_empty(to_be_moved.row + 1, to_be_moved.col):
                goal = (to_be_moved.row + 1, to_be_moved.col)
                add_new_pawn_move(start, goal, moves)
                if not to_be_moved.has_moved and is_empty(to_be_moved.row + 2, to_be_moved.col):
                    goal = (to_be_moved.row + 2, to_be_moved.col)
                    add_new_pawn_move(start, goal, moves)
        case "right_below":
            goal = (to_be_moved.row + 1, to_be_moved.col + 1)
            if (not is_empty(goal[0], goal[1])) or ((start, goal) in gss.possible_en_passant_moves):
                add_new_pawn_move_if_transformation_is_possible(start, goal, moves)
        case "left_below":
            goal = (to_be_moved.row + 1, to_be_moved.col - 1)
            if (not is_empty(goal[0], goal[1])) or ((start, goal) in gss.possible_en_passant_moves):
                add_new_pawn_move_if_transformation_is_possible(start, goal, moves)
    return moves


########################################################################################################################
# get general moves if piece is pinned: used for queens, rooks and bishops


def get_moves_if_pinned_from_above(to_be_moved, piece_type_initial) -> list:
    moves = []
    start = (to_be_moved.row, to_be_moved.col)
    r_0 = gss.pinning_candidates[not to_be_moved.color]["above"][0].row
    r_1 = gss.pieces[to_be_moved.color][0].row
    for r_ in range(r_0, r_1):
        if r_ != to_be_moved.row:
            goal = (r_, to_be_moved.col)
            add_new_move(start, goal, moves, piece_type_initial)
    return moves


def get_moves_if_pinned_from_right_above(to_be_moved, piece_type_initial) -> list:
    moves = []
    start = (to_be_moved.row, to_be_moved.col)
    r_0 = gss.pinning_candidates[not to_be_moved.color]["right_above"][0].row
    c_ = gss.pinning_candidates[not to_be_moved.color]["right_above"][0].col
    r_1 = gss.pieces[to_be_moved.color][0].row
    for r_ in range(r_0, r_1):
        if r_ != to_be_moved.row:
            goal = (r_, c_)
            add_new_move(start, goal, moves, piece_type_initial)
        c_ -= 1
    return moves


def get_moves_if_pinned_from_right(to_be_moved, piece_type_initial) -> list:
    moves = []
    start = (to_be_moved.row, to_be_moved.col)
    c_0 = gss.pieces[to_be_moved.color][0].col + 1
    c_1 = gss.pinning_candidates[not to_be_moved.color]["right"][0].col + 1
    for c_ in range(c_0, c_1):
        if c_ != to_be_moved.col:
            goal = (to_be_moved.row, c_)
            add_new_move(start, goal, moves, piece_type_initial)
    return moves


def get_moves_if_pinned_from_right_below(to_be_moved, piece_type_initial) -> list:
    moves = []
    start = (to_be_moved.row, to_be_moved.col)
    r_0 = gss.pieces[to_be_moved.color][0].row + 1
    c_ = gss.pieces[to_be_moved.color][0].col + 1
    r_1 = gss.pinning_candidates[not to_be_moved.color]["right_below"][0].row + 1
    for r_ in range(r_0, r_1):
        if r_ != to_be_moved.row:
            goal = (r_, c_)
            add_new_move(start, goal, moves, piece_type_initial)
        c_ += 1
    return moves


def get_moves_if_pinned_from_below(to_be_moved, piece_type_initial) -> list:
    moves = []
    start = (to_be_moved.row, to_be_moved.col)
    r_0 = gss.pieces[to_be_moved.color][0].row + 1
    r_1 = gss.pinning_candidates[not to_be_moved.color]["below"][0].row + 1
    for r_ in range(r_0, r_1):
        if r_ != to_be_moved.row:
            goal = (r_, to_be_moved.col)
            add_new_move(start, goal, moves, piece_type_initial)
    return moves


def get_moves_if_pinned_from_left_below(to_be_moved, piece_type_initial) -> list:
    moves = []
    start = (to_be_moved.row, to_be_moved.col)
    r_0 = gss.pieces[to_be_moved.color][0].row + 1
    c_ = gss.pieces[to_be_moved.color][0].col - 1
    r_1 = gss.pinning_candidates[not to_be_moved.color]["left_below"][0].row + 1
    for r_ in range(r_0, r_1):
        if r_ != to_be_moved.row:
            goal = (r_, c_)
            add_new_move(start, goal, moves, piece_type_initial)
        c_ -= 1
    return moves


def get_moves_if_pinned_from_left(to_be_moved, piece_type_initial) -> list:
    moves = []
    start = (to_be_moved.row, to_be_moved.col)
    c_0 = gss.pinning_candidates[not to_be_moved.color]["left"][0].col
    c_1 = gss.pieces[to_be_moved.color][0].col
    for c_ in range(c_0, c_1):
        if c_ != to_be_moved.col:
            goal = (to_be_moved.row, c_)
            add_new_move(start, goal, moves, piece_type_initial)
    return moves


def get_moves_if_pinned_from_left_above(to_be_moved, piece_type_initial) -> list:
    moves = []
    start = (to_be_moved.row, to_be_moved.col)
    r_0 = gss.pinning_candidates[not to_be_moved.color]["left_above"][0].row
    c_ = gss.pinning_candidates[not to_be_moved.color]["left_above"][0].col
    r_1 = gss.pieces[to_be_moved.color][0].row
    for r_ in range(r_0, r_1):
        if r_ != to_be_moved.row:
            goal = (r_, c_)
            add_new_move(start, goal, moves, piece_type_initial)
        c_ += 1
    return moves


########################################################################################################################
# get moves depending on piece type if not pinned


def get_moves_queen_if_not_pinned(to_be_moved) -> list:
    moves = get_moves_if_not_pinned_row_left(to_be_moved, "Q")
    moves += get_moves_if_not_pinned_row_right(to_be_moved, "Q")
    moves += get_moves_if_not_pinned_col_above(to_be_moved, "Q")
    moves += get_moves_if_not_pinned_col_below(to_be_moved, "Q")
    moves += get_moves_if_not_pinned_up_left(to_be_moved, "Q")
    moves += get_moves_if_not_pinned_up_right(to_be_moved, "Q")
    moves += get_moves_if_not_pinned_down_left(to_be_moved, "Q")
    moves += get_moves_if_not_pinned_down_right(to_be_moved, "Q")
    return moves


def get_moves_rook_if_not_pinned(to_be_moved) -> list:
    moves = get_moves_if_not_pinned_row_left(to_be_moved, "R")
    moves += get_moves_if_not_pinned_row_right(to_be_moved, "R")
    moves += get_moves_if_not_pinned_col_above(to_be_moved, "R")
    moves += get_moves_if_not_pinned_col_below(to_be_moved, "R")
    return moves


def get_moves_knight_if_not_pinned(to_be_moved) -> list:
    moves = []
    start = (to_be_moved.row, to_be_moved.col)
    for r_ in [to_be_moved.row - 1, to_be_moved.row + 1]:
        for c_ in [to_be_moved.col - 2, to_be_moved.col + 2]:
            if on_board(r_, c_) and (is_empty(r_, c_) or has_enemy_piece(r_, c_, to_be_moved.color)):
                add_new_move(start, (r_, c_), moves, "N")
    for r_ in [to_be_moved.row - 2, to_be_moved.row + 2]:
        for c_ in [to_be_moved.col - 1, to_be_moved.col + 1]:
            if on_board(r_, c_) and (is_empty(r_, c_) or has_enemy_piece(r_, c_, to_be_moved.color)):
                add_new_move(start, (r_, c_), moves, "N")
    return moves


def get_moves_bishop_if_not_pinned(to_be_moved) -> list:
    moves = get_moves_if_not_pinned_up_left(to_be_moved, "B")
    moves += get_moves_if_not_pinned_up_right(to_be_moved, "B")
    moves += get_moves_if_not_pinned_down_left(to_be_moved, "B")
    moves += get_moves_if_not_pinned_down_right(to_be_moved, "B")
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
        add_new_pawn_move_if_transformation_is_possible(start, goal, moves)
        if not to_be_moved.has_moved:
            goal = (to_be_moved.row - 2, to_be_moved.col)
            if is_empty(goal[0], goal[1]):
                add_new_pawn_move(start, goal, moves)
    for c_ in [to_be_moved.col - 1, to_be_moved.col + 1]:
        goal = (to_be_moved.row - 1, c_)
        if on_board(goal[0], goal[1]):
            direct_capture = not is_empty(goal[0], goal[1]) and has_enemy_piece(goal[0], goal[1], True)
            en_passant = (start, goal) in gss.possible_en_passant_moves
            if direct_capture or en_passant:
                add_new_pawn_move_if_transformation_is_possible(start, goal, moves)
    return moves


def get_moves_pawn_if_not_pinned_black(to_be_moved) -> list:
    moves = []
    start = (to_be_moved.row, to_be_moved.col)
    goal = (to_be_moved.row + 1, to_be_moved.col)
    if is_empty(goal[0], goal[1]):
        add_new_pawn_move_if_transformation_is_possible(start, goal, moves)
        if not to_be_moved.has_moved:
            goal = (to_be_moved.row + 2, to_be_moved.col)
            if is_empty(goal[0], goal[1]):
                add_new_pawn_move(start, goal, moves)
    for c_ in [to_be_moved.col - 1, to_be_moved.col + 1]:
        goal = (to_be_moved.row + 1, c_)
        if on_board(goal[0], goal[1]):
            direct_capture = not is_empty(goal[0], goal[1]) and has_enemy_piece(goal[0], goal[1], False)
            en_passant = (start, goal) in gss.possible_en_passant_moves
            if direct_capture or en_passant:
                add_new_pawn_move_if_transformation_is_possible(start, goal, moves)
    return moves


########################################################################################################################
# get general moves if piece is not pinned: used for queens, rooks and bishops


def get_moves_if_not_pinned_row_left(to_be_moved, piece_type_initial) -> list:
    moves = []
    start = (to_be_moved.row, to_be_moved.col)
    for c_ in range(to_be_moved.col - 1, -1, -1):
        goal = (to_be_moved.row, c_)
        if is_empty(goal[0], goal[1]):
            add_new_move(start, goal, moves, piece_type_initial)
        elif has_enemy_piece(goal[0], goal[1], to_be_moved.color):
            add_new_move(start, goal, moves, piece_type_initial)
            break
        else:
            break
    return moves


def get_moves_if_not_pinned_row_right(to_be_moved, piece_type_initial) -> list:
    moves = []
    start = (to_be_moved.row, to_be_moved.col)
    for c_ in range(to_be_moved.col + 1, 8):
        goal = (to_be_moved.row, c_)
        if is_empty(goal[0], goal[1]):
            add_new_move(start, goal, moves, piece_type_initial)
        elif has_enemy_piece(goal[0], goal[1], to_be_moved.color):
            add_new_move(start, goal, moves, piece_type_initial)
            break
        else:
            break
    return moves


def get_moves_if_not_pinned_col_above(to_be_moved, piece_type_initial) -> list:
    moves = []
    start = (to_be_moved.row, to_be_moved.col)
    for r_ in range(to_be_moved.row - 1, -1, -1):
        goal = (r_, to_be_moved.col)
        if is_empty(goal[0], goal[1]):
            add_new_move(start, goal, moves, piece_type_initial)
        elif has_enemy_piece(goal[0], goal[1], to_be_moved.color):
            add_new_move(start, goal, moves, piece_type_initial)
            break
        else:
            break
    return moves


def get_moves_if_not_pinned_col_below(to_be_moved, piece_type_initial) -> list:
    moves = []
    start = (to_be_moved.row, to_be_moved.col)
    for r_ in range(to_be_moved.row + 1, 8):
        goal = (r_, to_be_moved.col)
        if is_empty(goal[0], goal[1]):
            add_new_move(start, goal, moves, piece_type_initial)
        elif has_enemy_piece(goal[0], goal[1], to_be_moved.color):
            add_new_move(start, goal, moves, piece_type_initial)
            break
        else:
            break
    return moves


def get_moves_if_not_pinned_up_left(to_be_moved, piece_type_initial) -> list:
    moves = []
    start = (to_be_moved.row, to_be_moved.col)
    r_ = to_be_moved.row + 1
    c_ = to_be_moved.col - 1
    while on_board(r_, c_):
        if is_empty(r_, c_):
            add_new_move(start, (r_, c_), moves, piece_type_initial)
            r_ += 1
            c_ -= 1
        elif has_enemy_piece(r_, c_, to_be_moved.color):
            add_new_move(start, (r_, c_), moves, piece_type_initial)
            break
        else:
            break
    return moves


def get_moves_if_not_pinned_up_right(to_be_moved, piece_type_initial) -> list:
    moves = []
    start = (to_be_moved.row, to_be_moved.col)
    r_ = to_be_moved.row - 1
    c_ = to_be_moved.col + 1
    while on_board(r_, c_):
        if is_empty(r_, c_):
            add_new_move(start, (r_, c_), moves, piece_type_initial)
            r_ -= 1
            c_ += 1
        elif has_enemy_piece(r_, c_, to_be_moved.color):
            add_new_move(start, (r_, c_), moves, piece_type_initial)
            break
        else:
            break
    return moves


def get_moves_if_not_pinned_down_left(to_be_moved, piece_type_initial) -> list:
    moves = []
    start = (to_be_moved.row, to_be_moved.col)
    r_ = to_be_moved.row - 1
    c_ = to_be_moved.col - 1
    while on_board(r_, c_):
        if is_empty(r_, c_):
            add_new_move(start, (r_, c_), moves, piece_type_initial)
            r_ -= 1
            c_ -= 1
        elif has_enemy_piece(r_, c_, to_be_moved.color):
            add_new_move(start, (r_, c_), moves, piece_type_initial)
            break
        else:
            break
    return moves


def get_moves_if_not_pinned_down_right(to_be_moved, piece_type_initial) -> list:
    moves = []
    start = (to_be_moved.row, to_be_moved.col)
    r_ = to_be_moved.row + 1
    c_ = to_be_moved.col + 1
    while on_board(r_, c_):
        if is_empty(r_, c_):
            add_new_move(start, (r_, c_), moves, piece_type_initial)
            r_ += 1
            c_ += 1
        elif has_enemy_piece(r_, c_, to_be_moved.color):
            add_new_move(start, (r_, c_), moves, piece_type_initial)
            break
        else:
            break
    return moves


########################################################################################################################
# add new move to a given list of moves


def add_new_move(start, goal, moves, piece_type_initial):
    moves.append((start, goal))
    if is_empty(goal[0], goal[1]):
        n_0 = piece_type_initial + gss.file[goal[1]] + gss.rank[goal[0]]
        n_1 = piece_type_initial + gss.file[start[1]] + gss.file[goal[1]] + gss.rank[goal[0]]
        n_2 = piece_type_initial + gss.rank[start[0]] + gss.file[goal[1]] + gss.rank[goal[0]]
        n_3 = piece_type_initial + gss.file[start[1]] + gss.rank[start[0]] + gss.file[goal[1]] + gss.rank[goal[0]]
    else:
        n_0 = piece_type_initial + "x" + gss.file[goal[1]] + gss.rank[goal[0]]
        n_1 = piece_type_initial + gss.file[start[1]] + "x" + gss.file[goal[1]] + gss.rank[goal[0]]
        n_2 = piece_type_initial + gss.rank[start[0]] + "x" + gss.file[goal[1]] + gss.rank[goal[0]]
        n_3 = piece_type_initial + gss.file[start[1]] + gss.rank[start[0]] + "x" + gss.file[goal[1]] + gss.rank[goal[0]]
    notations = [n_0, n_1, n_2, n_3]
    gss.move_to_notation[(start, goal)] = notations
    for n in notations:
        if n in gss.notation_unic:
            gss.notation_unic[n] = False
        else:
            gss.notation_unic[n] = True


def add_new_pawn_move_if_transformation_is_possible(start, goal, moves: list):
    if goal[0] == 0 or goal[0] == 7:
        if (not gss.giving_check) or goal in gss.squares_to_break_check:
            gss.possible_pawn_transformations.append((start, goal))
            update_pawn_notations(start, goal)
    else:
        add_new_pawn_move(start, goal, moves)


def add_new_pawn_move(start, goal, moves):
    moves.append((start, goal))
    update_pawn_notations(start, goal)


def update_pawn_notations(start, goal):
    if start[1] == goal[1]:
        gss.move_to_notation[(start, goal)] = [gss.file[goal[1]] + gss.rank[goal[0]]]
    else:
        gss.move_to_notation[(start, goal)] = [gss.file[start[1]] + "x" + gss.file[goal[1]] + gss.rank[goal[0]]]
