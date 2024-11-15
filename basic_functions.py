import board


def on_board(r_considered: int, c_considered: int) -> bool:
    return 0 <= r_considered <= 7 and 0 <= c_considered <= 7


def is_empty(r_considered: int, c_considered: int) -> bool:
    return board.squares[r_considered][c_considered].piece is None


def has_enemy_piece(r_considered: int, c_considered: int, own_color: bool) -> bool:
    return board.squares[r_considered][c_considered].piece.color is not own_color
