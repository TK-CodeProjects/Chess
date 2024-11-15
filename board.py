class Square:

    def __init__(self):
        self.piece = None


squares = []
for r in range(8):
    row_of_squares = []
    for c in range(8):
        row_of_squares.append(Square())
    squares.append(row_of_squares)


def clear_board():
    for r_ in range(8):
        for c_ in range(8):
            squares[r_][c_].piece = None
