import pygame, copy
from random import randint

class Settings:
    def __init__(self):#initialize settings

        self.window_width = 640 #width of window
        self.window_height = 675 #height of window
        self.top_margin_height = 50 #Size of y margin
        self.bottom_margin_height = 25
        self.margin_width = 20 #Size of x margin
        self.gap_size = 2 #Space between rectangles
        self.game_running = True

        self.default_font_size = self.top_margin_height * 3/5

        self.num_rect = 3 #x and y number of squares in board

        self.board_width = self.window_width - 2 * self.margin_width #pixel width of board
        self.board_height = self.window_height - (self.top_margin_height + self.bottom_margin_height)#pixel height of board

        self.box_width = (self.board_width - self.gap_size * (self.num_rect - 1))/self.num_rect #box height
        self.box_height = (self.board_height - self.gap_size * (self.num_rect - 1))/self.num_rect #box width

        self.player1_move = 5 #Infected plaer number of moves per turn
        self.player2_move = 7 #Uninfected player number of moves per turn

        self.white = (255, 255, 255) #colors used
        self.gray = (199, 199, 199) #May need to change
        self.blue = (64, 133, 198)
        self.red = (240, 79, 69)
        self.dark_blue = (20, 54, 86)

        #game colors
        self.bg_color = self.gray
        self.empty_color = self.dark_blue
        self.infected_color = self.red
        self.uninfected_color = self.blue

    def left_top_coords_of_box(self, boxx,boxy):
        '''converts board coordinates to pixel coordinates'''
        left = (boxx) * (self.box_width + self.gap_size) + self.margin_width #formula for finding left of box
        top = (boxy) * (self.box_height + self.gap_size) + self.top_margin_height #formula for finding top of box
        return left, top

    def get_box_at_pixel(self, x, y):
        for boxx in range (self.num_rect + 1):
            for boxy in range (self.num_rect + 1):
                left, top = self.left_top_coords_of_box(boxx, boxy)
                box_rect = pygame.Rect(left, top, self.box_width, self.box_height) #runs through all rectanglas
                if box_rect.collidepoint(x,y): #tests if box is in box_rect
                    return (boxx, boxy)#coord of box
        return (None, None) #returns none,none if no 

    def draw_board(self, board, screen): 
        '''resets screen with new board'''

        screen.fill(self.bg_color)
        for boxx in range (self.num_rect):
            for boxy in range (self.num_rect):
                left, top = self.left_top_coords_of_box(boxx, boxy) #I don't know why this works but it works
                if board[boxy][boxx] == 0:
                    pygame.draw.rect(screen, self.empty_color,(left, top, self.box_width, self.box_height)) #draws empty boxes
                elif board[boxy][boxx] == 1:
                    pygame.draw.rect(screen, self.infected_color,(left, top, self.box_width, self.box_height)) #draws infected boxes
                elif board[boxy][boxx] == 2:
                    pygame.draw.rect(screen, self.uninfected_color,(left, top, self.box_width, self.box_height)) 


class game_array:
    def __init__(self, array_length):

        self.array_length = array_length

        self.board = [[0,0,0],[0,0,0],[0,0,0]]

    def change_rect_status(self, status, boxx, boxy): 
        '''changes the value in an entry in self.board'''

        self.board[boxy][boxx] = status

    def check_move_valid(self, valid_boxx, valid_boxy): 
        '''validates a move'''
    
        if self.board[valid_boxy][valid_boxx] == 0:
            return True
        return False

    def check_game_running(self, player, move_count): 
        '''Checks if game is running, returns True if running, False if not'''
        
        
        #Checks for filled rows
        for row in range(self.array_length):
            for column in range(3):
                if self.board[row][column] != player:
                    break
                elif column ==2:
                    return False

        #checks for filled columns
        for column in range(3):
            for row in range(3):
                if self.board[row][column] != player:
                    break
                elif row == 2:
                    return False

        #Checks diagonal from top left to bottom right
        for value in range(3):
            if self.board[value][value] != player:
                break
            elif value == 2:
                return False

        #Checks diagonal from top right to bottom left   
        for value in range(3):
            if self.board[value][2 - value] != player:
                break
            elif value == 2:
                return False
        #If board is filled, game ends
        if move_count == 10:
            return False

        return True


class text: #used for all text boxes
    def __init__(self, characters, text_size, color, screen, font = "freesansbold.ttf"):
        '''initializes object in text class'''
        self.characters = characters
        self.text_size = round(text_size)
        self.color = color
        self.screen = screen
        self.font = font

    def right_display_rectangle(self, x_right, y_cent):
        '''creates and displays text on screen'''
        
        font = pygame.font.Font(self.font, self.text_size) #creates a font object
        
        text_object = font.render(self.characters, True, self.color) #creates a text surface object

        rectangle = text_object.get_rect()

        #sets coordinates of rectangle based off of left side and height center
        rectangle.right = x_right
        rectangle.centery = y_cent

        self.screen.blit(text_object, rectangle)

    def left_display_rectangle(self, x_left, y_cent):
        '''creates and displays text on screen'''
        
        font = pygame.font.Font(self.font, self.text_size) #creates a font object
        
        text_object = font.render(self.characters, True, self.color) #creates a text surface object

        rectangle = text_object.get_rect()

        #sets coordinates of rectangle based off of left side and height center
        rectangle.left = x_left
        rectangle.centery = y_cent

        self.screen.blit(text_object, rectangle)

    def left_return_rectangle(self,x_left,y_cent):
        '''returns rectangle based on left,center coordinates'''
        font = pygame.font.Font(self.font, self.text_size) #creates a font object
        
        text_object = font.render(self.characters, True, self.color) #creates a text surface object

        rectangle = text_object.get_rect()

        #sets coordinates of rectangle based off of left side and height center
        rectangle.left = x_left
        rectangle.centery = y_cent

        return rectangle

    
        

class ai:
    def __init__(self, num_rect, player1_move, ai_player = 0, level = "easy"):
        '''initializes object in ai class'''
        self.ai_player = ai_player #Who the ai is playing (0:none(pvp),1:ai plaing infected player, 2:ai playing noninfected player)
        self.level = level #Level of ai (easy, medium, hard)
        self.num_rect = num_rect
        self.player1_move = player1_move
        
    def player1_easy(self, board, move_count):
        '''Picks a random move from an array of valid moves'''
        if move_count == 1: #If it is the first move, ai takes move in center
            column = round(self.num_rect / 2)
            return column, column
    
       #initializes move array
        move_array = board.valid_move_array(1, move_count, self.player1_move)
        
        valid_move_number = 0 #Initializes value containing number of valid moves

        for row in move_array:# Sums all valid moves in move_array
            valid_move_number = valid_move_number + row.count(1)
        
        random_index = randint(1,valid_move_number) #gets random move number
        
        current_index = 0 #initializes current index to count valid move positions

        #iterates through valid moves while increasing the corresponding index until the index is equal to the random index
        for row in range(1, self.num_rect + 1): 
            for column in range(1, self.num_rect + 1):
                if move_array[row][column] == 1: #if move is valid
                    current_index += 1 #increase current number
                    if current_index == random_index: #if this matches with the random number generator
                        return(column, row) #return the row and column of the chosen number 

    def player2_easy(self, board, move_count):
        '''Picks a random move from an array of valid moves'''
        if move_count == self.player1_move + 1: #On the noninfected player's first move, picks a random rectangle adjacent to a infected square
            return self.player1_easy(board, 2) 
       
       #initializes move array
        move_array = board.valid_move_array(2, move_count, self.player1_move)
        
        valid_move_number = 0 #Initializes value containing number of valid moves

        for row in move_array:# Sums all valid moves in move_array
            valid_move_number = valid_move_number + row.count(1)
        
        random_index = randint(1, valid_move_number) #gets random move number
        
        current_index = 0 #initializes current index to count valid move positions

        #iterates through valid moves while increasing the corresponding index until the index is equal to the random index
        for row in range(1, self.num_rect + 1): 
            for column in range(1, self.num_rect + 1):
                if move_array[row][column] == 1: #if move is valid
                    current_index += 1 #increase current number
                    if current_index == random_index: #if this matches with the random number generator
                        return(column, row) #return the row and column of the chosen number 

    def player1_medium(self):
        '''ranks moves based on their distance from the center and x'''

    def player2_medium(self, board, move_count):
        '''ranks moves based on their distance from the center and the nearest infected square'''
        
        move_array = board.valid_move_array(2, move_count, self.player1_move)

        rank_table = copy.deepcopy(board.board_setup)

        #Changes values of table containing the rankings of moves
        for row in range(1, self.num_rect + 1):#iterates through possible boxes
            for column in range(1, self.num_rect + 1):
                if move_array[row][column] == 1: #If it is a valid move
                    rank_table[row][column] = (((self.num_rect + 1)/2 - row)**2 + ((self.num_rect + 1)/2 - column)**2) ** 0.5 #Calculates distance to the center 
                    
                    #finds lowest distance 
                    lowest_dist = 10000 #initializes high lowest distance
                    for board_row in range(1, self.num_rect + 1):
                        for board_column in range(1, self.num_rect + 1):
                            if board.board[board_row][board_column] == 1:
                                dist_to_infected = ((row - board_row)**2 + ((column - board_column)**2)) ** 0.5
                                lowest_dist = min(lowest_dist, dist_to_infected) #compares current distance and previous distance
                    rank_table[row][column] = rank_table[row][column] + 1000*lowest_dist #adds lowest distance(weighted higher) to rank_table box
        
        #Finds lowest move
        lowest_ranking = 100000 #Initializes high lowest ranking
        for row in range(1, self.num_rect + 1):
            for column in range(1, self.num_rect + 1):
                if move_array[row][column] == 1:
                    if rank_table[row][column] < lowest_ranking:
                        best_move = (column, row)
                        lowest_ranking = rank_table[row][column]
        return best_move
                    
    def make_move(self, board, move_count):
        '''changes board'''
        if self.level == "easy":
            if self.ai_player == 1:
                boxx , boxy = self.player1_easy(board, move_count)
            else:
                boxx, boxy = self.player2_easy(board, move_count)
        elif self.level == "medium":
            if self.ai_player == 1:
                boxx, boxy = self.player1_medium(board, move_count)
            else:
                boxx, boxy = self.player2_medium(board, move_count)

        board.change_rect_status(self.ai_player, boxx, boxy) #change the status of the chosen box in the board