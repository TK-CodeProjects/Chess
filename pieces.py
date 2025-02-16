import pygame
import board
import game_states_and_settings as gss
import get_moves as gm
import execute_moves as em

########################################################################################################################
########################################################################################################################
# images

try:
    img_w_king = pygame.image.load("Pieces/KingW.png")
except pygame.error as e:
    print(f"Fehler beim Laden des Bildes {"Pieces/KingW.png"}: {e}")
try:
    img_w_queen = pygame.image.load("Pieces/QueenW.png")
except pygame.error as e:
    print(f"Fehler beim Laden des Bildes {"Pieces/QueenW.png"}: {e}")
try:
    img_w_rook = pygame.image.load("Pieces/RookW.png")
except pygame.error as e:
    print(f"Fehler beim Laden des Bildes {"Pieces/RookW.png"}: {e}")
try:
    img_w_knight = pygame.image.load("Pieces/KnightW.png")
except pygame.error as e:
    print(f"Fehler beim Laden des Bildes {"Pieces/KnightW.png"}: {e}")
try:
    img_w_bishop = pygame.image.load("Pieces/BishopW.png")
except pygame.error as e:
    print(f"Fehler beim Laden des Bildes {"Pieces/BishopW.png"}: {e}")
try:
    img_w_pawn = pygame.image.load("Pieces/PawnW.png")
except pygame.error as e:
    print(f"Fehler beim Laden des Bildes {"Pieces/PawnW.png"}: {e}")
try:
    img_b_king = pygame.image.load("Pieces/KingB.png")
except pygame.error as e:
    print(f"Fehler beim Laden des Bildes {"Pieces/KingB.png"}: {e}")
try:
    img_b_queen = pygame.image.load("Pieces/QueenB.png")
except pygame.error as e:
    print(f"Fehler beim Laden des Bildes {"Pieces/QueenB.png"}: {e}")
try:
    img_b_rook = pygame.image.load("Pieces/RookB.png")
except pygame.error as e:
    print(f"Fehler beim Laden des Bildes {"Pieces/RookB.png"}: {e}")
try:
    img_b_knight = pygame.image.load("Pieces/KnightB.png")
except pygame.error as e:
    print(f"Fehler beim Laden des Bildes {"Pieces/KnightB.png"}: {e}")
try:
    img_b_bishop = pygame.image.load("Pieces/BishopB.png")
except pygame.error as e:
    print(f"Fehler beim Laden des Bildes {"Pieces/BishopB.png"}: {e}")
try:
    img_b_pawn = pygame.image.load("Pieces/PawnB.png")
except pygame.error as e:
    print(f"Fehler beim Laden des Bildes {"Pieces/PawnB.png"}: {e}")

scale_factor = 1
img_right_sized = False


def resize_one_img(img):
    width, height = img.get_size()
    new_width = int(width * scale_factor)
    new_height = int(height * scale_factor)
    img = pygame.transform.scale(img, (new_width, new_height))
    return img


def resize_img(square_size):
    global scale_factor
    global img_right_sized
    global img_w_king
    global img_w_queen
    global img_w_rook
    global img_w_knight
    global img_w_bishop
    global img_w_pawn
    global img_b_king
    global img_b_queen
    global img_b_rook
    global img_b_knight
    global img_b_bishop
    global img_b_pawn
    scale_factor = square_size * 0.96 / img_w_king.get_height()
    img_w_king = resize_one_img(img_w_king)
    img_w_queen = resize_one_img(img_w_queen)
    img_w_rook = resize_one_img(img_w_rook)
    img_w_knight = resize_one_img(img_w_knight)
    img_w_bishop = resize_one_img(img_w_bishop)
    img_w_pawn = resize_one_img(img_w_pawn)
    img_b_king = resize_one_img(img_b_king)
    img_b_queen = resize_one_img(img_b_queen)
    img_b_rook = resize_one_img(img_b_rook)
    img_b_knight = resize_one_img(img_b_knight)
    img_b_bishop = resize_one_img(img_b_bishop)
    img_b_pawn = resize_one_img(img_b_pawn)
    img_right_sized = True


########################################################################################################################
########################################################################################################################
# classes for each type of piece


class Piece:

    def __init__(self, color: bool, row: int, col: int, img):
        self.color = color     # True: white / False: black
        self.row = row
        self.col = col
        self.img = img
        board.squares[row][col].piece = self

    def get_legal_moves(self) -> list:
        pass

    def execute_move(self, start: tuple, goal: tuple):
        gss.giving_check = False
        gss.squares_to_break_check = []
        gss.whites_turn = not gss.whites_turn

    def get_type(self) -> str:
        return self.__class__.__name__


class King(Piece):

    def __init__(self, color: bool, row: int, col: int, img):
        super().__init__(color, row, col, img)

    def get_legal_moves(self) -> list:
        return gm.get_moves_king(self)

    def execute_move(self, start: tuple, goal: tuple):
        super().execute_move(start, goal)
        em.execute_move_king(self, start, goal)


class Queen(Piece):

    def __init__(self, color: bool, row: int, col: int, img):
        super().__init__(color, row, col, img)
        self.pinned_from = None

    def get_legal_moves(self) -> list:
        return gm.get_moves_queen(self)

    def execute_move(self, start: tuple, goal: tuple):
        super().execute_move(start, goal)
        em.execute_move_queen(self, start, goal)


class Rook(Piece):

    def __init__(self, color: bool, row: int, col: int, img):
        super().__init__(color, row, col, img)
        self.pinned_from = None

    def get_legal_moves(self) -> list:
        return gm.get_moves_rook(self)

    def execute_move(self, start: tuple, goal: tuple):
        super().execute_move(start, goal)
        em.execute_move_rook(self, start, goal)


class Knight(Piece):

    def __init__(self, color: bool, row: int, col: int, img):
        super().__init__(color, row, col, img)
        self.pinned_from = None

    def get_legal_moves(self) -> list:
        return gm.get_moves_knight(self)

    def execute_move(self, start: tuple, goal: tuple):
        super().execute_move(start, goal)
        em.execute_move_knight(self, start, goal)


class Bishop(Piece):

    def __init__(self, color: bool, row: int, col: int, img):
        super().__init__(color, row, col, img)
        self.pinned_from = None

    def get_legal_moves(self) -> list:
        return gm.get_moves_bishop(self)

    def execute_move(self, start: tuple, goal: tuple):
        super().execute_move(start, goal)
        em.execute_move_bishop(self, start, goal)


class Pawn(Piece):

    def __init__(self, color: bool, row: int, col: int, img):
        super().__init__(color, row, col, img)
        self.has_moved = False
        self.pinned_from = None

    def get_legal_moves(self) -> list:
        return gm.get_moves_pawn(self)

    def execute_move(self, start: tuple, goal: tuple):
        super().execute_move(start, goal)
        em.execute_move_pawn(self, start, goal)

    def execute_transformation(self, start: tuple, goal: tuple, new_piece_type: str):
        super().execute_move(start, goal)
        match new_piece_type:
            case "Queen":
                if start[1] != goal[1]:
                    em.clear(goal)
                if self.color:
                    new_queen = Queen(True, goal[0], goal[1], img_w_queen)
                else:
                    new_queen = Queen(False, goal[0], goal[1], img_b_queen)
                em.execute_transformation_to_queen(self, start, goal, new_queen)
            case "Rook":
                if start[1] != goal[1]:
                    em.clear(goal)
                if self.color:
                    new_rook = Rook(True, goal[0], goal[1], img_w_rook)
                else:
                    new_rook = Rook(False, goal[0], goal[1], img_b_rook)
                em.execute_transformation_to_rook(self, start, goal, new_rook)
            case "Knight":
                if start[1] != goal[1]:
                    em.clear(goal)
                if self.color:
                    new_knight = Knight(True, goal[0], goal[1], img_w_knight)
                else:
                    new_knight = Knight(False, goal[0], goal[1], img_b_knight)
                em.execute_transformation_to_knight(self, start, goal, new_knight)
            case "Bishop":
                if start[1] != goal[1]:
                    em.clear(goal)
                if self.color:
                    new_bishop = Bishop(True, goal[0], goal[1], img_w_bishop)
                else:
                    new_bishop = Bishop(False, goal[0], goal[1], img_b_bishop)
                em.execute_transformation_to_bishop(self, start, goal, new_bishop)


########################################################################################################################
########################################################################################################################
# create pieces to start a new game


def reset_pieces():
    w_king = King(True, 7, 4, img_w_king)
    w_queen = Queen(True, 7, 3, img_w_queen)
    w_rook_l = Rook(True, 7, 0, img_w_rook)
    w_rook_r = Rook(True, 7, 7, img_w_rook)
    w_knight_l = Knight(True, 7, 1, img_w_knight)
    w_knight_r = Knight(True, 7, 6, img_w_knight)
    w_bishop_l = Bishop(True, 7, 2, img_w_bishop)
    w_bishop_r = Bishop(True, 7, 5, img_w_bishop)
    b_king = King(False, 0, 4, img_b_king)
    b_queen = Queen(False, 0, 3, img_b_queen)
    b_rook_l = Rook(False, 0, 0, img_b_rook)
    b_rook_r = Rook(False, 0, 7, img_b_rook)
    b_knight_l = Knight(False, 0, 1, img_b_knight)
    b_knight_r = Knight(False, 0, 6, img_b_knight)
    b_bishop_l = Bishop(False, 0, 2, img_b_bishop)
    b_bishop_r = Bishop(False, 0, 5, img_b_bishop)
    gss.pieces[True] = [w_king, w_queen, w_rook_l, w_rook_r, w_knight_l, w_knight_r, w_bishop_l, w_bishop_r]
    gss.pieces[False] = [b_king, b_queen, b_rook_l, b_rook_r, b_knight_l, b_knight_r, b_bishop_l, b_bishop_r]
    for c_ in range(8):
        gss.pieces[True].append(Pawn(True, 6, c_, img_w_pawn))
        gss.pieces[False].append(Pawn(False, 1, c_, img_b_pawn))
