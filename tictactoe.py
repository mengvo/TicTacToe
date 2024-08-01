# Mengzhen Vo

import pygame

pygame.init()

SCREEN_WIDTH = 300
SCREEN_HEIGHT = 300
x, y = (0, 0)
game_started, game_ended = False, False
x_turn = True

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Tic Tac Toe!")

# game grid
grid = [[None]*3 for i in range(3)]

# constants
O_COLOR = (39, 102, 219)
X_COLOR = (219, 39, 39)
BORDER_COLOR = (34, 37, 48)
BACKGROUND_COLOR = (201, 180, 171)
LINE_COLOR = (56, 54, 54)
LINE_WIDTH = 6
GREEN = (16, 232, 81)
RED = (232, 16, 16)
WHITE = (255, 255, 255)
TEXT_FONT = pygame.font.SysFont("Arial", 20)

# shape coordinates
y_coordinates = {}
y_coordinates["top_left"], y_coordinates["top_mid"], y_coordinates["top_right"] = (52, 52), (147, 52), (245, 52)
y_coordinates["mid_left"], y_coordinates["middle"], y_coordinates["mid_right"] = (52, 147), (147, 147), (245, 147)
y_coordinates["bot_left"], y_coordinates["bot_mid"], y_coordinates["bot_right"] = (52, 245), (147, 245), (245, 245)

x_coordinates = {} # [ (1st line), (2nd line) ]
x_coordinates["top_left"] = [((16, 16), (88, 88)), ((16, 88), (88, 16))]
x_coordinates["top_mid"] = [((114, 16), (186, 88)), ((114, 88), (186, 16))]
x_coordinates["top_right"] = [((212, 16), (284, 88)), ((212, 88), (284, 16))]
x_coordinates["mid_left"] = [((16, 114), (88, 186)), ((16, 186), (88, 114))]
x_coordinates["middle"] = [((114, 114), (186, 186)), ((114, 186), (186, 114))]
x_coordinates["mid_right"] = [((212, 114), (284, 186)), ((212, 186), (284, 114))]
x_coordinates["bot_left"] = [((16, 212), (88, 284)), ((16, 284), (88, 212))]
x_coordinates["bot_mid"] = [((114, 212), (186, 284)), ((114, 284), (186, 212))]
x_coordinates["bot_right"] = [((212, 212), (284, 284)), ((212, 284), (284, 212))]

def draw_o(screen, coordinate, color):
    pygame.draw.circle(screen, color, y_coordinates[coordinate], 40, 4)

def draw_x(screen, coordinate, color):
    list = x_coordinates[coordinate]
    for start, end in list:
        pygame.draw.line(screen, color, start, end, 5)

def draw_board(screen):
    screen.fill(BACKGROUND_COLOR)
    pygame.draw.rect(screen, BORDER_COLOR, (0, 0, SCREEN_WIDTH, SCREEN_HEIGHT), LINE_WIDTH)
    pygame.draw.line(screen, LINE_COLOR, (98, 6), (98, 294), LINE_WIDTH)
    pygame.draw.line(screen, LINE_COLOR, (196, 6), (196, 294), LINE_WIDTH)
    pygame.draw.line(screen, LINE_COLOR, (6, 98), (294, 98), LINE_WIDTH)
    pygame.draw.line(screen, LINE_COLOR, (6, 196), (294, 196), LINE_WIDTH)

def get_coordinate(x ,y):
    if x <= 100 and y <= 100:
        return "top_left"
    elif x > 100 and x <= 200 and y <= 100:
        return "top_mid"
    elif x > 200 and y <= 100:
        return "top_right"
    elif x <= 100 and y > 100 and y <= 200:
        return "mid_left"
    elif x > 100 and x <= 200 and y > 100 and y <= 200:
        return "middle"
    elif x > 200 and y > 100 and y <= 200:
        return "mid_right"
    elif x <= 100 and y > 200:
        return "bot_left"
    elif x > 100 and x <= 200 and y > 200:
        return "bot_mid"
    elif x > 200 and y > 200:
        return "bot_right"
    else:
        return ""

def draw_cell(x, y, screen, x_turn, grid):
    r = x // 100
    c = y // 100
    coordinate = get_coordinate(x, y)
    if grid[r][c] == None:
        if x_turn:
            draw_x(screen, coordinate, X_COLOR)
            grid[r][c] = 'X'
        else:
            draw_o(screen, coordinate, O_COLOR)
            grid[r][c] = 'O'
        return True
    return False

def check_win(grid, player):
    for row in grid:
        if all(cell == player for cell in row):
            return True
    
    for col in range(len(grid)):
        if all(row[col] == player for row in grid):
            return True
    
    if all(grid[i][i] == player for i in range(len(grid))):
        return True
    if all(grid[i][len(grid) - 1 - i] == player for i in range(len(grid))):
        return True
    
    return False
    
def draw_text(text, font, color, x, y):
    img = font.render(text, True, color)
    screen.blit(img, (x, y))

def draw_endscreen(game_won, player='X'):
    if game_won:
        if player == 'X':
            pygame.draw.rect(screen, BORDER_COLOR, (13, 95, 270, 110), 0)
            draw_text("Player X Wins!", TEXT_FONT, WHITE, 83, 100)
            draw_text("Would you like to play again?", TEXT_FONT, WHITE, 20, 125)
            draw_text("Yes", TEXT_FONT, GREEN, 80, 160)
            draw_text("No", TEXT_FONT, RED, 185, 160)
        elif player == 'O':
            pygame.draw.rect(screen, BORDER_COLOR, (13, 95, 270, 110), 0)
            draw_text("Player O Wins!", TEXT_FONT, WHITE, 83, 100)
            draw_text("Would you like to play again?", TEXT_FONT, WHITE, 20, 125)
            draw_text("Yes", TEXT_FONT, GREEN, 80, 160)
            draw_text("No", TEXT_FONT, RED, 185, 160)
    else:
        pygame.draw.rect(screen, BORDER_COLOR, (13, 95, 270, 110), 0)
        draw_text("It's a Draw!", TEXT_FONT, WHITE, 100, 100)
        draw_text("Would you like to play again?", TEXT_FONT, WHITE, 20, 125)
        draw_text("Yes", TEXT_FONT, GREEN, 80, 160)
        draw_text("No", TEXT_FONT, RED, 185, 160)

def is_full(grid):
    for row in grid:
        for element in row:
            if element is None:
                return False
    return True

def clear_grid(grid):
    for i in range(len(grid)):
        for j in range(len(grid[i])):
            grid[i][j] = None

run = True
while run:

    for event in pygame.event.get():
        if not game_started: # Ensures the board is not erased with each loop
            draw_board(screen)
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.MOUSEBUTTONDOWN and not game_ended: # adds 'X' or 'O'
            x, y = pygame.mouse.get_pos()
            game_started = True
            if draw_cell(x, y, screen, x_turn, grid):
                x_turn = not x_turn
        if check_win(grid, 'X'):
            game_ended = True
            draw_endscreen(True)
        elif check_win(grid, 'O'):
            game_ended = True
            draw_endscreen(True, 'O')
        elif is_full(grid):
            game_ended = True
            draw_endscreen(False)
        if event.type == pygame.MOUSEBUTTONDOWN and game_ended:
            x, y = pygame.mouse.get_pos()
            if y >= 150 and y <= 182:
                if x >= 70 and x <= 115: # User clicked on 'Yes'
                    game_started = game_ended = False
                    x_turn = True
                    clear_grid(grid)
                elif x >= 180 and x <= 212: # User clicked on 'No'
                    run = False

    pygame.display.update()

pygame.quit()