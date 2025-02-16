class Square:
    """
    Repräsentiert ein einzelnes Feld auf dem Schachbrett.
    Jedes Feld kann eine Schachfigur enthalten oder leer sein.
    """

    def __init__(self):
        self.piece = None  # Das Feld ist initial leer


# Initialisiere das Schachbrett als 8x8-Liste von Square-Objekten
squares = [[Square() for _ in range(8)] for _ in range(8)]


def clear_board():
    """
    Setzt das gesamte Schachbrett zurück, indem alle Figuren entfernt werden.
    """
    for row in squares:
        for square in row:
            square.piece = None


def board_to_str():
    """
    Gibt die aktuelle Stellung auf dem Brett als String zurück.

    - Leere Felder werden als "-" dargestellt.
    - Weiße Figuren werden durch Großbuchstaben dargestellt (K, Q, R, N, B, P).
    - Schwarze Figuren werden durch Kleinbuchstaben dargestellt (k, q, r, n, b, p).

    :return: String-Darstellung der aktuellen Stellung.
    """
    position = ""
    for row in squares:
        for square in row:
            piece = square.piece
            if piece is None:
                position += "-"
            else:
                symbol = {
                    "King": "K", "Queen": "Q", "Rook": "R", "Knight": "N", "Bishop": "B", "Pawn": "P"
                }.get(piece.get_type(), "?")
                position += symbol if piece.color else symbol.lower()
    return position


def on_board(r_considered: int, c_considered: int) -> bool:
    """
    Prüft, ob die angegebenen Koordinaten innerhalb des Schachbretts liegen.

    :param r_considered: Zeilenindex
    :param c_considered: Spaltenindex
    :return: True, wenn die Koordinaten gültig sind, sonst False.
    """
    return 0 <= r_considered <= 7 and 0 <= c_considered <= 7


def is_empty(r_considered: int, c_considered: int) -> bool:
    """
    Überprüft, ob das Feld an den angegebenen Koordinaten leer ist.

    :param r_considered: Zeilenindex
    :param c_considered: Spaltenindex
    :return: True, wenn das Feld leer ist, sonst False.
    """
    return squares[r_considered][c_considered].piece is None


def has_enemy_piece(r_considered: int, c_considered: int, own_color: bool) -> bool:
    """
    Überprüft, ob sich auf dem Feld eine gegnerische Figur befindet.

    :param r_considered: Zeilenindex
    :param c_considered: Spaltenindex
    :param own_color: Farbe der eigenen Figur (True für Weiß, False für Schwarz)
    :return: True, wenn auf dem Feld eine gegnerische Figur steht, sonst False.
    """
    piece = squares[r_considered][c_considered].piece
    return piece is not None and piece.color is not own_color
