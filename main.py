import pygame
import math
from random import randint
from ball import Ball

# configuration constants
WIDTH, HEIGHT = 800, 600
PADDLE_HEIGHT = 100
PADDLE_WIDTH = 15
MOVEMENT_SPEED = 5
MAX_BALL_SPEED = 4

# init pygame
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT), 0, 32)
pygame.display.set_caption('Ray casting')
font = pygame.font.SysFont('microsoftyaheimicrosoftyaheiuibold', 100)
clock = pygame.time.Clock()

# initial state
paddle1_y = 300
paddle2_y = 300
score = [0, 0]


def inp():
	global paddle1_y, paddle2_y
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			quit()
	# update paddle positions on key press
	if pygame.key.get_pressed()[ord('a')]:
		paddle1_y = min(max(paddle1_y - MOVEMENT_SPEED, 0), HEIGHT - PADDLE_HEIGHT)
	if pygame.key.get_pressed()[ord('z')]:
		paddle1_y = min(max(paddle1_y + MOVEMENT_SPEED, 0), HEIGHT - PADDLE_HEIGHT)
	if pygame.key.get_pressed()[ord('k')]:
		paddle2_y = min(max(paddle2_y - MOVEMENT_SPEED, 0), HEIGHT - PADDLE_HEIGHT)
	if pygame.key.get_pressed()[ord('m')]:
		paddle2_y = min(max(paddle2_y + MOVEMENT_SPEED, 0), HEIGHT - PADDLE_HEIGHT)


# normalize vector
def norm(a, div):
	v = math.sqrt(a[0] ** 2 + a[1] ** 2) / div
	if v == 0:
		return 0
	return [a[0] / v, a[1] / v]


def loop():
	global balls, paddle1_y, paddle2_y, score
	screen.fill((0, 0, 0))
	# draw paddles
	pygame.draw.rect(screen, (200, 200, 200), ((50, paddle1_y), (PADDLE_WIDTH, PADDLE_HEIGHT)))
	pygame.draw.rect(screen, (200, 200, 200), ((WIDTH - 50, paddle2_y), (PADDLE_WIDTH, PADDLE_HEIGHT)))

	for ball in balls:
		# update ball pos
		score = list(map(sum, zip(score, ball.update_position(WIDTH))))
		# check ball collisions
		ball.update_position(WIDTH)
		ball.collide_edges(WIDTH, HEIGHT)
		ball.collide_paddles(paddle1_y, paddle2_y, PADDLE_HEIGHT, PADDLE_WIDTH, WIDTH)
		# draw ball
		pygame.draw.circle(screen, (200, 200, 200), tuple(map(int, ball.pos)), ball.r)

	# draw score
	screen.blit(font.render('{:02d}:{:02d}'.format(*score), True, (255, 255, 255)), ((WIDTH - 275) // 2, 0))

	pygame.display.update()


# balls = [Ball(norm([randint(0, 5), randint(5, 10)], 4), randint(5, 15), randint(2, 5)) for i in range(10)]
balls = [Ball([-3.3, 2.2], 10, MAX_BALL_SPEED)]

while True:
	inp()
	loop()
	clock.tick(120)