import game_states_and_settings as gss
import board
import pins
import check_tests as ct

########################################################################################################################
########################################################################################################################
# functions to execute moves

########################################################################################################################
# functions to execute moves depending on piece type


def execute_move_king(moved_king, start: tuple, goal: tuple):
    if goal[1] == moved_king.col + 2:
        moved_rook = board.squares[moved_king.row][7].piece
        rook_start = (moved_king.row, 7)
        rook_goal = (moved_king.row, 5)
        relocate(moved_king, start, goal)
        relocate(moved_rook, rook_start, rook_goal)
        pins.update_pins_rook(moved_rook, rook_start, rook_goal)
        ct.direct_check_test_rook(moved_rook.color, rook_goal)
        pins.update_pin_attributes(rook_start, rook_goal)
        gss.counter_no_pawn_no_capture += 1
    elif goal[1] == moved_king.col - 2:
        moved_rook = board.squares[moved_king.row][0].piece
        rook_start = (moved_king.row, 0)
        rook_goal = (moved_king.row, 3)
        relocate(moved_king, start, goal)
        relocate(moved_rook, rook_start, rook_goal)
        pins.update_pins_rook(moved_rook, rook_start, rook_goal)
        ct.direct_check_test_rook(moved_rook.color, rook_goal)
        pins.update_pin_attributes(rook_start, rook_goal)
        gss.counter_no_pawn_no_capture += 1
    else:
        if board.is_empty(goal[0], goal[1]):
            relocate(moved_king, start, goal)
            gss.counter_no_pawn_no_capture += 1
            gss.update_history()
        else:
            clear(goal)
            relocate(moved_king, start, goal)
            gss.counter_no_pawn_no_capture = 0
            gss.clear_history()
            gss.history_1.append(board.board_to_str())
            update_draw_not_enough_material()
    pins.reset_pins(moved_king)
    if gss.castling_possible[moved_king.color]["00"]:
        gss.castling_possible[moved_king.color]["00"] = False
        gss.clear_history()
        gss.history_1.append(board.board_to_str())
    if gss.castling_possible[moved_king.color]["000"]:
        gss.castling_possible[moved_king.color]["000"] = False
        gss.clear_history()
        gss.history_1.append(board.board_to_str())
    enemy_king = gss.pieces[not moved_king.color][0]
    pins.update_pin_attributes_depending_on_king(start, goal, enemy_king)
    ct.deduction_check_test(moved_king.color, start, goal)


def execute_move_queen(moved_queen, start: tuple, goal: tuple):
    gss.update_castling_right(goal)
    if board.is_empty(goal[0], goal[1]):
        relocate(moved_queen, start, goal)
        gss.counter_no_pawn_no_capture += 1
        gss.update_history()
    else:
        clear(goal)
        relocate(moved_queen, start, goal)
        gss.counter_no_pawn_no_capture = 0
        gss.clear_history()
        gss.history_1.append(board.board_to_str())
        update_draw_not_enough_material()
    pins.update_pins_queen(moved_queen, start, goal)
    ct.direct_check_test_queen(moved_queen.color, goal)
    pins.update_pin_attributes(start, goal)


def execute_move_rook(moved_rook, start: tuple, goal: tuple):
    gss.update_castling_right(start)
    gss.update_castling_right(goal)
    if board.is_empty(goal[0], goal[1]):
        relocate(moved_rook, start, goal)
        gss.counter_no_pawn_no_capture += 1
        gss.update_history()
    else:
        clear(goal)
        relocate(moved_rook, start, goal)
        gss.counter_no_pawn_no_capture = 0
        gss.clear_history()
        gss.history_1.append(board.board_to_str())
        update_draw_not_enough_material()
    pins.update_pins_rook(moved_rook, start, goal)
    ct.direct_check_test_rook(moved_rook.color, goal)
    ct.deduction_check_test(moved_rook.color, start, goal)
    pins.update_pin_attributes(start, goal)


def execute_move_knight(moved_knight, start: tuple, goal: tuple):
    gss.update_castling_right(goal)
    if board.is_empty(goal[0], goal[1]):
        relocate(moved_knight, start, goal)
        gss.counter_no_pawn_no_capture += 1
        gss.update_history()
    else:
        clear(goal)
        relocate(moved_knight, start, goal)
        gss.counter_no_pawn_no_capture = 0
        gss.clear_history()
        gss.history_1.append(board.board_to_str())
        update_draw_not_enough_material()
    ct.direct_check_test_knight(moved_knight.color, goal)
    ct.deduction_check_test(moved_knight.color, start, goal)
    pins.update_pin_attributes(start, goal)


def execute_move_bishop(moved_bishop, start: tuple, goal: tuple):
    gss.update_castling_right(goal)
    if board.is_empty(goal[0], goal[1]):
        relocate(moved_bishop, start, goal)
        gss.counter_no_pawn_no_capture += 1
        gss.update_history()
    else:
        clear(goal)
        relocate(moved_bishop, start, goal)
        gss.counter_no_pawn_no_capture = 0
        gss.clear_history()
        gss.history_1.append(board.board_to_str())
        update_draw_not_enough_material()
    pins.update_pins_bishop(moved_bishop, start, goal)
    ct.direct_check_test_bishop(moved_bishop.color, goal)
    ct.deduction_check_test(moved_bishop.color, start, goal)
    pins.update_pin_attributes(start, goal)


def execute_move_pawn(moved_pawn, start: tuple, goal: tuple):
    gss.counter_no_pawn_no_capture = 0
    gss.clear_history()
    gss.history_1.append(board.board_to_str())
    gss.update_castling_right(goal)
    if not moved_pawn.has_moved:
        moved_pawn.has_moved = True
        gss.update_possible_en_passant_moves(start, goal)
    capturing_en_passant = False
    if start[1] != goal[1]:
        if not board.is_empty(goal[0], goal[1]):
            clear(goal)
        else:
            capturing_en_passant = True
            clear((start[0], goal[1]))
            board.squares[start[0]][goal[1]].piece = None
        update_draw_not_enough_material()
    relocate(moved_pawn, start, goal)
    ct.direct_check_test_pawn(moved_pawn.color, goal)
    ct.deduction_check_test(moved_pawn.color, start, goal)
    if capturing_en_passant:
        ct.deduction_check_test_en_passant(moved_pawn.color, start, goal)
        pins.update_pin_attributes_en_passant(start, goal)
    else:
        pins.update_pin_attributes(start, goal)


########################################################################################################################
# pawn transformations


def execute_transformation_to_queen(moved_pawn, start: tuple, goal: tuple, new_queen):
    gss.counter_no_pawn_no_capture = 0
    gss.clear_history()
    gss.history_1.append(board.board_to_str())
    gss.update_castling_right(goal)
    pins.add_new_queen_to_pinning_candidates(new_queen, goal)
    board.squares[start[0]][start[1]].piece = None
    board.squares[goal[0]][goal[1]].piece = new_queen
    gss.pieces[moved_pawn.color].remove(moved_pawn)
    gss.pieces[moved_pawn.color].append(new_queen)
    ct.direct_check_test_queen(new_queen.color, goal)
    ct.deduction_check_test(moved_pawn.color, start, goal)
    pins.update_pin_attributes(start, goal)
    gss.move_to_notation[(start, goal)][0] = gss.move_to_notation[(start, goal)][0] + "=Q"


def execute_transformation_to_rook(moved_pawn, start: tuple, goal: tuple, new_rook):
    gss.counter_no_pawn_no_capture = 0
    gss.clear_history()
    gss.history_1.append(board.board_to_str())
    gss.update_castling_right(goal)
    pins.add_new_rook_to_pinning_candidates(new_rook, goal)
    board.squares[start[0]][start[1]].piece = None
    board.squares[goal[0]][goal[1]].piece = new_rook
    gss.pieces[moved_pawn.color].remove(moved_pawn)
    gss.pieces[moved_pawn.color].append(new_rook)
    ct.direct_check_test_rook(new_rook.color, goal)
    ct.deduction_check_test(moved_pawn.color, start, goal)
    pins.update_pin_attributes(start, goal)
    gss.move_to_notation[(start, goal)][0] = gss.move_to_notation[(start, goal)][0] + "=R"


def execute_transformation_to_knight(moved_pawn, start: tuple, goal: tuple, new_knight):
    gss.counter_no_pawn_no_capture = 0
    gss.clear_history()
    gss.history_1.append(board.board_to_str())
    update_draw_not_enough_material()
    gss.update_castling_right(goal)
    board.squares[start[0]][start[1]].piece = None
    board.squares[goal[0]][goal[1]].piece = new_knight
    gss.pieces[moved_pawn.color].remove(moved_pawn)
    gss.pieces[moved_pawn.color].append(new_knight)
    ct.direct_check_test_knight(new_knight.color, goal)
    ct.deduction_check_test(moved_pawn.color, start, goal)
    pins.update_pin_attributes(start, goal)
    gss.move_to_notation[(start, goal)][0] = gss.move_to_notation[(start, goal)][0] + "=N"


def execute_transformation_to_bishop(moved_pawn, start: tuple, goal: tuple, new_bishop):
    gss.counter_no_pawn_no_capture = 0
    gss.clear_history()
    gss.history_1.append(board.board_to_str())
    update_draw_not_enough_material()
    gss.update_castling_right(goal)
    pins.add_new_bishop_to_pinning_candidates(new_bishop, goal)
    board.squares[start[0]][start[1]].piece = None
    board.squares[goal[0]][goal[1]].piece = new_bishop
    gss.pieces[moved_pawn.color].remove(moved_pawn)
    gss.pieces[moved_pawn.color].append(new_bishop)
    ct.direct_check_test_bishop(new_bishop.color, goal)
    ct.deduction_check_test(moved_pawn.color, start, goal)
    pins.update_pin_attributes(start, goal)
    gss.move_to_notation[(start, goal)][0] = gss.move_to_notation[(start, goal)][0] + "=B"


########################################################################################################################
# other functions


def clear(goal: tuple):
    captured_piece = board.squares[goal[0]][goal[1]].piece
    enemy_king = gss.pieces[not captured_piece.color][0]
    pins.remove_captured_piece_from_pinning_candidates(captured_piece, enemy_king)
    gss.pieces[captured_piece.color].remove(captured_piece)


def relocate(moved_piece, start: tuple, goal: tuple):
    board.squares[goal[0]][goal[1]].piece = moved_piece
    board.squares[start[0]][start[1]].piece = None
    moved_piece.row = goal[0]
    moved_piece.col = goal[1]


def add_x_to_notation(start, goal):
    for i, notation in enumerate(gss.move_to_notation[(start, goal)]):
        gss.move_to_notation[(start, goal)][i] = notation[:-2] + "x" + notation[-2:]


def update_draw_not_enough_material():
    num_pieces = (len(gss.pieces[True]), len(gss.pieces[False]))
    match num_pieces:
        case (1, 1):
            gss.draw_not_enough_material = True
        case (1, 2):
            piece_type = gss.pieces[False][1].get_type()
            if piece_type == "Bishop" or piece_type == "Knight":
                gss.draw_not_enough_material = True
        case (2, 1):
            piece_type = gss.pieces[True][1].get_type()
            if piece_type == "Bishop" or piece_type == "Knight":
                gss.draw_not_enough_material = True
        case (2, 2):
            if gss.pieces[True][1].get_type() == "Bishop" and gss.pieces[False][1].get_type() == "Bishop":
                bishop_w = gss.pieces[True][1]
                bishop_b = gss.pieces[False][1]
                square_color_w = (bishop_w.row + bishop_w.col) % 2
                square_color_b = (bishop_b.row + bishop_b.col) % 2
                if square_color_w == square_color_b:
                    gss.draw_not_enough_material = True
