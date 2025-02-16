import board

########################################################################################################################
# Einstellungen

white_human = True
black_human = True

########################################################################################################################
# Zustände

whites_turn = True
move_counter = 1
legal_moves = []                # Liste aller ausführbaren Züge
giving_check = False            # gibt an, ob durch den letzten Zug ein Schach gegeben wurde
squares_to_break_check = []     # Liste aller Felder, durch die ein Schach mittels "Dazwischenziehen" aufgehoben werden
castling_possible = {
    True: {
        "00": True, "000": True
    },
    False: {
        "00": True, "000": True
    }
}
pieces = {True: [], False: []}  # weiße und schwarze Figuren
pinning_candidates = {          # Figuren, die sich in der gleichen Reihe, Linie oder Diagonale wie der gegnerische
    True: {                     # König befinden und sich in die entsprechende Richtung bewegen können.
        "above": [],            # True: weiße Figuren, False: schwarze Figuren
        "right_above": [],
        "right": [],
        "right_below": [],
        "below": [],
        "left_below": [],
        "left": [],
        "left_above": []
    },
    False: {
        "above": [],
        "right_above": [],
        "right": [],
        "right_below": [],
        "below": [],
        "left_below": [],
        "left": [],
        "left_above": []
    }
}
possible_en_passant_moves = []
possible_pawn_transformations = []
history_1 = []          # Verlauf aller Stellungen, die einmal aufgetreten sind und erneut auftreten können
history_2 = []          # Verlauf aller Stellungen, die bereits zweimal aufgetreten sind und erneut auftreten können
draw_position_repetition = False    # Spielende durch dreifache Zugwiederholung
draw_not_enough_material = False    # Spielende durch zu wenig Material
counter_no_pawn_no_capture = 0      # Zähler für die 50-Zug-Regel
rank = {0: "8", 1: "7", 2: "6", 3: "5", 4: "4", 5: "3", 6: "2", 7: "1"}
file = {0: "a", 1: "b", 2: "c", 3: "d", 4: "e", 5: "f", 6: "g", 7: "h"}
move_to_notation = {}
notation_unic = {}


########################################################################################################################
# Updates


def update_castling_right(square_where_rook_starts_game: tuple):
    """
    Aktualisiert die Rochaderechte basierend auf der Startposition des Turms.
    """
    match square_where_rook_starts_game:
        case (0, 0):
            castling_possible[False]["000"] = False
        case (0, 7):
            castling_possible[False]["00"] = False
        case (7, 0):
            castling_possible[True]["000"] = False
        case (7, 7):
            castling_possible[True]["00"] = False


def update_giving_check_and_squares_to_break_check_by_deduction(squares_to_break_deduction_check: list):
    """
    Diese Funktion wird ausschließlich dann aufgerufen, wenn durch eine entsprechende Funktion ein Abzugsschach erkannt
    wird. Sie behandelt zwei Fälle:

    1. **Doppelschach**: Falls eine vorherige Prüfung bereits ein direktes Schach erkannt hat, liegt ein Doppelschach
    vor. In diesem Fall gibt es keine Möglichkeit, das Schach durch Dazwischenziehen einer Figur zu unterbinden.

    2. **Einfaches Abzugsschach**: Die entsprechenden Parameter werden aktualisiert.
    """
    global giving_check
    global squares_to_break_check
    if giving_check:
        squares_to_break_check = []
    else:
        giving_check = True
        squares_to_break_check = squares_to_break_deduction_check


def update_possible_en_passant_moves(start_square: tuple, goal: tuple):
    """
    Diese Funktion wird aufgerufen, wenn ein Bauer zwei Felder nach vorne zieht, sodass ggf. ein en Passant möglich ist.
    Die benötigten Informationen, um zu beurteilen, ob im nächsten Zug ein en Passant möglich ist, werden an die
    entsprechende Funktion weitergegeben.
    """
    if start_square[0] == goal[0] - 2:      # schwarzer Bauer zieht zwei Felder vor
        en_passant_r = goal[0]              # neue Reihe des Bauers
        en_passant_c = goal[1] - 1          # Linie neben dem Bauer
        update_possible_en_passant_moves_black_pawn_moved(en_passant_r, en_passant_c, goal)
        en_passant_c = goal[1] + 1          # Linie neben dem Bauer
        update_possible_en_passant_moves_black_pawn_moved(en_passant_r, en_passant_c, goal)
    elif start_square[0] == goal[0] + 2:    # weißer Bauer zieht zwei Felder vor
        en_passant_r = goal[0]              # neue Reihe des Bauers
        en_passant_c = goal[1] - 1          # Linie neben dem Bauer
        update_possible_en_passant_moves_white_pawn_moved(en_passant_r, en_passant_c, goal)
        en_passant_c = goal[1] + 1          # Linie neben dem Bauer
        update_possible_en_passant_moves_white_pawn_moved(en_passant_r, en_passant_c, goal)


def update_possible_en_passant_moves_black_pawn_moved(en_passant_r: int, en_passant_c: int, goal: tuple):
    """
    Die Funktion prüft, ob ein weißer Bauer auf dem richtigen Feld steht, um im nächsten Zug en Passant schlagen zu
    können. Ist dies der Fall, wird der Zug gespeichert.
    """
    if board.on_board(en_passant_r, en_passant_c) and not board.is_empty(en_passant_r, en_passant_c):
        en_passant_piece = board.squares[en_passant_r][en_passant_c].piece
        if en_passant_piece.color and en_passant_piece.get_type() == "Pawn":
            possible_en_passant_moves.append(((en_passant_r, en_passant_c), (goal[0] - 1, goal[1])))


def update_possible_en_passant_moves_white_pawn_moved(en_passant_r: int, en_passant_c: int, goal: tuple):
    """
    Die Funktion prüft, ob ein schwarzer Bauer auf dem richtigen Feld steht, um im nächsten Zug en Passant schlagen zu
    können. Ist dies der Fall, wird der Zug gespeichert.
    """
    if board.on_board(en_passant_r, en_passant_c) and not board.is_empty(en_passant_r, en_passant_c):
        en_passant_piece = board.squares[en_passant_r][en_passant_c].piece
        if (not en_passant_piece.color) and en_passant_piece.get_type() == "Pawn":
            possible_en_passant_moves.append(((en_passant_r, en_passant_c), (goal[0] + 1, goal[1])))


def new_game():
    """
    Setzt alle notwendigen Variablen zurück, um ein neues Spiel zu starten.
    """
    global whites_turn
    global legal_moves
    global giving_check
    global squares_to_break_check
    global possible_en_passant_moves
    global possible_pawn_transformations
    global move_counter
    global counter_no_pawn_no_capture
    global draw_position_repetition
    global draw_not_enough_material
    whites_turn = True
    reset_legal_moves()
    giving_check = False
    squares_to_break_check = []
    possible_en_passant_moves = []
    possible_pawn_transformations = []
    castling_possible[True]["00"] = True
    castling_possible[True]["000"] = True
    castling_possible[False]["00"] = True
    castling_possible[False]["000"] = True
    for key in pinning_candidates[True]:
        pinning_candidates[True][key] = []
        pinning_candidates[False][key] = []
    move_counter = 1
    counter_no_pawn_no_capture = 0
    draw_position_repetition = False
    draw_not_enough_material = False
    clear_history()
    update_history()


def reset_legal_moves():
    """
    Die Funktion wird nach jedem Zug aufgerufen und sammelt alle Züge, die der nun ziehende Spieler ausführen darf.
    """
    global legal_moves
    global possible_pawn_transformations
    legal_moves = []
    possible_pawn_transformations = []
    if giving_check:
        legal_moves = pieces[whites_turn][0].get_legal_moves()
        if len(squares_to_break_check) > 0:
            for movable_piece in pieces[whites_turn]:
                for move in movable_piece.get_legal_moves():
                    if move[1] in squares_to_break_check:
                        legal_moves.append(move)
    else:
        for movable_piece in pieces[whites_turn]:
            legal_moves += movable_piece.get_legal_moves()


def clear_history():
    """
    Wird aufgerufen, wenn ein neues Spiel beginnt oder ein Bauern- oder Schlagzug ausgeführt wurde.
    """
    global history_1
    global history_2
    history_1 = []
    history_2 = []


def update_history():
    """
    Aktualisiert die Spielverlauf-Listen anhand der aktuellen Stellung.
    """
    global draw_position_repetition
    position = board.board_to_str()
    if position in history_2:
        draw_position_repetition = True
    elif position in history_1:
        history_1.remove(position)
        history_2.append(position)
    else:
        history_1.append(position)
