import pygame
import random
import gui
import board
import game_states_and_settings as gss

clock = pygame.time.Clock()
running = True

gui.set_and_draw_pieces()
gss.reset_legal_moves()

grabbed = None

while running:

    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                if gui.b_white.rect.collidepoint(event.pos):
                    if gss.white_human:
                        gss.white_human = False
                        gui.b_white.set_text("Weiß: Computer")
                    else:
                        gss.white_human = True
                        gui.b_white.set_text("Weiß: Mensch")
                elif gui.b_black.rect.collidepoint(event.pos):
                    if gss.black_human:
                        gss.black_human = False
                        gui.b_black.set_text("Schwarz: Computer")
                    else:
                        gss.black_human = True
                        gui.b_black.set_text("Schwarz: Mensch")
                elif gui.b_rotate.rect.collidepoint(event.pos):
                    gui.rotate()
                elif gui.b_new_game.rect.collidepoint(event.pos):
                    board.clear_board()
                    gui.set_and_draw_pieces()
                    gss.new_game()
                    gss.reset_legal_moves()
                elif gui.b_exit.rect.collidepoint(event.pos):
                    running = False
                else:
                    if (gss.whites_turn and gss.white_human) or (not gss.whites_turn and gss.black_human):
                        grabbed = gui.grab_piece(event.pos)
        elif event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:
                if (gss.whites_turn and gss.white_human) or (not gss.whites_turn and gss.black_human):
                    if grabbed is not None:
                        release = gui.get_square(event.pos)
                        if release is not None:
                            tried_move = ((grabbed.row, grabbed.col), release)
                            if tried_move in gss.legal_moves:
                                gss.possible_en_passant_moves = []
                                grabbed.execute_move((grabbed.row, grabbed.col), release)
                                gss.reset_legal_moves()
                            elif tried_move in gss.possible_pawn_transformations:
                                gss.possible_en_passant_moves = []
                                grabbed.execute_transformation((grabbed.row, grabbed.col), release, "Queen")
                                gss.reset_legal_moves()

                        grabbed = None

    if (gss.whites_turn and not gss.white_human) or (not gss.whites_turn and not gss.black_human):
        for move in gss.possible_pawn_transformations:
            gss.legal_moves.append((move[0], move[1], "Queen"))
            gss.legal_moves.append((move[0], move[1], "Rook"))
            gss.legal_moves.append((move[0], move[1], "Knight"))
            gss.legal_moves.append((move[0], move[1], "Bishop"))
        if len(gss.legal_moves) > 0:
            gss.possible_en_passant_moves = []
            random_move = random.choice(gss.legal_moves)
            chosen_piece = board.squares[random_move[0][0]][random_move[0][1]].piece
            if len(random_move) == 2:
                chosen_piece.execute_move(random_move[0], random_move[1])
            else:
                chosen_piece.execute_transformation(random_move[0], random_move[1], random_move[2])
            gss.reset_legal_moves()

    gui.screen.fill(gui.background)
    gui.draw_buttons()
    gui.draw_squares_and_pieces(grabbed)
    if grabbed is not None:
        x, y = pygame.mouse.get_pos()
        gui.screen.blit(grabbed.img, (x, y))

    pygame.display.update()
    clock.tick(64)


pygame.quit()
