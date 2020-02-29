#Tic Tac Toe in Pygame
#created by Inle Bush

import pygame, sys, copy, time
from pygame.locals import *
from random import randint
from definitions import *


def main():
    pygame.init()

    while True:
        settings = Settings() #initializes settings

        #Initializes variables
        mousex = 0
        mousey = 0 
        game_running = True

        screen = pygame.display.set_mode((settings.window_width, settings.window_height))
        pygame.display.set_caption("Tic-Tac-Toe")
        
        game_board = game_array(settings.num_rect) #make initial game board

        game_ai = ai(settings.num_rect, settings.player1_move, 0, "medium")#initiaizes game ai
        player = 1
        move_count = 1

        settings.draw_board(game_board.board, screen)
        pygame.display.flip()

        #creates objects with text class
        score_text = text("Current Player: Red", settings.default_font_size, settings.dark_blue, screen) #score rect
        winner = text("Filler", settings.default_font_size, settings.dark_blue, screen) #score rect
        title = text("Tic-Tac-Toe", settings.default_font_size, settings.dark_blue, screen) #title rect
        restart_game = text("Restart Game", settings.default_font_size, settings.dark_blue, screen) #restart button

        #Main Loop
        while game_running:
            mouse_clicked = False
                
            

            if player != game_ai.ai_player: #Only looks for mouse clicks when it is the players turn
                #runs through events
                for event in pygame.event.get(): 
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        sys.exit()

                    elif event.type == MOUSEBUTTONUP:
                        mousex, mousey = event.pos
                        mouse_clicked = True

                if mouse_clicked:
                    boxx, boxy = settings.get_box_at_pixel(mousex, mousey)
                    if boxx != None and boxy != None: #checks if click was in a rectangle
                        if game_board.check_move_valid(boxx, boxy):
                            game_board.change_rect_status(player, boxx, boxy)
                            move_count += 1 #increases move count
                            game_running = game_board.check_game_running(player, move_count)#checks game running

            else:
                time.sleep(0.2) #waits while ai makes move
                game_ai.make_move(game_board, move_count) #ai makes move
                move_count += 1 #increases move count
                game_running = game_board.check_game_running(player, move_count)#checks game running

            #switches player at end of turn
            if move_count % 2 == 1:
                player = 1
                current_player = 'Red'
                score_text.color = settings.red
            else:
                player = 2
                current_player = 'Blue'
                score_text.color = settings.blue

            settings.draw_board(game_board.board, screen)

            score_text.characters = "Current Player: " + current_player

            #displays score text in the center of the top margin and in the 
            score_text.right_display_rectangle(settings.window_width - settings.margin_width, settings.top_margin_height/2)
            title.left_display_rectangle(settings.margin_width, settings.top_margin_height / 2)

            pygame.display.flip() 
        
        #creates display
        settings.draw_board(game_board.board, screen)

        #creates text box at top
        restart_game.left_display_rectangle(settings.margin_width, settings.top_margin_height / 2)
        pygame.display.flip() 

        restart_game_rectangle = restart_game.left_return_rectangle(settings.margin_width, settings.top_margin_height / 2)

        while not game_running: #Lets window run until player closes
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                elif event.type == MOUSEBUTTONUP:
                    mousex, mousey = event.pos
                    mouse_clicked = True
            if restart_game_rectangle.collidepoint(mousex, mousey):
                game_running = True

if __name__ == "__main__":
    main()