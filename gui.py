import pygame
import board
import game_states_and_settings as gss
import pieces

pygame.init()

background = (16, 16, 16)
button_color = (24, 24, 24)
font_color = (255, 255, 255)
black = (0, 0, 0)
white = (255, 255, 255)
light = (250, 240, 230)
dark = (205, 188, 174)
red_check = (255, 0, 0)
red_checkmate = (128, 0, 0)

font = pygame.font.SysFont("monospace", 16)
font_label = pygame.font.SysFont("monospace", 20)
selected_color = True
str_executed_move = ""
scrolling = False
y_mouse_when_scrolling_starts = 0
y_slider_when_scrolling_starts = 0
new_game_size = False
y_whole_on_visible_game = 0

screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
screen.fill(background)

board_from_white_players_perspective = True
square_size = screen.get_height()/8
board_x = (screen.get_width() - screen.get_height()) / 2
board_y = 0

square_rects = []
for r in range(8):
    row_square_rects = []
    for c in range(8):
        new_square = pygame.Rect(board_x + c * square_size, board_y + r * square_size, square_size, square_size)
        row_square_rects.append(new_square)
        if (r + c) % 2 == 0:
            pygame.draw.rect(screen, light, new_square)
        else:
            pygame.draw.rect(screen, dark, new_square)
    square_rects.append(row_square_rects)

square_queen = None
square_rook = None
square_knight = None
square_bishop = None

########################################################################################################################
# gui element sizes for sub menus

x_right = board_x + 8 * square_size + 0.125 * square_size
x_left = 0.125 * square_size
w_elements = board_x - 0.25 * square_size
h_elements = 0.25 * square_size
h_buttons = 3/8 * square_size
tb_gab = 0.0625 * square_size
x_executed_move_left = square_size / 8
x_executed_move_right = w_elements / 2
x_executed_move = x_executed_move_left
y_executed_move = square_size / 8

########################################################################################################################
########################################################################################################################
# classes


class Button:

    def __init__(self, x, y, w, h, text, button_font=font):
        self.font = button_font
        self.rendered_text = self.font.render(text, True, font_color)
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.text_x = self.x + 0.5 * (self.w - self.rendered_text.get_width())
        self.text_y = self.y + 0.5 * (self.h - self.rendered_text.get_height())
        self.rect = pygame.Rect(x, y, w, h)

    def set_text(self, text):
        self.rendered_text = self.font.render(text, True, font_color)
        self.text_x = self.x + 0.5 * (self.w - self.rendered_text.get_width())
        self.text_y = self.y + 0.5 * (self.h - self.rendered_text.get_height())

    def draw(self):
        pygame.draw.rect(screen, button_color, self.rect)
        screen.blit(self.rendered_text, (self.text_x, self.text_y))


########################################################################################################################
########################################################################################################################
# menus

########################################################################################################################
# functions to simplify menu design


def set_label(row, label_text, label_font):
    label = label_font.render(label_text, True, (255, 255, 255))
    y_label = row * 0.5 * square_size + 0.25 * square_size
    return label, y_label


def set_button(x, row, button_text, button_font):
    y = row * 0.5 * square_size + 1/16 * square_size
    return Button(x, y, w_elements, h_buttons, button_text, button_font)


def set_surface(row, num_rows):
    surface = pygame.Surface([w_elements, 0.5 * square_size * num_rows - 1/8 * square_size])
    surface.fill(button_color)
    y_surface = row * 0.5 * square_size
    return surface, y_surface


def set_rect(x, row, num_rows):
    y = row * 0.5 * square_size
    frame = pygame.Rect(x, y, w_elements, 0.5 * square_size * num_rows - 1/8 * square_size)
    return frame


########################################################################################################################
# main menu

l_game_settings, y_l_game_settings = set_label(0, "Spieleinstellungen:", font_label)
b_white = set_button(x_left, 1, "Weiß: Mensch", font)
b_black = set_button(x_left, 2, "Schwarz: Mensch", font)
b_rotate = set_button(x_left, 3, "Brett drehen", font)
b_new_game = set_button(x_left, 4, "Neues Spiel", font)
b_exit = set_button(x_left, 15, "Beenden", font)

l_game, y_l_game = set_label(0, "Spielverlauf:", font_label)
s_whole_game, y_s_whole_game = set_surface(1, 14.5)
s_visible_game, y_s_visible_game = set_surface(1, 15)
x_ = screen.get_width() - 3 * x_left
y_ = y_s_visible_game + x_left
w_ = x_left
h_ = s_visible_game.get_height() - 2 * x_left
r_scroll_bar = pygame.Rect(x_, y_, w_, h_)
r_slider = pygame.Rect(0, 0, 0, 0)

r_end_of_game_message = set_rect(x_right, 15, 1)
l_end_of_game_message, y_l_end_of_game_message = set_label(15, "", font)

########################################################################################################################
########################################################################################################################
# functions

########################################################################################################################
# function to draw the menu


def draw_menu():
    screen.blit(l_game_settings, (x_left, y_l_game_settings))
    b_white.draw()
    b_black.draw()
    b_rotate.draw()
    b_new_game.draw()
    b_exit.draw()
    screen.blit(l_game, (x_right, y_l_game))
    global s_visible_game
    global y_s_visible_game
    global r_scroll_bar
    global y_whole_on_visible_game

    if len(gss.legal_moves) == 0:
        s_visible_game, y_s_visible_game = set_surface(1, 14.5)
        x__ = screen.get_width() - 3 * x_left
        y__ = y_s_visible_game + x_left
        w__ = x_left
        h__ = s_visible_game.get_height() - 2 * x_left
        r_scroll_bar = pygame.Rect(x__, y__, w__, h__)
        screen.blit(l_end_of_game_message, (x_right, y_l_end_of_game_message))

    if s_whole_game.get_height() > s_visible_game.get_height():
        global r_slider
        global new_game_size
        w__ = 2 * x_left
        h__ = int(s_visible_game.get_height() / s_whole_game.get_height() * r_scroll_bar.h)
        x__ = r_scroll_bar.x - 0.5 * x_left
        if scrolling:
            y__ = pygame.mouse.get_pos()[1] - y_mouse_when_scrolling_starts + y_slider_when_scrolling_starts
            y__min = r_scroll_bar.y
            y__max = r_scroll_bar.y + r_scroll_bar.h - h__
            y__ = max(y__min, min(y__, y__max))
            y_min = 0
            y_max = s_visible_game.get_height() - s_whole_game.get_height()
            y_whole_on_visible_game = y_min + (y__ - y__min) * (y_max - y_min) / (y__max - y__min)
        elif new_game_size:
            y__ = r_scroll_bar.y + r_scroll_bar.h - h__
            y_whole_on_visible_game = s_visible_game.get_height() - s_whole_game.get_height()
        else:
            y__ = r_slider.y

        new_game_size = False
        s_visible_game.blit(s_whole_game, (0, y_whole_on_visible_game))
        screen.blit(s_visible_game, (x_right, y_s_visible_game))
        r_slider = pygame.Rect(x__, y__, w__, h__)
        pygame.draw.rect(screen, background, r_scroll_bar)
        pygame.draw.rect(screen, (32, 32, 32), r_slider)
    else:
        s_visible_game.blit(s_whole_game, (0, y_whole_on_visible_game))
        screen.blit(s_visible_game, (x_right, y_s_visible_game))


########################################################################################################################
# functions to realize button use


def b_white_use():
    if gss.white_human:
        gss.white_human = False
        b_white.set_text("Weiß: Computer")
    else:
        gss.white_human = True
        b_white.set_text("Weiß: Mensch")


def b_black_use():
    if gss.black_human:
        gss.black_human = False
        b_black.set_text("Schwarz: Computer")
    else:
        gss.black_human = True
        b_black.set_text("Schwarz: Mensch")


def b_rotate_use():
    global board_from_white_players_perspective
    board_from_white_players_perspective = not board_from_white_players_perspective
    draw_squares()
    for white_piece in gss.pieces[True]:
        draw_piece(white_piece)
    for black_piece in gss.pieces[False]:
        draw_piece(black_piece)


def b_new_game_use():
    board.clear_board()
    reset_and_draw_pieces()
    gss.new_game()
    pygame.draw.rect(screen, background, r_end_of_game_message)
    gss.reset_legal_moves()
    global x_executed_move
    global y_executed_move
    global s_whole_game
    global s_visible_game
    global y_s_whole_game
    global y_s_visible_game
    global y_whole_on_visible_game
    global r_scroll_bar
    x_executed_move = x_executed_move_left
    y_executed_move = square_size / 8
    s_whole_game, y_s_whole_game = set_surface(1, 14.5)
    s_visible_game, y_s_visible_game = set_surface(1, 15)
    y_whole_on_visible_game = 0
    x__ = screen.get_width() - 3 * x_left
    y__ = y_s_visible_game + x_left
    w__ = x_left
    h__ = s_visible_game.get_height() - 2 * x_left
    r_scroll_bar = pygame.Rect(x__, y__, w__, h__)


########################################################################################################################
# draw functions


def reset_and_draw_pieces():
    if not pieces.img_right_sized:
        pieces.resize_img(square_size)
    pieces.reset_pieces()
    for white_piece in gss.pieces[True]:
        draw_piece(white_piece)
    for black_piece in gss.pieces[False]:
        draw_piece(black_piece)


def draw_squares():
    for r_ in range(8):
        for c_ in range(8):
            if (r_ + c_) % 2 == 0:
                pygame.draw.rect(screen, light, square_rects[r_][c_])
            else:
                pygame.draw.rect(screen, dark, square_rects[r_][c_])
    if gss.giving_check:
        checked_king = gss.pieces[gss.whites_turn][0]
        r_ = checked_king.row
        c_ = checked_king.col
        if not board_from_white_players_perspective:
            r_ = 7 - r_
            c_ = 7 - c_
        draw = gss.draw_not_enough_material or gss.draw_position_repetition or gss.counter_no_pawn_no_capture == 50
        if len(gss.legal_moves) == 0 and not draw:
            pygame.draw.rect(screen, red_checkmate, square_rects[r_][c_])
        else:
            pygame.draw.rect(screen, red_check, square_rects[r_][c_])


def draw_piece(piece):
    row = piece.row
    col = piece.col
    if not board_from_white_players_perspective:
        row = 7 - row
        col = 7 - col
    x = board_x + col * square_size + (square_size - piece.img.get_width()) / 2
    y = board_y + row * square_size + (square_size - piece.img.get_height() - 4)
    screen.blit(piece.img, (x, y))


def draw_squares_and_pieces():
    draw_squares()
    for white_piece in gss.pieces[True]:
        draw_piece(white_piece)
    for black_piece in gss.pieces[False]:
        draw_piece(black_piece)


def draw_squares_and_pieces_except(exception):
    draw_squares()
    for white_piece in gss.pieces[True]:
        if white_piece != exception:
            draw_piece(white_piece)
    for black_piece in gss.pieces[False]:
        if black_piece != exception:
            draw_piece(black_piece)


def draw_selection(transformation_col):
    if board_from_white_players_perspective:
        c_ = transformation_col
    else:
        c_ = 7 - transformation_col
    whites_turn_and_perspective = gss.whites_turn and board_from_white_players_perspective
    blacks_turn_and_perspective = not gss.whites_turn and not board_from_white_players_perspective
    if whites_turn_and_perspective or blacks_turn_and_perspective:
        r_queen = 0
        r_rook = 1
        r_knight = 2
        r_bishop = 3
    else:
        r_queen = 7
        r_rook = 6
        r_knight = 5
        r_bishop = 4
    global square_queen
    global square_rook
    global square_knight
    global square_bishop
    square_queen = pygame.Rect(board_x + c_ * square_size, board_y + r_queen * square_size, square_size, square_size)
    square_rook = pygame.Rect(board_x + c_ * square_size, board_y + r_rook * square_size, square_size, square_size)
    square_knight = pygame.Rect(board_x + c_ * square_size, board_y + r_knight * square_size, square_size, square_size)
    square_bishop = pygame.Rect(board_x + c_ * square_size, board_y + r_bishop * square_size, square_size, square_size)
    pygame.draw.rect(screen, button_color, square_queen)
    pygame.draw.rect(screen, button_color, square_rook)
    pygame.draw.rect(screen, button_color, square_knight)
    pygame.draw.rect(screen, button_color, square_bishop)
    if gss.whites_turn:
        draw_img(r_queen, c_, pieces.img_w_queen)
        draw_img(r_rook, c_, pieces.img_w_rook)
        draw_img(r_knight, c_, pieces.img_w_knight)
        draw_img(r_bishop, c_, pieces.img_w_bishop)
    else:
        draw_img(r_queen, c_, pieces.img_b_queen)
        draw_img(r_rook, c_, pieces.img_b_rook)
        draw_img(r_knight, c_, pieces.img_b_knight)
        draw_img(r_bishop, c_, pieces.img_b_bishop)


def draw_img(r_img, c_img, img):
    x = board_x + c_img * square_size + (square_size - img.get_width()) / 2
    y = board_y + r_img * square_size + (square_size - img.get_height() - 4)
    screen.blit(img, (x, y))


def reset_str_executed_move(executed_move):
    global str_executed_move
    possible_notations = gss.move_to_notation[executed_move]
    str_executed_move = possible_notations[0]
    if len(possible_notations) > 1:
        for pn in possible_notations:
            if gss.notation_unic[pn]:
                str_executed_move = pn
                break
    if gss.whites_turn:
        if gss.giving_check:
            str_executed_move = str_executed_move + "+"
        gss.move_counter += 1
    else:
        if gss.move_counter < 10:
            str_executed_move = "  " + str(gss.move_counter) + ". " + str_executed_move
        elif gss.move_counter < 100:
            str_executed_move = " " + str(gss.move_counter) + ". " + str_executed_move
        else:
            str_executed_move = str(gss.move_counter) + ". " + str_executed_move
        if gss.giving_check:
            str_executed_move = str_executed_move + "+"
    gss.move_to_notation = {}
    gss.notation_unic = {}


def print_executed_move():
    global str_executed_move
    global x_executed_move
    global y_executed_move
    global s_whole_game
    global new_game_size

    if len(gss.legal_moves) == 0 and str_executed_move[-1] == "+":
        draw = gss.draw_not_enough_material or gss.draw_position_repetition or gss.counter_no_pawn_no_capture == 50
        if not draw:
            str_executed_move = str_executed_move[:-1] + "#"
    s_executed_move = font.render(str_executed_move, True, white)
    needed_height = y_executed_move + s_executed_move.get_height() + square_size / 8
    if needed_height > s_whole_game.get_height():
        s_new_size = pygame.Surface([s_whole_game.get_width(), needed_height])
        s_new_size.fill(button_color)
        s_new_size.blit(s_whole_game, [0, 0])
        s_new_size.blit(s_executed_move, [x_executed_move, y_executed_move])
        s_whole_game = s_new_size.copy()
        new_game_size = True
    else:
        s_whole_game.blit(s_executed_move, [x_executed_move, y_executed_move])
    if x_executed_move == x_executed_move_left:
        x_executed_move = x_executed_move_right
    else:
        x_executed_move = x_executed_move_left
        y_executed_move += square_size / 8


def set_end_of_game_message(case_end):
    global l_end_of_game_message
    global y_l_end_of_game_message
    match case_end:
        case "white_wins":
            text = "Schachmatt: Weiß gewinnt!"
            l_end_of_game_message, y_l_end_of_game_message = set_label(15, text, font)
        case "black_wins":
            text = "Schachmatt: Schwarz gewinnt!"
            l_end_of_game_message, y_l_end_of_game_message = set_label(15, text, font)
        case "patt":
            text = "Patt!"
            l_end_of_game_message, y_l_end_of_game_message = set_label(15, text, font)
        case "too_many_moves":
            text = "Remis: 50-Züge-Regel!"
            l_end_of_game_message, y_l_end_of_game_message = set_label(15, text, font)
        case "position_repetition":
            text = "Remis: dreifache Zugwiederholung!"
            l_end_of_game_message, y_l_end_of_game_message = set_label(15, text, font)
        case "material":
            text = "Remis: unzureichendes Material!"
            l_end_of_game_message, y_l_end_of_game_message = set_label(15, text, font)


def start_scrolling(y_mouse):
    global scrolling
    global y_mouse_when_scrolling_starts
    global y_slider_when_scrolling_starts
    scrolling = True
    y_mouse_when_scrolling_starts = y_mouse
    y_slider_when_scrolling_starts = r_slider.y
