# libraries
import csv
import random
import pygame
from random import randint
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
global markers_count

# setup a rectangle for "Play Again" Option
again_rect = Rect(screen_width // 2 - 80, screen_height // 2, 160, 50)

# create empty 3 x 3 list to represent the grid
for x in range (3):
	row = [0] * 3
	markers.append(row)

# function drawing a board
def draw_board():
	bg = (51, 51, 204)
	grid = (0, 204, 255)
	screen.fill(bg)
	for x in range(1,3):
		pygame.draw.line(screen, grid, (0, 300 * x), (screen_width, 300 * x), line_width)
		pygame.draw.line(screen, grid, (300 * x, 0), (300 * x, screen_height), line_width)

# function drawing a markers
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

# prints out game over
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

# checks if game is over
def check_game_over():
	global game_over
	global winner

	x_pos = 0
	for x in markers:
		# check columns
		if sum(x) == 3:
			winner = 1
			game_over = True
		if sum(x) == -3:
			winner = -1
			game_over = True
		# check rows
		if markers[0][x_pos] + markers [1][x_pos] + markers [2][x_pos] == 3:
			winner = 1
			game_over = True
		if markers[0][x_pos] + markers [1][x_pos] + markers [2][x_pos] == -3:
			winner = -1
			game_over = True
		x_pos += 1

	# check cross
	if markers[0][0] + markers[1][1] + markers [2][2] == 3 or markers[2][0] + markers[1][1] + markers [0][2] == 3:
		winner = 1
		game_over = True
	if markers[0][0] + markers[1][1] + markers [2][2] == -3 or markers[2][0] + markers[1][1] + markers [0][2] == -3:
		winner = -1
		game_over = True

	# check for tie
	if game_over == False:
		tie = True
		for row in markers:
			for i in row:
				if i == 0:
					tie = False
		# if it is a tie, then call game over and set winner to 0 (no one)
		if tie == True:
			game_over = True
			winner = 0

# saves the course of the game
def write_to_csv():
	with open('tictactoe.csv', 'a', newline='') as csvfile:
		fieldnames = ['1', '2', '3', '4', '5', '6', '7', '8', '9', 'Winner']
		writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
		z = 1
		row_data = {}
		for i in range(3):
			for j in range(3):
				row_data[str(z)] = markers[j][i]
				z += 1
		row_data['Winner'] = winner
		writer.writerow(row_data)

# generates move randomly
def generate_move(player):
	posx = random.randint(1, 800)
	posy = random.randint(1, 800)
	markers_count = 0
	cell_x = posx // 300
	cell_y = posy // 300
	
	if markers[cell_x][cell_y] == 0:
		markers[cell_x][cell_y] = player
	elif (markers[cell_x][cell_y] == -1) or (markers[cell_x][cell_y] == 1):
		generate_move(player)

	for x in markers:
		for y in x:
			if y == 1:
				markers_count += 1

	if markers_count >= 3:
		check_game_over()

# defines which player starts first (X or O)
# X: 1
# O: -1 
player = 1

# function to simulate game between two players
def simulate_game(games_count = 1000):
    global game_over, player, winner, markers
    i = 0
    run = True
    while run:
        # draw board and markers first
        draw_board()
        draw_markers()

        # handle events
        for event in pygame.event.get():
            # handle game exit
            if event.type == pygame.QUIT:
                run = False

		# handles simulations count
        if (i>=games_count):
            run = False
		
		# preserves the nature of tic-tac-toe
        if game_over == False:
            if player == 1:
                generate_move(player)
            elif player == -1:
                generate_move(player)
            player *= -1

		# if game is over, function calls to save the game to CSV file
		# and reset the variables so the new game can be started
        if game_over == True:
            write_to_csv()
            i+=1
            # reset variables
            game_over = False
            player = 1
            markers = []
            winner = 0
            # create empty 3 x 3 list to represent the grid
            for x in range(3):
                row = [0] * 3
                markers.append(row)

        pygame.display.update()

    pygame.quit()

# function to call normal game between two players
def game():
	global game_over, player, winner, markers, clicked
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
						markers[cell_x][cell_y] = player
						player *= -1
						check_game_over()

		#check if game has been won
		if game_over == True:
			draw_game_over(winner)
			#check for mouseclick to see if we clicked on Play Again
			if event.type == pygame.MOUSEBUTTONDOWN and clicked == False:
				clicked = True
			if event.type == pygame.MOUSEBUTTONUP and clicked == True:
				clicked = False
				pos = pygame.mouse.get_pos()
				if again_rect.collidepoint(pos):
					#reset variables
					game_over = False
					player = 1
					pos = (0,0)
					markers = []
					winner = 0
					#create empty 3 x 3 list to represent the grid
					for x in range (3):
						row = [0] * 3
						markers.append(row)

		#update display
		pygame.display.update()

	pygame.quit()

simulate_game()
