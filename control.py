import pygame
from typing import Optional
import board
import game_states_and_settings as gss
import pieces
import gui

running = True
grabbed: Optional[pieces.Piece] = None
transforming_pawn = False
transformation_square: Optional[tuple] = None
being_transformed: Optional[pieces.Pawn] = None

gui.reset_and_draw_pieces()
gss.reset_legal_moves()

########################################################################################################################
########################################################################################################################
# functions

########################################################################################################################
# functions around left mouse click


def left_mouse_click(pos):
    global running
    global transforming_pawn
    if gui.s_whole_game.get_height() > gui.s_visible_game.get_height() and gui.r_slider.collidepoint(pos):
        gui.start_scrolling(pos[1])
    elif gui.b_rotate.rect.collidepoint(pos):
        gui.b_rotate_use()
    elif gui.b_exit.rect.collidepoint(pos):
        running = False
    if transforming_pawn:
        if gui.b_new_game.rect.collidepoint(pos):
            transforming_pawn = False
            gui.b_new_game_use()
        else:
            left_mouse_click_if_transforming_pawn(pos)
    else:
        if gui.b_white.rect.collidepoint(pos):
            gui.b_white_use()
        elif gui.b_black.rect.collidepoint(pos):
            gui.b_black_use()
        elif gui.b_new_game.rect.collidepoint(pos):
            gui.b_new_game_use()
        else:
            left_mouse_click_if_not_transforming_pawn(pos)


def left_mouse_click_if_transforming_pawn(pos):
    if gui.square_queen.collidepoint(pos):
        transform_pawn("Queen")
    elif gui.square_rook.collidepoint(pos):
        transform_pawn("Rook")
    elif gui.square_knight.collidepoint(pos):
        transform_pawn("Knight")
    elif gui.square_bishop.collidepoint(pos):
        transform_pawn("Bishop")


def left_mouse_click_if_not_transforming_pawn(pos):
    if (gss.whites_turn and gss.white_human) or (not gss.whites_turn and gss.black_human):
        global grabbed
        grabbed = grab_piece(pos)
        if grabbed is not None:
            pygame.mouse.set_visible(False)


def transform_pawn(piece_type: str):
    gss.possible_en_passant_moves = []
    start = (being_transformed.row, being_transformed.col)
    being_transformed.execute_transformation(start, transformation_square, piece_type)
    gui.reset_str_executed_move((start, transformation_square))
    gss.reset_legal_moves()
    global transforming_pawn
    transforming_pawn = False
    gui.print_executed_move()


def left_mouse_release(pos):
    if gui.scrolling:
        gui.scrolling = False
    if (gss.whites_turn and gss.white_human) or (not gss.whites_turn and gss.black_human):
        global grabbed
        if grabbed is not None:
            release = get_square(pos)
            if release is not None:
                tried_move = ((grabbed.row, grabbed.col), release)
                if tried_move in gss.legal_moves:
                    gss.possible_en_passant_moves = []
                    grabbed.execute_move((grabbed.row, grabbed.col), release)
                    gui.reset_str_executed_move(tried_move)
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
                elif tried_move in gss.possible_pawn_transformations:
                    global transforming_pawn
                    global transformation_square
                    global being_transformed
                    transforming_pawn = True
                    transformation_square = release
                    being_transformed = grabbed
            grabbed = None
            pygame.mouse.set_visible(True)


def update():
    gui.screen.fill(gui.background)
    gui.draw_menu()
    if grabbed is None:
        if transforming_pawn:
            gui.draw_squares_and_pieces_except(being_transformed)
        else:
            gui.draw_squares_and_pieces()
    else:
        gui.draw_squares_and_pieces_except(grabbed)
        x, y = pygame.mouse.get_pos()
        x -= grabbed.img.get_width() / 2
        y -= grabbed.img.get_height() / 2
        gui.screen.blit(grabbed.img, (x, y))
    if transforming_pawn:
        gui.draw_selection(transformation_square[1])
    pygame.display.update()


def grab_piece(pos):
    for r_ in range(8):
        for c_ in range(8):
            if gui.square_rects[r_][c_].collidepoint(pos):
                if gui.board_from_white_players_perspective:
                    click_r = r_
                    click_c = c_
                else:
                    click_r = 7 - r_
                    click_c = 7 - c_
                return board.squares[click_r][click_c].piece
    return None


def get_square(pos):
    for r_ in range(8):
        for c_ in range(8):
            if gui.square_rects[r_][c_].collidepoint(pos):
                if gui.board_from_white_players_perspective:
                    click_r = r_
                    click_c = c_
                else:
                    click_r = 7 - r_
                    click_c = 7 - c_
                return click_r, click_c
    return None
    
