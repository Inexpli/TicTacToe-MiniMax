import pygame
from pygame.locals import *

pygame.init()

screen_height = 900
screen_width = 900
line_width = 5
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('Tic Tac Toe')

#define colours
red = (255, 0, 0)
green = (0, 255, 0)
blue = (0, 0, 255)

#define font
font = pygame.font.SysFont(None, 40)

#define variables
clicked = False
player = 1
pos = (0,0)
markers = []
game_over = False
winner = 0

#setup a rectangle for "Play Again" Option
again_rect = Rect(screen_width // 2 - 80, screen_height // 2, 160, 50)

#create empty 3 x 3 list to represent the grid
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


def check_game_over():
	global game_over
	global winner

	x_pos = 0
	for x in markers:
		#check columns
		if sum(x) == 3:
			winner = 1
			game_over = True
		if sum(x) == -3:
			winner = -1
			game_over = True
		#check rows
		if markers[0][x_pos] + markers [1][x_pos] + markers [2][x_pos] == 3:
			winner = 1
			game_over = True
		if markers[0][x_pos] + markers [1][x_pos] + markers [2][x_pos] == -3:
			winner = -1
			game_over = True
		x_pos += 1

	#check cross
	if markers[0][0] + markers[1][1] + markers [2][2] == 3 or markers[2][0] + markers[1][1] + markers [0][2] == 3:
		winner = 1
		game_over = True
	if markers[0][0] + markers[1][1] + markers [2][2] == -3 or markers[2][0] + markers[1][1] + markers [0][2] == -3:
		winner = 2
		game_over = True

	#check for tie
	if game_over == False:
		tie = True
		for row in markers:
			for i in row:
				if i == 0:
					tie = False
		#if it is a tie, then call game over and set winner to 0 (no one)
		if tie == True:
			game_over = True
			winner = 0



def draw_game_over(winner):

	if winner != 0:
		end_text = "Player " + str(winner) + " wins!"
	elif winner == 0:
		end_text = "You have tied!"

	end_img = font.render(end_text, True, blue)
	pygame.draw.rect(screen, green, (screen_width // 2 - 100, screen_height // 2 - 60, 200, 50))
	screen.blit(end_img, (screen_width // 2 - 100, screen_height // 2 - 50))

	again_text = 'Play Again?'
	again_img = font.render(again_text, True, blue)
	pygame.draw.rect(screen, green, again_rect)
	screen.blit(again_img, (screen_width // 2 - 80, screen_height // 2 + 10))


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