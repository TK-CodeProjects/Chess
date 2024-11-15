import pygame
import board
import game_states_and_settings as gss
import get_moves as gm
import execute_moves as em

scale_factor = 0.38

########################################################################################################################
########################################################################################################################
# classes for each type of piece


class Piece:

    def __init__(self, color: bool, row: int, col: int, img_path: str):
        self.color = color     # True: white / False: black
        self.row = row
        self.col = col
        self.img = self.load_img(img_path)
        board.squares[row][col].piece = self

    def get_legal_moves(self) -> list:
        pass

    def execute_move(self, start: tuple, goal: tuple):
        gss.giving_check = False
        gss.squares_to_break_check = []
        gss.whites_turn = not gss.whites_turn

    def get_type(self) -> str:
        return self.__class__.__name__

    @staticmethod
    def load_img(img_path: str):
        try:
            img = pygame.image.load(img_path)
            width, height = img.get_size()
            new_width = int(width * scale_factor)
            new_height = int(height * scale_factor)
            img = pygame.transform.scale(img, (new_width, new_height))
            return img
        except pygame.error as e:
            print(f"Fehler beim Laden des Bildes {img_path}: {e}")
            return None


class King(Piece):

    def __init__(self, color: bool, row: int, col: int, img_path: str):
        super().__init__(color, row, col, img_path)

    def get_legal_moves(self) -> list:
        return gm.get_moves_king(self)

    def execute_move(self, start: tuple, goal: tuple):
        super().execute_move(start, goal)
        em.execute_move_king(self, start, goal)


class Queen(Piece):

    def __init__(self, color: bool, row: int, col: int, img_path: str):
        super().__init__(color, row, col, img_path)
        self.pinned_from = None

    def get_legal_moves(self) -> list:
        return gm.get_moves_queen(self)

    def execute_move(self, start: tuple, goal: tuple):
        super().execute_move(start, goal)
        em.execute_move_queen(self, start, goal)


class Rook(Piece):

    def __init__(self, color: bool, row: int, col: int, img_path: str):
        super().__init__(color, row, col, img_path)
        self.pinned_from = None

    def get_legal_moves(self) -> list:
        return gm.get_moves_rook(self)

    def execute_move(self, start: tuple, goal: tuple):
        super().execute_move(start, goal)
        em.execute_move_rook(self, start, goal)


class Knight(Piece):

    def __init__(self, color: bool, row: int, col: int, img_path: str):
        super().__init__(color, row, col, img_path)
        self.pinned_from = None

    def get_legal_moves(self) -> list:
        return gm.get_moves_knight(self)

    def execute_move(self, start: tuple, goal: tuple):
        super().execute_move(start, goal)
        em.execute_move_knight(self, start, goal)


class Bishop(Piece):

    def __init__(self, color: bool, row: int, col: int, img_path: str):
        super().__init__(color, row, col, img_path)
        self.pinned_from = None

    def get_legal_moves(self) -> list:
        return gm.get_moves_bishop(self)

    def execute_move(self, start: tuple, goal: tuple):
        super().execute_move(start, goal)
        em.execute_move_bishop(self, start, goal)


class Pawn(Piece):

    def __init__(self, color: bool, row: int, col: int, img_path: str):
        super().__init__(color, row, col, img_path)
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
                    new_queen = Queen(True, goal[0], goal[1], "Pieces/QueenW.png")
                else:
                    new_queen = Queen(False, goal[0], goal[1], "Pieces/QueenB.png")
                em.execute_transformation_to_queen(self, start, goal, new_queen)
            case "Rook":
                if start[1] != goal[1]:
                    em.clear(goal)
                if self.color:
                    new_rook = Rook(True, goal[0], goal[1], "Pieces/RookW.png")
                else:
                    new_rook = Rook(False, goal[0], goal[1], "Pieces/RookB.png")
                em.execute_transformation_to_rook(self, start, goal, new_rook)
            case "Knight":
                if start[1] != goal[1]:
                    em.clear(goal)
                if self.color:
                    new_knight = Knight(True, goal[0], goal[1], "Pieces/KnightW.png")
                else:
                    new_knight = Knight(False, goal[0], goal[1], "Pieces/KnightB.png")
                em.execute_transformation_to_knight(self, start, goal, new_knight)
            case "Bishop":
                if start[1] != goal[1]:
                    em.clear(goal)
                if self.color:
                    new_bishop = Bishop(True, goal[0], goal[1], "Pieces/BishopW.png")
                else:
                    new_bishop = Bishop(False, goal[0], goal[1], "Pieces/BishopB.png")
                em.execute_transformation_to_bishop(self, start, goal, new_bishop)


########################################################################################################################
########################################################################################################################
# create pieces to start a new game


def set_pieces():
    w_king = King(True, 7, 4, "Pieces/KingW.png")
    w_queen = Queen(True, 7, 3, "Pieces/QueenW.png")
    w_rook_l = Rook(True, 7, 0, "Pieces/RookW.png")
    w_rook_r = Rook(True, 7, 7, "Pieces/RookW.png")
    w_knight_l = Knight(True, 7, 1, "Pieces/KnightW.png")
    w_knight_r = Knight(True, 7, 6, "Pieces/KnightW.png")
    w_bishop_l = Bishop(True, 7, 2, "Pieces/BishopW.png")
    w_bishop_r = Bishop(True, 7, 5, "Pieces/BishopW.png")
    b_king = King(False, 0, 4, "Pieces/KingB.png")
    b_queen = Queen(False, 0, 3, "Pieces/QueenB.png")
    b_rook_l = Rook(False, 0, 0, "Pieces/RookB.png")
    b_rook_r = Rook(False, 0, 7, "Pieces/RookB.png")
    b_knight_l = Knight(False, 0, 1, "Pieces/KnightB.png")
    b_knight_r = Knight(False, 0, 6, "Pieces/KnightB.png")
    b_bishop_l = Bishop(False, 0, 2, "Pieces/BishopB.png")
    b_bishop_r = Bishop(False, 0, 5, "Pieces/BishopB.png")
    gss.pieces[True] = [w_king, w_queen, w_rook_l, w_rook_r, w_knight_l, w_knight_r, w_bishop_l, w_bishop_r]
    gss.pieces[False] = [b_king, b_queen, b_rook_l, b_rook_r, b_knight_l, b_knight_r, b_bishop_l, b_bishop_r]
    for c_ in range(8):
        gss.pieces[True].append(Pawn(True, 6, c_, "Pieces/PawnW.png"))
        gss.pieces[False].append(Pawn(False, 1, c_, "Pieces/PawnB.png"))
