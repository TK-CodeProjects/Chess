import board
import game_states_and_settings as gss

########################################################################################################################
########################################################################################################################
# Funktionen zum Testen, ob der ziehende König einen gegebenen Zug ausführen darf


def check_test(color: bool, r: int, c: int) -> bool:
    """
    Die Funktion wird aufgerufen, um zu prüfen, ob der ziehende Spieler den König auf das Feld (r, c) ziehen darf. Für
    jede gegnerische Figur wird dafür ein entsprechender Test durchgeführt bis entweder eine Schach-gebende Figur
    gefunden wurde oder alle Figuren getestet wurden.

    :param color: Farbe des ziehenden Königs
    :param r: Zeilenindex des Zielfelds
    :param c: Spaltenindex des Zielfelds
    :return: True, wenn der König nach dem eigenen Zug bedroht wäre, sonst False.
    """
    for enemy_piece in gss.pieces[not color]:
        if not (enemy_piece.row == r and enemy_piece.col == c):
            match enemy_piece.get_type():
                case "King":
                    if check_test_king(r, c, enemy_piece):
                        return True
                case "Queen":
                    if check_test_queen(r, c, enemy_piece):
                        return True
                case "Rook":
                    if check_test_rook(r, c, enemy_piece):
                        return True
                case "Knight":
                    if check_test_knight(r, c, enemy_piece):
                        return True
                case "Bishop":
                    if check_test_bishop(r, c, enemy_piece):
                        return True
                case "Pawn":
                    if check_test_pawn(r, c, enemy_piece):
                        return True
    return False


########################################################################################################################
# Funktionen zum Testen, ob der ziehende König einen gegebenen Zug ausführen darf - abhängig von der potenziell
# drohenden Figur


def check_test_king(r_king: int, c_king: int, enemy_king) -> bool:
    """
    Hilfsfunktion, um den obigen "check_test" durchzuführen. Sie prüft, ob der ziehende König durch den gegebenen Zug
    vom gegnerischen König bedroht werden würde.

    :param r_king: Zeilenindex des Zielfelds des ziehenden Königs
    :param c_king: Spaltenindex des Zielfelds des ziehenden Königs
    :param enemy_king: gegnerischer König
    :return: True, wenn der König nach dem eigenen Zug von der Figur "enemy_king" bedroht werden würde, sonst False
    """
    return (r_king - 1 <= enemy_king.row <= r_king + 1) and (c_king - 1 <= enemy_king.col <= c_king + 1)


def check_test_queen(r_king: int, c_king: int, enemy_queen) -> bool:
    """
    Hilfsfunktion, um den obigen "check_test" durchzuführen. Sie prüft, ob der ziehende König durch den gegebenen Zug
    von der gegnerischen Dame bedroht werden würde. Die Richtungen, aus denen der König angegriffen werden kann, werden
    dabei separat in den entsprechenden Unterfunktionen getestet.

    :param r_king: Zeilenindex des Zielfelds des ziehenden Königs
    :param c_king: Spaltenindex des Zielfelds des ziehenden Königs
    :param enemy_queen: gegnerische Dame
    :return: True, wenn der König nach dem eigenen Zug von der Figur "enemy_queen" bedroht werden würde, sonst False
    """
    if enemy_queen.row == r_king:
        return check_test_row(r_king, c_king, enemy_queen)
    if enemy_queen.col == c_king:
        return check_test_col(r_king, c_king, enemy_queen)
    if enemy_queen.row + enemy_queen.col == r_king + c_king:
        return check_test_diag_up(r_king, c_king, enemy_queen)
    if enemy_queen.row - enemy_queen.col == r_king - c_king:
        return check_test_diag_down(r_king, c_king, enemy_queen)
    return False


def check_test_rook(r_king: int, c_king: int, enemy_rook) -> bool:
    """
    Hilfsfunktion, um den obigen "check_test" durchzuführen. Sie prüft, ob der ziehende König durch den gegebenen Zug
    vom gegnerischen Turm bedroht werden würde. Die Richtungen, aus denen der König angegriffen werden kann, werden
    dabei separat in den entsprechenden Unterfunktionen getestet.

    :param r_king: Zeilenindex des Zielfelds des ziehenden Königs
    :param c_king: Spaltenindex des Zielfelds des ziehenden Königs
    :param enemy_rook: gegnerischer Turm
    :return: True, wenn der König nach dem eigenen Zug von der Figur "enemy_rook" bedroht werden würde, sonst False
    """
    if enemy_rook.row == r_king:
        return check_test_row(r_king, c_king, enemy_rook)
    if enemy_rook.col == c_king:
        return check_test_col(r_king, c_king, enemy_rook)
    return False


def check_test_knight(r_king: int, c_king: int, enemy_knight) -> bool:
    """
    Hilfsfunktion, um den obigen "check_test" durchzuführen. Sie prüft, ob der ziehende König durch den gegebenen Zug
    vom gegnerischen Springer bedroht werden würde.

    :param r_king: Zeilenindex des Zielfelds des ziehenden Königs
    :param c_king: Spaltenindex des Zielfelds des ziehenden Königs
    :param enemy_knight: gegnerischer Springer
    :return: True, wenn der König nach dem eigenen Zug von der Figur "enemy_knight" bedroht werden würde, sonst False
    """
    r1_c2 = enemy_knight.row in [r_king - 1, r_king + 1] and enemy_knight.col in [c_king - 2, c_king + 2]
    r2_c1 = enemy_knight.row in [r_king - 2, r_king + 2] and enemy_knight.col in [c_king - 1, c_king + 1]
    return r1_c2 or r2_c1


def check_test_bishop(r_king: int, c_king: int, enemy_bishop) -> bool:
    """
    Hilfsfunktion, um den obigen "check_test" durchzuführen. Sie prüft, ob der ziehende König durch den gegebenen Zug
    vom gegnerischen Läufer bedroht werden würde. Die Richtungen, aus denen der König angegriffen werden kann, werden
    dabei separat in den entsprechenden Unterfunktionen getestet.

    :param r_king: Zeilenindex des Zielfelds des ziehenden Königs
    :param c_king: Spaltenindex des Zielfelds des ziehenden Königs
    :param enemy_bishop: gegnerischer Läufer
    :return: True, wenn der König nach dem eigenen Zug von der Figur "enemy_bishop" bedroht werden würde, sonst False
    """
    if enemy_bishop.row + enemy_bishop.col == r_king + c_king:
        return check_test_diag_up(r_king, c_king, enemy_bishop)
    if enemy_bishop.row - enemy_bishop.col == r_king - c_king:
        return check_test_diag_down(r_king, c_king, enemy_bishop)
    return False


def check_test_pawn(r_king: int, c_king: int, enemy_pawn) -> bool:
    """
    Hilfsfunktion, um den obigen "check_test" durchzuführen. Sie prüft, ob der ziehende König durch den gegebenen Zug
    vom gegnerischen Bauern bedroht werden würde.

    :param r_king: Zeilenindex des Zielfelds des ziehenden Königs
    :param c_king: Spaltenindex des Zielfelds des ziehenden Königs
    :param enemy_pawn: gegnerischer Bauer
    :return: True, wenn der König nach dem eigenen Zug von der Figur "enemy_pawn" bedroht werden würde, sonst False
    """
    if enemy_pawn.color:
        return enemy_pawn.row == r_king + 1 and enemy_pawn.col in [c_king - 1, c_king + 1]
    return enemy_pawn.row == r_king - 1 and enemy_pawn.col in [c_king - 1, c_king + 1]


########################################################################################################################
# Funktionen zum Testen, ob der ziehende König einen gegebenen Zug ausführen darf - abhängig von der Richtung aus der
# eine potenzielle Drohung besteht


def check_test_row(r_king: int, c_king: int, enemy_piece) -> bool:
    """
    Die Funktion wird ausschließlich dann aufgerufen, wenn geprüft wird, ob der König des ziehenden Spielers das Feld
    (r_king, c_king) betreten kann (ohne dann im Schach zu stehen) und die gegnerische Figur "enemy_piece" sowohl
    auf der entsprechenden Reihe steht, als auch in der Lage ist sich entlang einer Reihe zu bewegen (Dame oder Turm).
    Sie prüft, ob alle Felder zwischen dem Zielfeld des Königs und der gegnerischen Figur frei sind, ohne dass eine
    blockierende Figur das Schach verhindern würde. Zu beachten ist, dass das aktuelle Feld des Königs als freies Feld
    gewertet werden muss.

    :param r_king: Zeilenindex des Zielfelds des ziehenden Königs
    :param c_king: Spaltenindex des Zielfelds des ziehenden Königs
    :param enemy_piece: gegnerische Figur
    :return: True, wenn der König nach dem eigenen Zug von der Figur "enemy_piece" bedroht werden würde, sonst False
    """
    c_too_small = min(c_king, enemy_piece.col)
    c_too_big = max(c_king, enemy_piece.col)
    for c_ in range(c_too_small + 1, c_too_big):
        if not board.is_empty(r_king, c_):
            blocking_piece = board.squares[r_king][c_].piece
            if blocking_piece.get_type() != "King" or blocking_piece.color == enemy_piece.color:
                return False
    return True


def check_test_col(r_king: int, c_king: int, enemy_piece) -> bool:
    """
    Die Funktion wird ausschließlich dann aufgerufen, wenn geprüft wird, ob der König des ziehenden Spielers das Feld
    (r_king, c_king) betreten kann (ohne dann im Schach zu stehen) und die gegnerische Figur "enemy_piece" sowohl
    auf der entsprechenden Linie steht, als auch in der Lage ist sich entlang einer Linie zu bewegen (Dame oder Turm).
    Sie prüft, ob alle Felder zwischen dem Zielfeld des Königs und der gegnerischen Figur frei sind, ohne dass eine
    blockierende Figur das Schach verhindern würde. Zu beachten ist, dass das aktuelle Feld des Königs als freies Feld
    gewertet werden muss.

    :param r_king: Zeilenindex des Zielfelds des ziehenden Königs
    :param c_king: Spaltenindex des Zielfelds des ziehenden Königs
    :param enemy_piece: gegnerische Figur
    :return: True, wenn der König nach dem eigenen Zug von der Figur "enemy_piece" bedroht werden würde, sonst False
    """
    r_too_small = min(r_king, enemy_piece.row)
    r_too_big = max(r_king, enemy_piece.row)
    for r_ in range(r_too_small + 1, r_too_big):
        if not board.is_empty(r_, c_king):
            blocking_piece = board.squares[r_][c_king].piece
            if blocking_piece.get_type() != "King" or blocking_piece.color == enemy_piece.color:
                return False
    return True


def check_test_diag_up(r_king: int, c_king: int, enemy_piece) -> bool:
    """
    Die Funktion wird ausschließlich dann aufgerufen, wenn geprüft wird, ob der König des ziehenden Spielers das Feld
    (r_king, c_king) betreten kann (ohne dann im Schach zu stehen) und die gegnerische Figur "enemy_piece" sowohl
    auf der entsprechenden Diagonalen steht (von links unten nach rechts oben), als auch in der Lage ist sich entlang
    einer Diagonalen zu bewegen (Dame oder Läufer). Sie prüft, ob alle Felder zwischen dem Zielfeld des Königs und der
    gegnerischen Figur frei sind, ohne dass eine blockierende Figur das Schach verhindern würde. Zu beachten ist, dass
    das aktuelle Feld des Königs als freies Feld gewertet werden muss.

    :param r_king: Zeilenindex des Zielfelds des ziehenden Königs
    :param c_king: Spaltenindex des Zielfelds des ziehenden Königs
    :param enemy_piece: gegnerische Figur
    :return: True, wenn der König nach dem eigenen Zug von der Figur "enemy_piece" bedroht werden würde, sonst False
    """
    r_ = min(r_king, enemy_piece.row) + 1
    c_ = max(c_king, enemy_piece.col) - 1
    r_too_big = max(r_king, enemy_piece.row)
    while r_ < r_too_big:
        if not board.is_empty(r_, c_):
            blocking_piece = board.squares[r_][c_].piece
            if blocking_piece.get_type() != "King" or blocking_piece.color == enemy_piece.color:
                return False
        r_ += 1
        c_ -= 1
    return True


def check_test_diag_down(r_king: int, c_king: int, enemy_piece) -> bool:
    """
    Die Funktion wird ausschließlich dann aufgerufen, wenn geprüft wird, ob der König des ziehenden Spielers das Feld
    (r_king, c_king) betreten kann (ohne dann im Schach zu stehen) und die gegnerische Figur "enemy_piece" sowohl
    auf der entsprechenden Diagonalen steht (von links oben nach rechts unten), als auch in der Lage ist sich entlang
    einer Diagonalen zu bewegen (Dame oder Läufer). Sie prüft, ob alle Felder zwischen dem Zielfeld des Königs und der
    gegnerischen Figur frei sind, ohne dass eine blockierende Figur das Schach verhindern würde. Zu beachten ist, dass
    das aktuelle Feld des Königs als freies Feld gewertet werden muss.

    :param r_king: Zeilenindex des Zielfelds des ziehenden Königs
    :param c_king: Spaltenindex des Zielfelds des ziehenden Königs
    :param enemy_piece: gegnerische Figur
    :return: True, wenn der König nach dem eigenen Zug von der Figur "enemy_piece" bedroht werden würde, sonst False
    """
    r_ = min(r_king, enemy_piece.row) + 1
    c_ = min(c_king, enemy_piece.col) + 1
    r_too_big = max(r_king, enemy_piece.row)
    while r_ < r_too_big:
        if not board.is_empty(r_, c_):
            blocking_piece = board.squares[r_][c_].piece
            if blocking_piece.get_type() != "King" or blocking_piece.color == enemy_piece.color:
                return False
        r_ += 1
        c_ += 1
    return True


########################################################################################################################
########################################################################################################################
# Funktionen zum Überprüfen, ob eine Figur mit ihrem Zug ein Schach gibt


def direct_check_test_queen(color: bool, goal: tuple):
    """
    Diese Funktion wird aufgerufen, wenn eine Dame der Farbe "color" auf das Feld "goal" gezogen wurde und prüft, ob
    durch den ausgeführten Zug ein Schach gegeben wird. Ist dies der Fall, werden der Bool "giving_check" und die Liste
    "squares_to_break_check" in der Datei "game_states_and_settings.py" entsprechend aktualisiert.
    Zunächst wird geprüft, ob der gegnerische König sich auf einem Feld befindet, dass durch eine Dame auf einem sonst
    leeren Brett von "goal" aus erreicht werden kann. Ob, die Felder zwischen "goal" und gegnerischem König tatsächlich
    frei sind, wird anschließend durch die entsprechende Unterfunktion geprüft - inklusive der ggf. notwendigen
    Aktualisierungen.

    :param color: Farbe der gezogenen Dame
    :param goal: Feld, auf dem die Dame platziert wurde
    """
    enemy_king = gss.pieces[not color][0]
    if goal[0] == enemy_king.row:
        direct_check_test_row(goal, enemy_king)
    elif goal[1] == enemy_king.col:
        direct_check_test_col(goal, enemy_king)
    elif goal[0] + goal[1] == enemy_king.row + enemy_king.col:
        direct_check_test_diag_up(goal, enemy_king)
    elif goal[0] - goal[1] == enemy_king.row - enemy_king.col:
        direct_check_test_diag_down(goal, enemy_king)


def direct_check_test_rook(color: bool, goal: tuple):
    """
    Diese Funktion wird aufgerufen, wenn ein Turm der Farbe "color" auf das Feld "goal" gezogen wurde und prüft, ob
    durch den ausgeführten Zug ein Schach gegeben wird. Ist dies der Fall, werden der Bool "giving_check" und die Liste
    "squares_to_break_check" in der Datei "game_states_and_settings.py" entsprechend aktualisiert.
    Zunächst wird geprüft, ob der gegnerische König sich auf einem Feld befindet, dass durch einen Turm auf einem sonst
    leeren Brett von "goal" aus erreicht werden kann. Ob, die Felder zwischen "goal" und gegnerischem König tatsächlich
    frei sind, wird anschließend durch die entsprechende Unterfunktion geprüft - inklusive der ggf. notwendigen
    Aktualisierungen.

    :param color: Farbe des gezogenen Turms
    :param goal: Feld, auf dem der Turm platziert wurde
    """
    enemy_king = gss.pieces[not color][0]
    if goal[0] == enemy_king.row:
        direct_check_test_row(goal, enemy_king)
    elif goal[1] == enemy_king.col:
        direct_check_test_col(goal, enemy_king)


def direct_check_test_knight(color: bool, goal: tuple):
    """
    Diese Funktion wird aufgerufen, wenn ein Springer der Farbe "color" auf das Feld "goal" gezogen wurde und prüft, ob
    durch den ausgeführten Zug ein Schach gegeben wird. Ist dies der Fall, werden der Bool "giving_check" und die Liste
    "squares_to_break_check" in der Datei "game_states_and_settings.py" entsprechend aktualisiert.

    :param color: Farbe des gezogenen Springers
    :param goal: Feld, auf dem der Springer platziert wurde
    """
    enemy_king = gss.pieces[not color][0]
    r1_c2 = enemy_king.row in [goal[0] - 1, goal[0] + 1] and enemy_king.col in [goal[1] - 2, goal[1] + 2]
    r2_c1 = enemy_king.row in [goal[0] - 2, goal[0] + 2] and enemy_king.col in [goal[1] - 1, goal[1] + 1]
    if r1_c2 or r2_c1:
        gss.giving_check = True
        gss.squares_to_break_check = [goal]


def direct_check_test_bishop(color: bool, goal: tuple):
    """
    Diese Funktion wird aufgerufen, wenn ein Läufer der Farbe "color" auf das Feld "goal" gezogen wurde und prüft, ob
    durch den ausgeführten Zug ein Schach gegeben wird. Ist dies der Fall, werden der Bool "giving_check" und die Liste
    "squares_to_break_check" in der Datei "game_states_and_settings.py" entsprechend aktualisiert.
    Zunächst wird geprüft, ob der gegnerische König sich auf einem Feld befindet, dass durch einen Läufer auf einem
    sonst leeren Brett von "goal" aus erreicht werden kann. Ob, die Felder zwischen "goal" und gegnerischem König
    tatsächlich frei sind, wird anschließend durch die entsprechende Unterfunktion geprüft - inklusive der ggf.
    notwendigen Aktualisierungen.

    :param color: Farbe des gezogenen Läufers
    :param goal: Feld, auf dem der Läufer platziert wurde
    """
    enemy_king = gss.pieces[not color][0]
    if goal[0] + goal[1] == enemy_king.row + enemy_king.col:
        direct_check_test_diag_up(goal, enemy_king)
    elif goal[0] - goal[1] == enemy_king.row - enemy_king.col:
        direct_check_test_diag_down(goal, enemy_king)


def direct_check_test_pawn(color: bool, goal: tuple):
    """
    Diese Funktion wird aufgerufen, wenn ein Bauer der Farbe "color" auf das Feld "goal" gezogen wurde und prüft, ob
    durch den ausgeführten Zug ein Schach gegeben wird. Ist dies der Fall, werden der Bool "giving_check" und die Liste
    "squares_to_break_check" in der Datei "game_states_and_settings.py" entsprechend aktualisiert.

    :param color: Farbe des gezogenen Bauern
    :param goal: Feld, auf dem der Bauer platziert wurde
    """
    enemy_king = gss.pieces[not color][0]
    if color:
        if enemy_king.row == goal[0] - 1 and enemy_king.col in [goal[1] - 1, goal[1] + 1]:
            gss.giving_check = True
            gss.squares_to_break_check = [goal]
    else:
        if enemy_king.row == goal[0] + 1 and enemy_king.col in [goal[1] - 1, goal[1] + 1]:
            gss.giving_check = True
            gss.squares_to_break_check = [goal]


def direct_check_test_row(goal: tuple, enemy_king):
    """
    Diese Funktion wird aufgerufen, wenn sich eine Figur, die sich entlang einer Reihe bewegen kann (Dame oder Turm)
    nach ihrem Zug in der gleichen Reihe, wie der gegnerische König befindet. Es wird geprüft, ob alle Felder zwischen
    Figur und König frei sind. Ist dies der Fall, wird durch den ausgeführten Zug ein Schach gegeben und der Bool
    "giving_check" und die Liste "squares_to_break_check" in der Datei "game_states_and_settings.py" werden entsprechend
    aktualisiert.

    :param goal: neues Feld der gezogenen Figur
    :param enemy_king: gegnerischer König
    """
    gss.giving_check = True
    gss.squares_to_break_check = [goal]
    c_too_small = min(goal[1], enemy_king.col)
    c_too_big = max(goal[1], enemy_king.col)
    for c_ in range(c_too_small + 1, c_too_big):
        if board.is_empty(goal[0], c_):
            gss.squares_to_break_check.append((goal[0], c_))
        else:
            gss.giving_check = False
            return


def direct_check_test_col(goal: tuple, enemy_king):
    """
    Diese Funktion wird aufgerufen, wenn sich eine Figur, die sich entlang einer Linie bewegen kann (Dame oder Turm)
    nach ihrem Zug in der gleichen Linie, wie der gegnerische König befindet. Es wird geprüft, ob alle Felder zwischen
    Figur und König frei sind. Ist dies der Fall, wird durch den ausgeführten Zug ein Schach gegeben und der Bool
    "giving_check" und die Liste "squares_to_break_check" in der Datei "game_states_and_settings.py" werden entsprechend
    aktualisiert.

    :param goal: neues Feld der gezogenen Figur
    :param enemy_king: gegnerischer König
    """
    gss.giving_check = True
    gss.squares_to_break_check = [goal]
    r_too_small = min(goal[0], enemy_king.row)
    r_too_big = max(goal[0], enemy_king.row)
    for r_ in range(r_too_small + 1, r_too_big):
        if board.is_empty(r_, goal[1]):
            gss.squares_to_break_check.append((r_, goal[1]))
        else:
            gss.giving_check = False
            return


def direct_check_test_diag_up(goal: tuple, enemy_king):
    """
    Diese Funktion wird aufgerufen, wenn sich eine Figur, die sich entlang einer Diagonalen bewegen kann (Dame oder
    Läufer) nach ihrem Zug auf der gleichen Diagonalen (von links unten nach rechts oben), wie der gegnerische König
    befindet. Es wird geprüft, ob alle Felder zwischen Figur und König frei sind. Ist dies der Fall, wird durch den
    ausgeführten Zug ein Schach gegeben und der Bool "giving_check" und die Liste "squares_to_break_check" in der Datei
    "game_states_and_settings.py" werden entsprechend aktualisiert.

    :param goal: neues Feld der gezogenen Figur
    :param enemy_king: gegnerischer König
    """
    gss.giving_check = True
    gss.squares_to_break_check = [goal]
    r_ = min(goal[0], enemy_king.row) + 1
    c_ = max(goal[1], enemy_king.col) - 1
    r_too_big = max(goal[0], enemy_king.row)
    while r_ < r_too_big:
        if board.is_empty(r_, c_):
            gss.squares_to_break_check.append((r_, c_))
            r_ += 1
            c_ -= 1
        else:
            gss.giving_check = False
            return


def direct_check_test_diag_down(goal: tuple, enemy_king):
    """
    Diese Funktion wird aufgerufen, wenn sich eine Figur, die sich entlang einer Diagonalen bewegen kann (Dame oder
    Läufer) nach ihrem Zug auf der gleichen Diagonalen (von links oben nach rechts unten), wie der gegnerische König
    befindet. Es wird geprüft, ob alle Felder zwischen Figur und König frei sind. Ist dies der Fall, wird durch den
    ausgeführten Zug ein Schach gegeben und der Bool "giving_check" und die Liste "squares_to_break_check" in der Datei
    "game_states_and_settings.py" werden entsprechend aktualisiert.

    :param goal: neues Feld der gezogenen Figur
    :param enemy_king: gegnerischer König
    """
    gss.giving_check = True
    gss.squares_to_break_check = [goal]
    r_ = min(goal[0], enemy_king.row) + 1
    c_ = min(goal[1], enemy_king.col) + 1
    r_too_big = max(goal[0], enemy_king.row)
    while r_ < r_too_big:
        if board.is_empty(r_, c_):
            gss.squares_to_break_check.append((r_, c_))
            r_ += 1
            c_ += 1
        else:
            gss.giving_check = False
            return


########################################################################################################################
########################################################################################################################
# Funktionen zum Überprüfen, ob durch einen gegebenen Zug ein Abzugsschach gegeben wird


def deduction_check_test(moved_piece_color: bool, start: tuple, goal: tuple):
    enemy_king = gss.pieces[not moved_piece_color][0]
    if start[0] == enemy_king.row and start[0] != goal[0]:
        deduction_check_test_row(moved_piece_color, start, enemy_king)
    elif start[1] == enemy_king.col and start[1] != goal[1]:
        deduction_check_test_col(moved_piece_color, start, enemy_king)
    else:
        start_up = start[0] + start[1]
        king_up = enemy_king.row + enemy_king.col
        goal_up = goal[0] + goal[1]
        start_down = start[0] - start[1]
        king_down = enemy_king.row - enemy_king.col
        goal_down = goal[0] - goal[1]
        if start_up == king_up and start_up != goal_up:
            deduction_check_test_diag_up(moved_piece_color, start, enemy_king)
        elif start_down == king_down and start_down != goal_down:
            deduction_check_test_diag_down(moved_piece_color, start, enemy_king)


def deduction_check_test_en_passant(moved_pawn_color: bool, start: tuple, goal: tuple):
    enemy_king = gss.pieces[not moved_pawn_color][0]
    captured_pawn_square = (start[0], goal[1])
    if captured_pawn_square[0] + captured_pawn_square[1] == enemy_king.row + enemy_king.col:
        deduction_check_test_diag_up(moved_pawn_color, captured_pawn_square, enemy_king)
    elif captured_pawn_square[0] - captured_pawn_square[1] == enemy_king.row - enemy_king.col:
        deduction_check_test_diag_up(moved_pawn_color, captured_pawn_square, enemy_king)


########################################################################################################################
# deduction check tests depending on location/direction


def deduction_check_test_row(moved_piece_color: bool, start: tuple, enemy_king):
    if start[1] < enemy_king.col:
        deduction_check_test_left(moved_piece_color, enemy_king)
    else:
        deduction_check_test_right(moved_piece_color, enemy_king)


def deduction_check_test_col(moved_piece_color: bool, start: tuple, enemy_king):
    if start[0] < enemy_king.row:
        deduction_check_test_above(moved_piece_color, enemy_king)
    else:
        deduction_check_test_below(moved_piece_color, enemy_king)


def deduction_check_test_diag_up(moved_piece_color: bool, start: tuple, enemy_king):
    if start[0] < enemy_king.row:
        deduction_check_test_right_above(moved_piece_color, enemy_king)
    else:
        deduction_check_test_left_below(moved_piece_color, enemy_king)


def deduction_check_test_diag_down(moved_piece_color: bool, start: tuple, enemy_king):
    if start[0] < enemy_king.row:
        deduction_check_test_left_above(moved_piece_color, enemy_king)
    else:
        deduction_check_test_right_below(moved_piece_color, enemy_king)


def deduction_check_test_above(moved_piece_color: bool, enemy_king):
    if len(gss.pinning_candidates[moved_piece_color]["above"]) > 0:
        maybe_check_giving_r = gss.pinning_candidates[moved_piece_color]["above"][0].row
        squares_to_break_deduction_check = [(maybe_check_giving_r, enemy_king.col)]
        for r_ in range(maybe_check_giving_r + 1, enemy_king.row):
            if board.is_empty(r_, enemy_king.col):
                squares_to_break_deduction_check.append((r_, enemy_king.col))
            else:
                return
        gss.update_giving_check_and_squares_to_break_check_by_deduction(squares_to_break_deduction_check)


def deduction_check_test_right(moved_piece_color: bool, enemy_king):
    if len(gss.pinning_candidates[moved_piece_color]["right"]) > 0:
        maybe_check_giving_c = gss.pinning_candidates[moved_piece_color]["right"][0].col
        squares_to_break_deduction_check = [(enemy_king.row, maybe_check_giving_c)]
        for c_ in range(enemy_king.col + 1, maybe_check_giving_c):
            if board.is_empty(enemy_king.row, c_):
                squares_to_break_deduction_check.append((enemy_king.row, c_))
            else:
                return
        gss.update_giving_check_and_squares_to_break_check_by_deduction(squares_to_break_deduction_check)


def deduction_check_test_below(moved_piece_color: bool, enemy_king):
    if len(gss.pinning_candidates[moved_piece_color]["below"]) > 0:
        maybe_check_giving_r = gss.pinning_candidates[moved_piece_color]["below"][0].row
        squares_to_break_deduction_check = [(maybe_check_giving_r, enemy_king.col)]
        for r_ in range(enemy_king.row + 1, maybe_check_giving_r):
            if board.is_empty(r_, enemy_king.col):
                squares_to_break_deduction_check.append((r_, enemy_king.col))
            else:
                return
        gss.update_giving_check_and_squares_to_break_check_by_deduction(squares_to_break_deduction_check)


def deduction_check_test_left(moved_piece_color: bool, enemy_king):
    if len(gss.pinning_candidates[moved_piece_color]["left"]) > 0:
        maybe_check_giving_c = gss.pinning_candidates[moved_piece_color]["left"][0].col
        squares_to_break_deduction_check = [(enemy_king.row, maybe_check_giving_c)]
        for c_ in range(maybe_check_giving_c + 1, enemy_king.col):
            if board.is_empty(enemy_king.row, c_):
                squares_to_break_deduction_check.append((enemy_king.row, c_))
            else:
                return
        gss.update_giving_check_and_squares_to_break_check_by_deduction(squares_to_break_deduction_check)


def deduction_check_test_right_above(moved_piece_color: bool, enemy_king):
    if len(gss.pinning_candidates[moved_piece_color]["right_above"]) > 0:
        r_ = gss.pinning_candidates[moved_piece_color]["right_above"][0].row
        c_ = gss.pinning_candidates[moved_piece_color]["right_above"][0].col
        squares_to_break_deduction_check = [(r_, c_)]
        r_ += 1
        c_ -= 1
        while r_ < enemy_king.row:
            if board.is_empty(r_, c_):
                squares_to_break_deduction_check.append((r_, c_))
                r_ += 1
                c_ -= 1
            else:
                return
        gss.update_giving_check_and_squares_to_break_check_by_deduction(squares_to_break_deduction_check)


def deduction_check_test_right_below(moved_piece_color: bool, enemy_king):
    if len(gss.pinning_candidates[moved_piece_color]["right_below"]) > 0:
        r_ = gss.pinning_candidates[moved_piece_color]["right_below"][0].row
        c_ = gss.pinning_candidates[moved_piece_color]["right_below"][0].col
        squares_to_break_deduction_check = [(r_, c_)]
        r_ -= 1
        c_ -= 1
        while r_ > enemy_king.row:
            if board.is_empty(r_, c_):
                squares_to_break_deduction_check.append((r_, c_))
                r_ -= 1
                c_ -= 1
            else:
                return
        gss.update_giving_check_and_squares_to_break_check_by_deduction(squares_to_break_deduction_check)


def deduction_check_test_left_below(moved_piece_color: bool, enemy_king):
    if len(gss.pinning_candidates[moved_piece_color]["left_below"]) > 0:
        r_ = gss.pinning_candidates[moved_piece_color]["left_below"][0].row
        c_ = gss.pinning_candidates[moved_piece_color]["left_below"][0].col
        squares_to_break_deduction_check = [(r_, c_)]
        r_ -= 1
        c_ += 1
        while r_ > enemy_king.row:
            if board.is_empty(r_, c_):
                squares_to_break_deduction_check.append((r_, c_))
                r_ -= 1
                c_ += 1
            else:
                return
        gss.update_giving_check_and_squares_to_break_check_by_deduction(squares_to_break_deduction_check)


def deduction_check_test_left_above(moved_piece_color: bool, enemy_king):
    if len(gss.pinning_candidates[moved_piece_color]["left_above"]) > 0:
        r_ = gss.pinning_candidates[moved_piece_color]["left_above"][0].row
        c_ = gss.pinning_candidates[moved_piece_color]["left_above"][0].col
        squares_to_break_deduction_check = [(r_, c_)]
        r_ += 1
        c_ += 1
        while r_ < enemy_king.row:
            if board.is_empty(r_, c_):
                squares_to_break_deduction_check.append((r_, c_))
                r_ += 1
                c_ += 1
            else:
                return
        gss.update_giving_check_and_squares_to_break_check_by_deduction(squares_to_break_deduction_check)
