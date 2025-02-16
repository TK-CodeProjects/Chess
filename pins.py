import board
import game_states_and_settings as gss

########################################################################################################################
########################################################################################################################
# functions to update pinning_candidates

########################################################################################################################
# functions to update pinning_candidates depending on piece type


def update_pins_queen(moved_queen, start: tuple, goal: tuple):
    enemy_king = gss.pieces[not moved_queen.color][0]
    remove_queen_from_pinning_candidates(moved_queen, start, goal, enemy_king)
    add_queen_to_pinning_candidates(moved_queen, start, goal, enemy_king)


def update_pins_rook(moved_rook, start: tuple, goal: tuple):
    enemy_king = gss.pieces[not moved_rook.color][0]
    remove_rook_from_pinning_candidates(moved_rook, start, goal, enemy_king)
    add_rook_to_pinning_candidates(moved_rook, start, goal, enemy_king)


def update_pins_bishop(moved_bishop, start: tuple, goal: tuple):
    enemy_king = gss.pieces[not moved_bishop.color][0]
    remove_bishop_from_pinning_candidates(moved_bishop, start, goal, enemy_king)
    add_bishop_to_pinning_candidates(moved_bishop, start, goal, enemy_king)


########################################################################################################################
# functions to remove piece from pinning_candidates depending on piece type


def remove_queen_from_pinning_candidates(moved_queen, start: tuple, goal: tuple, enemy_king):
    if start[0] == enemy_king.row and start[0] != goal[0]:
        remove_piece_from_pinning_candidates_row(moved_queen, start, enemy_king)
    elif start[1] == enemy_king.col and start[1] != goal[1]:
        remove_piece_from_pinning_candidates_col(moved_queen, start, enemy_king)
    else:
        start_up = start[0] + start[1]
        king_up = enemy_king.row + enemy_king.col
        goal_up = goal[0] + goal[1]
        start_down = start[0] - start[1]
        king_down = enemy_king.row - enemy_king.col
        goal_down = goal[0] - goal[1]
        if start_up == king_up and start_up != goal_up:
            remove_piece_from_pinning_candidates_diag_up(moved_queen, start, enemy_king)
        elif start_down == king_down and start_down != goal_down:
            remove_piece_from_pinning_candidates_diag_down(moved_queen, start, enemy_king)


def remove_rook_from_pinning_candidates(moved_rook, start: tuple, goal: tuple, enemy_king):
    if start[0] == enemy_king.row and start[0] != goal[0]:
        remove_piece_from_pinning_candidates_row(moved_rook, start, enemy_king)
    elif start[1] == enemy_king.col and start[1] != goal[1]:
        remove_piece_from_pinning_candidates_col(moved_rook, start, enemy_king)


def remove_bishop_from_pinning_candidates(moved_bishop, start: tuple, goal: tuple, enemy_king):
    start_square_up = start[0] + start[1]
    king_up = enemy_king.row + enemy_king.col
    goal_up = goal[0] + goal[1]
    start_square_down = start[0] - start[1]
    king_down = enemy_king.row - enemy_king.col
    goal_down = goal[0] - goal[1]
    if start_square_up == king_up and start_square_up != goal_up:
        remove_piece_from_pinning_candidates_diag_up(moved_bishop, start, enemy_king)
    elif start_square_down == king_down and start_square_down != goal_down:
        remove_piece_from_pinning_candidates_diag_down(moved_bishop, start, enemy_king)


########################################################################################################################
# functions to remove piece from pinning_candidates depending on relation to enemy king


def remove_piece_from_pinning_candidates_row(moved_piece, start: tuple, enemy_king):
    if start[1] < enemy_king.col:
        gss.pinning_candidates[moved_piece.color]["left"].remove(moved_piece)
    else:
        gss.pinning_candidates[moved_piece.color]["right"].remove(moved_piece)


def remove_piece_from_pinning_candidates_col(moved_piece, start: tuple, enemy_king):
    if start[0] < enemy_king.row:
        gss.pinning_candidates[moved_piece.color]["above"].remove(moved_piece)
    else:
        gss.pinning_candidates[moved_piece.color]["below"].remove(moved_piece)


def remove_piece_from_pinning_candidates_diag_up(moved_piece, start: tuple, enemy_king):
    if start[0] < enemy_king.row:
        gss.pinning_candidates[moved_piece.color]["right_above"].remove(moved_piece)
    else:
        gss.pinning_candidates[moved_piece.color]["left_below"].remove(moved_piece)


def remove_piece_from_pinning_candidates_diag_down(moved_piece, start: tuple, enemy_king):
    if start[0] < enemy_king.row:
        gss.pinning_candidates[moved_piece.color]["left_above"].remove(moved_piece)
    else:
        gss.pinning_candidates[moved_piece.color]["right_below"].remove(moved_piece)


def remove_captured_piece_from_pinning_candidates(captured_piece, enemy_king):
    match captured_piece.get_type():
        case "Queen":
            if captured_piece.row == enemy_king.row:
                if captured_piece.col < enemy_king.col:
                    gss.pinning_candidates[captured_piece.color]["left"].remove(captured_piece)
                else:
                    gss.pinning_candidates[captured_piece.color]["right"].remove(captured_piece)
            elif captured_piece.col == enemy_king.col:
                if captured_piece.row < enemy_king.row:
                    gss.pinning_candidates[captured_piece.color]["above"].remove(captured_piece)
                else:
                    gss.pinning_candidates[captured_piece.color]["below"].remove(captured_piece)
            elif captured_piece.row + captured_piece.col == enemy_king.row + enemy_king.col:
                if captured_piece.row < enemy_king.row:
                    gss.pinning_candidates[captured_piece.color]["right_above"].remove(captured_piece)
                else:
                    gss.pinning_candidates[captured_piece.color]["left_below"].remove(captured_piece)
            elif captured_piece.row - captured_piece.col == enemy_king.row - enemy_king.col:
                if captured_piece.row < enemy_king.row:
                    gss.pinning_candidates[captured_piece.color]["left_above"].remove(captured_piece)
                else:
                    gss.pinning_candidates[captured_piece.color]["right_below"].remove(captured_piece)
        case "Rook":
            if captured_piece.row == enemy_king.row:
                if captured_piece.col < enemy_king.col:
                    gss.pinning_candidates[captured_piece.color]["left"].remove(captured_piece)
                else:
                    gss.pinning_candidates[captured_piece.color]["right"].remove(captured_piece)
            elif captured_piece.col == enemy_king.col:
                if captured_piece.row < enemy_king.row:
                    gss.pinning_candidates[captured_piece.color]["above"].remove(captured_piece)
                else:
                    gss.pinning_candidates[captured_piece.color]["below"].remove(captured_piece)
        case "Bishop":
            if captured_piece.row + captured_piece.col == enemy_king.row + enemy_king.col:
                if captured_piece.row < enemy_king.row:
                    gss.pinning_candidates[captured_piece.color]["right_above"].remove(captured_piece)
                else:
                    gss.pinning_candidates[captured_piece.color]["left_below"].remove(captured_piece)
            elif captured_piece.row - captured_piece.col == enemy_king.row - enemy_king.col:
                if captured_piece.row < enemy_king.row:
                    gss.pinning_candidates[captured_piece.color]["left_above"].remove(captured_piece)
                else:
                    gss.pinning_candidates[captured_piece.color]["right_below"].remove(captured_piece)


########################################################################################################################
# functions to add piece to pinning_candidates depending on piece type


def add_queen_to_pinning_candidates(moved_queen, start: tuple, goal: tuple, enemy_king):
    if goal[0] == enemy_king.row and start[0] != goal[0]:
        add_piece_to_pinning_candidates_row(moved_queen, goal, enemy_king)
    elif goal[1] == enemy_king.col and start[1] != goal[1]:
        add_piece_to_pinning_candidates_col(moved_queen, goal, enemy_king)
    else:
        start_up = start[0] + start[1]
        king_up = enemy_king.row + enemy_king.col
        goal_up = goal[0] + goal[1]
        start_down = start[0] - start[1]
        king_down = enemy_king.row - enemy_king.col
        goal_down = goal[0] - goal[1]
        if goal_up == king_up and start_up != goal_up:
            add_piece_to_pinning_candidates_diag_up(moved_queen, goal, enemy_king)
        elif goal_down == king_down and start_down != goal_down:
            add_piece_to_pinning_candidates_diag_down(moved_queen, goal, enemy_king)


def add_rook_to_pinning_candidates(moved_rook, start: tuple, goal: tuple, enemy_king):
    if goal[0] == enemy_king.row and start[0] != goal[0]:
        add_piece_to_pinning_candidates_row(moved_rook, goal, enemy_king)
    elif goal[1] == enemy_king.col and start[1] != goal[1]:
        add_piece_to_pinning_candidates_col(moved_rook, goal, enemy_king)


def add_bishop_to_pinning_candidates(moved_bishop, start: tuple, goal: tuple, enemy_king):
    start_up = start[0] + start[1]
    king_up = enemy_king.row + enemy_king.col
    goal_up = goal[0] + goal[1]
    start_down = start[0] - start[1]
    king_down = enemy_king.row - enemy_king.col
    goal_down = goal[0] - goal[1]
    if goal_up == king_up and start_up != goal_up:
        add_piece_to_pinning_candidates_diag_up(moved_bishop, goal, enemy_king)
    elif goal_down == king_down and start_down != goal_down:
        add_piece_to_pinning_candidates_diag_down(moved_bishop, goal, enemy_king)


########################################################################################################################
# functions to add new piece to pinning_candidates after pawn transformation depending on piece type


def add_new_queen_to_pinning_candidates(new_queen, location: tuple):
    enemy_king = gss.pieces[not new_queen.color][0]
    if location[0] == enemy_king.row:
        add_piece_to_pinning_candidates_row(new_queen, location, enemy_king)
    elif location[1] == enemy_king.col:
        add_piece_to_pinning_candidates_col(new_queen, location, enemy_king)
    elif location[0] + location[1] == enemy_king.row + enemy_king.col:
        add_piece_to_pinning_candidates_diag_up(new_queen, location, enemy_king)
    elif location[0] - location[1] == enemy_king.row - enemy_king.col:
        add_piece_to_pinning_candidates_diag_down(new_queen, location, enemy_king)


def add_new_rook_to_pinning_candidates(new_rook, location: tuple):
    enemy_king = gss.pieces[not new_rook.color][0]
    if location[0] == enemy_king.row:
        add_piece_to_pinning_candidates_row(new_rook, location, enemy_king)
    elif location[1] == enemy_king.col:
        add_piece_to_pinning_candidates_col(new_rook, location, enemy_king)


def add_new_bishop_to_pinning_candidates(new_bishop, location: tuple):
    enemy_king = gss.pieces[not new_bishop.color][0]
    if location[0] + location[1] == enemy_king.row + enemy_king.col:
        add_piece_to_pinning_candidates_diag_up(new_bishop, location, enemy_king)
    elif location[0] - location[1] == enemy_king.row - enemy_king.col:
        add_piece_to_pinning_candidates_diag_down(new_bishop, location, enemy_king)


########################################################################################################################
# functions to add piece to pinning_candidates depending on relation to enemy king


def add_piece_to_pinning_candidates_row(moved_piece, goal: tuple, enemy_king):
    if goal[1] < enemy_king.col:
        insert_to_pinning_candidates(moved_piece, "left")
    else:
        insert_to_pinning_candidates(moved_piece, "right")


def add_piece_to_pinning_candidates_col(moved_piece, goal: tuple, enemy_king):
    if goal[0] < enemy_king.row:
        insert_to_pinning_candidates(moved_piece, "above")
    else:
        insert_to_pinning_candidates(moved_piece, "below")


def add_piece_to_pinning_candidates_diag_up(moved_piece, goal: tuple, enemy_king):
    if goal[0] < enemy_king.row:
        insert_to_pinning_candidates(moved_piece, "right_above")
    else:
        insert_to_pinning_candidates(moved_piece, "left_below")


def add_piece_to_pinning_candidates_diag_down(moved_piece, goal: tuple, enemy_king):
    if goal[0] < enemy_king.row:
        insert_to_pinning_candidates(moved_piece, "left_above")
    else:
        insert_to_pinning_candidates(moved_piece, "right_below")


########################################################################################################################
# insert piece


def insert_to_pinning_candidates(to_be_inserted, pinning_from: str):
    match pinning_from:
        case "above" | "left_above" | "right_above":
            inserted = False
            for i, pinning_piece in enumerate(gss.pinning_candidates[to_be_inserted.color][pinning_from]):
                if to_be_inserted.row > pinning_piece.row:
                    gss.pinning_candidates[to_be_inserted.color][pinning_from].insert(i, to_be_inserted)
                    inserted = True
                    break
            if not inserted:
                gss.pinning_candidates[to_be_inserted.color][pinning_from].append(to_be_inserted)
        case "below" | "left_below" | "right_below":
            inserted = False
            for i, pinning_piece in enumerate(gss.pinning_candidates[to_be_inserted.color][pinning_from]):
                if to_be_inserted.row < pinning_piece.row:
                    gss.pinning_candidates[to_be_inserted.color][pinning_from].insert(i, to_be_inserted)
                    inserted = True
                    break
            if not inserted:
                gss.pinning_candidates[to_be_inserted.color][pinning_from].append(to_be_inserted)
        case "left":
            inserted = False
            for i, pinning_piece in enumerate(gss.pinning_candidates[to_be_inserted.color][pinning_from]):
                if to_be_inserted.col > pinning_piece.col:
                    gss.pinning_candidates[to_be_inserted.color][pinning_from].insert(i, to_be_inserted)
                    inserted = True
                    break
            if not inserted:
                gss.pinning_candidates[to_be_inserted.color][pinning_from].append(to_be_inserted)
        case "right":
            inserted = False
            for i, pinning_piece in enumerate(gss.pinning_candidates[to_be_inserted.color][pinning_from]):
                if to_be_inserted.col < pinning_piece.col:
                    gss.pinning_candidates[to_be_inserted.color][pinning_from].insert(i, to_be_inserted)
                    inserted = True
                    break
            if not inserted:
                gss.pinning_candidates[to_be_inserted.color][pinning_from].append(to_be_inserted)


########################################################################################################################
########################################################################################################################
# functions to reset pinning_candidates


def reset_pins(moved_king):
    for maybe_pinned in gss.pieces[moved_king.color]:
        if maybe_pinned.get_type != "King":
            maybe_pinned.pinned_from = None
    maybe_pinning_color = not moved_king.color
    gss.pinning_candidates[maybe_pinning_color]["above"] = []
    gss.pinning_candidates[maybe_pinning_color]["right_above"] = []
    gss.pinning_candidates[maybe_pinning_color]["right"] = []
    gss.pinning_candidates[maybe_pinning_color]["right_below"] = []
    gss.pinning_candidates[maybe_pinning_color]["below"] = []
    gss.pinning_candidates[maybe_pinning_color]["left_below"] = []
    gss.pinning_candidates[maybe_pinning_color]["left"] = []
    gss.pinning_candidates[maybe_pinning_color]["left_above"] = []
    for pinning_candidate in gss.pieces[maybe_pinning_color]:
        match pinning_candidate.get_type():
            case "Queen":
                add_queen_to_reset_pinning_candidates(pinning_candidate, moved_king)
            case "Rook":
                add_rook_to_reset_pinning_candidates(pinning_candidate, moved_king)
            case "Bishop":
                add_bishop_to_reset_pinning_candidates(pinning_candidate, moved_king)
    update_pin_attributes_above(moved_king)
    update_pin_attributes_right_above(moved_king)
    update_pin_attributes_right(moved_king)
    update_pin_attributes_right_below(moved_king)
    update_pin_attributes_below(moved_king)
    update_pin_attributes_left_below(moved_king)
    update_pin_attributes_left(moved_king)
    update_pin_attributes_left_above(moved_king)


def add_queen_to_reset_pinning_candidates(pinning_candidate, enemy_king):
    goal = (pinning_candidate.row, pinning_candidate.col)
    if goal[0] == enemy_king.row:
        add_piece_to_pinning_candidates_row(pinning_candidate, goal, enemy_king)
    elif goal[1] == enemy_king.col:
        add_piece_to_pinning_candidates_col(pinning_candidate, goal, enemy_king)
    else:
        king_up = enemy_king.row + enemy_king.col
        goal_up = goal[0] + goal[1]
        king_down = enemy_king.row - enemy_king.col
        goal_down = goal[0] - goal[1]
        if goal_up == king_up:
            add_piece_to_pinning_candidates_diag_up(pinning_candidate, goal, enemy_king)
        elif goal_down == king_down:
            add_piece_to_pinning_candidates_diag_down(pinning_candidate, goal, enemy_king)


def add_rook_to_reset_pinning_candidates(pinning_candidate, enemy_king):
    goal = (pinning_candidate.row, pinning_candidate.col)
    if goal[0] == enemy_king.row:
        add_piece_to_pinning_candidates_row(pinning_candidate, goal, enemy_king)
    elif goal[1] == enemy_king.col:
        add_piece_to_pinning_candidates_col(pinning_candidate, goal, enemy_king)


def add_bishop_to_reset_pinning_candidates(pinning_candidate, enemy_king):
    goal = (pinning_candidate.row, pinning_candidate.col)
    king_up = enemy_king.row + enemy_king.col
    goal_up = goal[0] + goal[1]
    king_down = enemy_king.row - enemy_king.col
    goal_down = goal[0] - goal[1]
    if goal_up == king_up:
        add_piece_to_pinning_candidates_diag_up(pinning_candidate, goal, enemy_king)
    elif goal_down == king_down:
        add_piece_to_pinning_candidates_diag_down(pinning_candidate, goal, enemy_king)


########################################################################################################################
########################################################################################################################
# functions to update pin attributes


def update_pin_attributes(start: tuple, goal: tuple):
    king = gss.pieces[True][0]
    update_pin_attributes_depending_on_king(start, goal, king)
    king = gss.pieces[False][0]
    update_pin_attributes_depending_on_king(start, goal, king)


def update_pin_attributes_en_passant(start: tuple, goal: tuple):
    captured_pawn_square = (start[0], goal[1])
    king = gss.pieces[True][0]
    update_pin_attributes_depending_on_king(start, goal, king)
    update_pin_attributes_depending_on_king_en_passant(captured_pawn_square, king)
    king = gss.pieces[False][0]
    update_pin_attributes_depending_on_king(start, goal, king)
    update_pin_attributes_depending_on_king_en_passant(captured_pawn_square, king)


def update_pin_attributes_depending_on_king(start: tuple, goal: tuple, king):
    update_pin_attributes_row(start, goal, king)
    update_pin_attributes_col(start, goal, king)
    update_pin_attributes_diag_up(start, goal, king)
    update_pin_attributes_diag_down(start, goal, king)


def update_pin_attributes_depending_on_king_en_passant(captured_pawn_square: tuple, king):
    if captured_pawn_square[0] + captured_pawn_square[1] == king.row + king.col:
        if captured_pawn_square[0] < king.row:
            update_pin_attributes_right_above(king)
        else:
            update_pin_attributes_left_below(king)
    elif captured_pawn_square[0] - captured_pawn_square[1] == king.row - king.col:
        if captured_pawn_square[0] < king.row:
            update_pin_attributes_left_above(king)
        else:
            update_pin_attributes_right_below(king)


########################################################################################################################
# functions to update pin attributes depending on start and goal position


def update_pin_attributes_row(start: tuple, goal: tuple, king):
    if start[0] == king.row:
        if start[1] < king.col:
            update_pin_attributes_left(king)
        else:
            update_pin_attributes_right(king)
    elif goal[0] == king.row:
        if goal[1] < king.col:
            update_pin_attributes_left(king)
        else:
            update_pin_attributes_right(king)


def update_pin_attributes_col(start: tuple, goal: tuple, king):
    if start[1] == king.col:
        if start[0] < king.row:
            update_pin_attributes_above(king)
        else:
            update_pin_attributes_below(king)
    elif goal[1] == king.col:
        if goal[0] < king.row:
            update_pin_attributes_above(king)
        else:
            update_pin_attributes_below(king)


def update_pin_attributes_diag_up(start: tuple, goal: tuple, king):
    if start[0] + start[1] == king.row + king.col:
        if start[0] < king.row:
            update_pin_attributes_right_above(king)
        else:
            update_pin_attributes_left_below(king)
    elif goal[0] + goal[1] == king.row + king.col:
        if goal[0] < king.row:
            update_pin_attributes_right_above(king)
        else:
            update_pin_attributes_left_below(king)


def update_pin_attributes_diag_down(start: tuple, goal: tuple, king):
    if start[0] - start[1] == king.row - king.col:
        if start[0] < king.row:
            update_pin_attributes_left_above(king)
        else:
            update_pin_attributes_right_below(king)
    elif goal[0] - goal[1] == king.row - king.col:
        if goal[0] < king.row:
            update_pin_attributes_left_above(king)
        else:
            update_pin_attributes_right_below(king)


########################################################################################################################
# functions to update pin attributes depending on pinning direction


def update_pin_attributes_above(king):
    for r_ in range(king.row):
        if not board.is_empty(r_, king.col):
            maybe_pinned = board.squares[r_][king.col].piece
            if maybe_pinned.color == king.color:
                maybe_pinned.pinned_from = None
    if len(gss.pinning_candidates[not king.color]["above"]) == 0:
        return
    maybe_pinning = gss.pinning_candidates[not king.color]["above"][0]
    maybe_pinned = None
    for r_ in range(maybe_pinning.row + 1, king.row):
        if not board.is_empty(r_, king.col):
            if maybe_pinned is not None:
                return
            maybe_pinned = board.squares[r_][king.col].piece
    if maybe_pinned is not None and maybe_pinned.color == king.color:
        maybe_pinned.pinned_from = "above"


def update_pin_attributes_right_above(king):
    r_ = king.row - 1
    c_ = king.col + 1
    while board.on_board(r_, c_):
        if not board.is_empty(r_, c_):
            maybe_pinned = board.squares[r_][c_].piece
            if maybe_pinned.color == king.color:
                maybe_pinned.pinned_from = None
        r_ -= 1
        c_ += 1
    if len(gss.pinning_candidates[not king.color]["right_above"]) == 0:
        return
    maybe_pinning = gss.pinning_candidates[not king.color]["right_above"][0]
    maybe_pinned = None
    r_ = king.row - 1
    c_ = king.col + 1
    while r_ != maybe_pinning.row:
        if not board.is_empty(r_, c_):
            if maybe_pinned is not None:
                return
            maybe_pinned = board.squares[r_][c_].piece
        r_ -= 1
        c_ += 1
    if maybe_pinned is not None and maybe_pinned.color == king.color:
        maybe_pinned.pinned_from = "right_above"


def update_pin_attributes_right(king):
    for c_ in range(king.col + 1, 8):
        if not board.is_empty(king.row, c_):
            maybe_pinned = board.squares[king.row][c_].piece
            if maybe_pinned.color == king.color:
                maybe_pinned.pinned_from = None
    if len(gss.pinning_candidates[not king.color]["right"]) == 0:
        return
    maybe_pinning = gss.pinning_candidates[not king.color]["right"][0]
    maybe_pinned = None
    for c_ in range(king.col + 1, maybe_pinning.col):
        if not board.is_empty(king.row, c_):
            if maybe_pinned is not None:
                return
            maybe_pinned = board.squares[king.row][c_].piece
    if maybe_pinned is not None and maybe_pinned.color == king.color:
        maybe_pinned.pinned_from = "right"


def update_pin_attributes_right_below(king):
    r_ = king.row + 1
    c_ = king.col + 1
    while board.on_board(r_, c_):
        if not board.is_empty(r_, c_):
            maybe_pinned = board.squares[r_][c_].piece
            if maybe_pinned.color == king.color:
                maybe_pinned.pinned_from = None
        r_ += 1
        c_ += 1
    if len(gss.pinning_candidates[not king.color]["right_below"]) == 0:
        return
    maybe_pinning = gss.pinning_candidates[not king.color]["right_below"][0]
    maybe_pinned = None
    r_ = king.row + 1
    c_ = king.col + 1
    while r_ != maybe_pinning.row:
        if not board.is_empty(r_, c_):
            if maybe_pinned is not None:
                return
            maybe_pinned = board.squares[r_][c_].piece
        r_ += 1
        c_ += 1
    if maybe_pinned is not None and maybe_pinned.color == king.color:
        maybe_pinned.pinned_from = "right_below"


def update_pin_attributes_below(king):
    for r_ in range(king.row + 1, 8):
        if not board.is_empty(r_, king.col):
            maybe_pinned = board.squares[r_][king.col].piece
            if maybe_pinned.color == king.color:
                maybe_pinned.pinned_from = None
    if len(gss.pinning_candidates[not king.color]["below"]) == 0:
        return
    maybe_pinning = gss.pinning_candidates[not king.color]["below"][0]
    maybe_pinned = None
    for r_ in range(king.row + 1, maybe_pinning.row):
        if not board.is_empty(r_, king.col):
            if maybe_pinned is not None:
                return
            maybe_pinned = board.squares[r_][king.col].piece
    if maybe_pinned is not None and maybe_pinned.color == king.color:
        maybe_pinned.pinned_from = "below"


def update_pin_attributes_left_below(king):
    r_ = king.row + 1
    c_ = king.col - 1
    while board.on_board(r_, c_):
        if not board.is_empty(r_, c_):
            maybe_pinned = board.squares[r_][c_].piece
            if maybe_pinned.color == king.color:
                maybe_pinned.pinned_from = None
        r_ += 1
        c_ -= 1
    if len(gss.pinning_candidates[not king.color]["left_below"]) == 0:
        return
    maybe_pinning = gss.pinning_candidates[not king.color]["left_below"][0]
    maybe_pinned = None
    r_ = king.row + 1
    c_ = king.col - 1
    while r_ != maybe_pinning.row:
        if not board.is_empty(r_, c_):
            if maybe_pinned is not None:
                return
            maybe_pinned = board.squares[r_][c_].piece
        r_ += 1
        c_ -= 1
    if maybe_pinned is not None and maybe_pinned.color == king.color:
        maybe_pinned.pinned_from = "left_below"


def update_pin_attributes_left(king):
    for c_ in range(king.col):
        if not board.is_empty(king.row, c_):
            maybe_pinned = board.squares[king.row][c_].piece
            if maybe_pinned.color == king.color:
                maybe_pinned.pinned_from = None
    if len(gss.pinning_candidates[not king.color]["left"]) == 0:
        return
    maybe_pinning = gss.pinning_candidates[not king.color]["left"][0]
    maybe_pinned = None
    for c_ in range(maybe_pinning.col + 1, king.col):
        if not board.is_empty(king.row, c_):
            if maybe_pinned is not None:
                return
            maybe_pinned = board.squares[king.row][c_].piece
    if maybe_pinned is not None and maybe_pinned.color == king.color:
        maybe_pinned.pinned_from = "left"


def update_pin_attributes_left_above(king):
    r_ = king.row - 1
    c_ = king.col - 1
    while board.on_board(r_, c_):
        if not board.is_empty(r_, c_):
            maybe_pinned = board.squares[r_][c_].piece
            if maybe_pinned.color == king.color:
                maybe_pinned.pinned_from = None
        r_ -= 1
        c_ -= 1
    if len(gss.pinning_candidates[not king.color]["left_above"]) == 0:
        return
    maybe_pinning = gss.pinning_candidates[not king.color]["left_above"][0]
    maybe_pinned = None
    r_ = king.row - 1
    c_ = king.col - 1
    while r_ != maybe_pinning.row:
        if not board.is_empty(r_, c_):
            if maybe_pinned is not None:
                return
            maybe_pinned = board.squares[r_][c_].piece
        r_ -= 1
        c_ -= 1
    if maybe_pinned is not None and maybe_pinned.color == king.color:
        maybe_pinned.pinned_from = "left_above"
