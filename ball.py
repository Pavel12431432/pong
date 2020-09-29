import math


INITIAL_POSITION = [400, 300]

class Ball:
	def __init__(self, velocity, r, max_speed):
		self.pos = INITIAL_POSITION
		self.velocity = velocity
		self.r = r
		self.max_speed = max_speed

	# collide ball with edges
	def collide_edges(self, width, height):
		if not self.r < self.pos[0] < width - self.r:
			self.velocity[0] *= -1
		elif not self.r < self.pos[1] < height - self.r:
			self.velocity[1] *= -1
		self.pos[0] = min(max(self.pos[0], self.r), width - self.r)
		self.pos[1] = min(max(self.pos[1], self.r), height - self.r)

	# collide ball with paddles
	def collide_paddles(self, paddle1_y, paddle2_y, paddle_height, paddle_width, width):
		# check if ball is colliding with left paddle
		if 50 - self.r < self.pos[0] < 50 + paddle_width + self.r and paddle1_y - self.r < self.pos[
			1] < paddle1_y + paddle_height + self.r:
			# get velocity based on where the ball hit the paddle
			angle = translate(self.pos[1] - paddle1_y, 0, paddle_height, -math.radians(45), math.radians(45))
			self.velocity = [self.max_speed * math.cos(angle), self.max_speed * math.sin(angle)]
		# check if ball is colliding with right paddle
		elif width - 50 + self.r > self.pos[0] > width - 50 - self.r and paddle2_y - self.r < self.pos[
			1] < paddle2_y + paddle_height + self.r:
			# get velocity based on where the ball hit the paddle
			angle = translate(self.pos[1] - paddle2_y, 0, paddle_height, math.radians(225), math.radians(135))
			self.velocity = [self.max_speed * math.cos(angle), self.max_speed * math.sin(angle)]

	def reset_position(self):
		self.pos = INITIAL_POSITION

	# update ball position
	def update_position(self, max_width):
		score1, score2 = 0, 0
		self.pos = list(map(sum, zip(self.pos, self.velocity)))
		# check if player has scored
		if self.pos[0] < 50:
			score1 = 1
			self.pos = INITIAL_POSITION
		elif self.pos[0] > max_width - 50:
			score2 = 1
			self.pos = INITIAL_POSITION
		# return score updates
		return score1, score2

def translate(value, leftMin, leftMax, rightMin, rightMax):
	leftSpan = leftMax - leftMin
	rightSpan = rightMax - rightMin
	valueScaled = float(value - leftMin) / float(leftSpan)
	return rightMin + (valueScaled * rightSpan)
