import pygame
import board
import game_states_and_settings as gss
import pieces

pygame.init()

background = (16, 16, 16)
button_color = (12, 12, 12)
font_color = (255, 255, 255)
light = (250, 240, 230)
dark = (205, 188, 174)
red_check = (255, 0, 0)
red_checkmate = (64, 0, 0)

font = pygame.font.SysFont("monospace", 16)

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


class Button:

    def __init__(self, x, y, w, h, text):
        self.rendered_text = font.render(text, True, font_color)
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.text_x = self.x + 0.5 * (self.w - self.rendered_text.get_width())
        self.text_y = self.y + 0.5 * (self.h - self.rendered_text.get_height())
        self.rect = pygame.Rect(x, y, w, h)

    def set_text(self, text):
        self.rendered_text = font.render(text, True, font_color)
        self.text_x = self.x + 0.5 * (self.w - self.rendered_text.get_width())
        self.text_y = self.y + 0.5 * (self.h - self.rendered_text.get_height())

    def draw(self):
        pygame.draw.rect(screen, button_color, self.rect)
        screen.blit(self.rendered_text, (self.text_x, self.text_y))


def draw_buttons():
    b_white.draw()
    b_black.draw()
    b_rotate.draw()
    b_new_game.draw()
    b_exit.draw()


x_ = board_x + 8.5 * square_size
y_ = square_size / 4
w_ = (screen.get_width() - 8 * square_size) / 2 - square_size
h_ = square_size / 2
b_white = Button(x_, y_, w_, h_, "Weiß: Mensch")
y_ += square_size
b_black = Button(x_, y_, w_, h_, "Schwarz: Mensch")
y_ += square_size
b_rotate = Button(x_, y_, w_, h_, "Brett drehen")
y_ += square_size
b_new_game = Button(x_, y_, w_, h_, "Neues Spiel")
y_ += square_size
b_exit = Button(x_, y_, w_, h_, "Beenden")
draw_buttons()

########################################################################################################################
########################################################################################################################
# functions


def set_and_draw_pieces():
    pieces.set_pieces()
    for white_piece in gss.pieces[True]:
        draw_piece(white_piece)
    for black_piece in gss.pieces[False]:
        draw_piece(black_piece)


def rotate():
    global board_from_white_players_perspective
    board_from_white_players_perspective = not board_from_white_players_perspective
    draw_squares()
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
        if len(gss.legal_moves) == 0:
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


def draw_squares_and_pieces(grabbed_piece):
    draw_squares()
    for white_piece in gss.pieces[True]:
        if white_piece != grabbed_piece:
            draw_piece(white_piece)
    for black_piece in gss.pieces[False]:
        if black_piece != grabbed_piece:
            draw_piece(black_piece)


def grab_piece(pos):
    for r_ in range(8):
        for c_ in range(8):
            if square_rects[r_][c_].collidepoint(pos):
                if board_from_white_players_perspective:
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
            if square_rects[r_][c_].collidepoint(pos):
                if board_from_white_players_perspective:
                    click_r = r_
                    click_c = c_
                else:
                    click_r = 7 - r_
                    click_c = 7 - c_
                return click_r, click_c
    return None
