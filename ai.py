import random
import board
import gui
import game_states_and_settings as gss


def play():
    for move in gss.possible_pawn_transformations:
        gss.legal_moves.append((move[0], move[1], "Queen"))
        gss.legal_moves.append((move[0], move[1], "Rook"))
        gss.legal_moves.append((move[0], move[1], "Knight"))
        gss.legal_moves.append((move[0], move[1], "Bishop"))
    if len(gss.legal_moves) > 0:
        gss.possible_en_passant_moves = []
        random_move = random.choice(gss.legal_moves)
        chosen_piece = board.squares[random_move[0][0]][random_move[0][1]].piece
        if len(random_move) == 2:
            chosen_piece.execute_move(random_move[0], random_move[1])
        else:
            chosen_piece.execute_transformation(random_move[0], random_move[1], random_move[2])
        gui.reset_str_executed_move((random_move[0], random_move[1]))
        if gss.counter_no_pawn_no_capture == 50:
            gss.legal_moves = []
            gss.possible_pawn_transformations = []
            gui.set_end_of_game_message("too_many_moves")
        elif gss.draw_position_repetition:
            gss.legal_moves = []
            gss.possible_pawn_transformations = []
            gui.set_end_of_game_message("position_repetition")
        elif gss.draw_not_enough_material:
            gss.legal_moves = []
            gss.possible_pawn_transformations = []
            gui.set_end_of_game_message("material")
        else:
            gss.reset_legal_moves()
            if len(gss.legal_moves) == 0:
                if gss.giving_check:
                    if gss.whites_turn:
                        gui.set_end_of_game_message("black_wins")
                    else:
                        gui.set_end_of_game_message("white_wins")
                else:
                    gui.set_end_of_game_message("patt")
        gui.print_executed_move()
