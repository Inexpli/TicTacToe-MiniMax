import csv
import math
import random
import pygame
from pygame.locals import *

pygame.init()

# game window config (screen width, height etc.)
screen_height = 900
screen_width = 900
line_width = 5
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('Tic Tac Toe')

# define font
font = pygame.font.SysFont(None, 40)

# define variables
clicked = False
pos = (0,0)
markers = []
game_over = False
winner = 0

# setup a rectangle for "Play Again" Option
again_rect = Rect(screen_width // 2 - 80, screen_height // 2, 160, 50)

# create empty 3 x 3 list to represent the grid
for x in range (3):
    row = [0] * 3
    markers.append(row)

def draw_board():
    bg = (51, 51, 204)
    grid = (0, 204, 255)
    screen.fill(bg)
    for x in range(1,3):
        pygame.draw.line(screen, grid, (0, 300 * x), (screen_width, 300 * x), line_width)
        pygame.draw.line(screen, grid, (300 * x, 0), (300 * x, screen_height), line_width)

def draw_markers():
    x_pos = 0
    for x in markers:
        y_pos = 0
        for y in x:
            if y == 1:
                pygame.draw.line(screen, (255, 0, 102), (x_pos * 300 + 45, y_pos * 300 + 45), (x_pos * 300 + 245, y_pos * 300 + 245), 7)
                pygame.draw.line(screen, (255, 0, 102), (x_pos * 300 + 245, y_pos * 300 + 45), (x_pos * 300 + 45, y_pos * 300 + 245), 7)
            if y == -1:
                pygame.draw.circle(screen, (255, 255, 255), (x_pos * 300 + 150, y_pos * 300 + 150), 90, 7)
            y_pos += 1
        x_pos += 1	

def num_empty_squares(markers):
    empty = 0
    for row in markers:
        for i in row:
            if i == 0:
                empty += 1
    return empty

def available_moves(markers):
    moves = []
    for i, row in enumerate(markers):
        for j, cell in enumerate(row):
            if cell == 0:
                moves.append((i, j))
    return moves

def make_move(markers, i, j, letter):
    if markers[i][j] == 0:
        markers[i][j] = letter
        return True
    return False

def check_game_over(markers):
    for x in markers:
        if sum(x) == 3:
            return 1
        if sum(x) == -3:
            return -1

    for x_pos in range(3):
        if markers[0][x_pos] + markers[1][x_pos] + markers[2][x_pos] == 3:
            return 1
        if markers[0][x_pos] + markers[1][x_pos] + markers[2][x_pos] == -3:
            return -1

    if markers[0][0] + markers[1][1] + markers[2][2] == 3 or markers[2][0] + markers[1][1] + markers[0][2] == 3:
        return 1
    if markers[0][0] + markers[1][1] + markers[2][2] == -3 or markers[2][0] + markers[1][1] + markers[0][2] == -3:
        return -1

    if num_empty_squares(markers) == 0:
        return 0

    return None

def draw_game_over(winner):
    if winner != 0:
        end_text = "Player " + str(winner) + " wins!"
    elif winner == 0:
        end_text = "You have tied!"

    end_img = font.render(end_text, True, (255, 102, 0))
    pygame.draw.rect(screen, (0, 0, 0), (screen_width // 2 - 100, screen_height // 2 - 60, 200, 50))
    screen.blit(end_img, (screen_width // 2 - 100, screen_height // 2 - 50))

    again_text = 'Play Again?'
    again_img = font.render(again_text, True, (255, 102, 0))
    pygame.draw.rect(screen, (0, 0, 0), again_rect)
    screen.blit(again_img, (screen_width // 2 - 80, screen_height // 2 + 10))

def minimax(markers, player):
    max_player = 1
    other_player = -1 if player == 1 else 1

    if check_game_over(markers) == other_player:
        return {'position': None, 'score': 1 * (num_empty_squares(markers) + 1) if other_player == max_player else -1 * (num_empty_squares(markers) + 1)}
    elif check_game_over(markers) == 0:
        return {'position': None, 'score': 0}

    if player == max_player:
        best = {'position': None, 'score': -math.inf}  # each score should maximize
    else:
        best = {'position': None, 'score': math.inf}  # each score should minimize
    for possible_move in available_moves(markers):
        make_move(markers, possible_move[0], possible_move[1], player)
        sim_score = minimax(markers, other_player)  # simulate a game after making that move

        # undo move
        markers[possible_move[0]][possible_move[1]] = 0

        sim_score['position'] = possible_move  # this represents the move optimal next move

        if player == max_player:  # X is max player
            if sim_score['score'] > best['score']:
                best = sim_score
        else:
            if sim_score['score'] < best['score']:
                best = sim_score
    return best

def generate_move(markers, player):
    if len(available_moves(markers)) == 9:
        square = random.choice(available_moves(markers))
    else:
        square = minimax(markers, player)['position']
    return square

def game():
    global game_over, winner, markers, clicked
    #main loop
    run = True
    while run:
        #draw board and markers first
        draw_board()
        draw_markers()

        #handle events
        for event in pygame.event.get():
            #handle game exit
            if event.type == pygame.QUIT:
                run = False
            #run new game
            if game_over == False:
                #check for mouseclick
                if event.type == pygame.MOUSEBUTTONDOWN and clicked == False:
                    clicked = True
                if event.type == pygame.MOUSEBUTTONUP and clicked == True:
                    clicked = False
                    pos = pygame.mouse.get_pos()
                    cell_x = pos[0] // 300
                    cell_y = pos[1] // 300
                    if markers[cell_x][cell_y] == 0:
                        markers[cell_x][cell_y] = 1
                        winner = check_game_over(markers)
                        if winner is None:
                            ai_move = generate_move(markers, -1)
                            markers[ai_move[0]][ai_move[1]] = -1
                            winner = check_game_over(markers)
                            if winner is not None:
                                game_over = True
                        else:
                            game_over = True

        #check if game has been won
        if game_over == True:
            draw_game_over(winner)
            if event.type == pygame.MOUSEBUTTONDOWN and clicked == False:
                clicked = True
            if event.type == pygame.MOUSEBUTTONUP and clicked == True:
                clicked = False
                pos = pygame.mouse.get_pos()
                if again_rect.collidepoint(pos):
                    game_over = False
                    markers = [[0] * 3 for _ in range(3)]
                    winner = 0

        pygame.display.update()

    pygame.quit()

game()
