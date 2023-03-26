import math
import random
import pygame
import tkinter as tk
from tkinter import messagebox


class cube(object):
	rows = 20
	w = 500
	def __init__(self,start,dirnx=1,dirny=0,color=(0,255,128), points = 1):
		self.pos = start
		self.dirnx = 0
		self.dirny = 0
		self.color = color
		self.points = points


	def move(self, dirnx, dirny):
		self.dirnx = dirnx
		self.dirny = dirny
		self.pos = (self.pos[0] + self.dirnx, self.pos[1] + self.dirny)

	def draw(self, surface, eyes=False):
		dis = self.w // self.rows
		i = self.pos[0]
		j = self.pos[1]

		pygame.draw.rect(surface, self.color, (i*dis+1,j*dis+1, dis-2, dis-2))
		if eyes:
			center = dis//2
			radius = 3
			circleMiddle = (i*dis+center-radius,j*dis+8)
			circleMiddle2 = (i*dis + dis -radius*2, j*dis+8)
			pygame.draw.circle(surface, (0,0,0), circleMiddle, radius)
			pygame.draw.circle(surface, (0,0,0), circleMiddle2, radius)




class snake(object):
	body = []
	turns = {}
	def __init__(self, color, pos):
		self.color = color
		self.head = cube(pos)
		self.body.append(self.head)
		self.dirnx = 0
		self.dirny = 1
	def move(self):
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()

			keys = pygame.key.get_pressed()

			for key in keys:
				if keys[pygame.K_LEFT]:
					if not self.dirnx == 1:
						self.dirnx = -1
						self.dirny = 0
						self.turns[self.head.pos[:]] = [self.dirnx, self.dirny]

				elif keys[pygame.K_RIGHT]:
					if not self.dirnx == -1:
							self.dirnx = 1
							self.dirny = 0
							self.turns[self.head.pos[:]] = [self.dirnx, self.dirny]

				elif keys[pygame.K_UP]:
					if not self.dirny == 1:
						self.dirnx = 0
						self.dirny = -1
						self.turns[self.head.pos[:]] = [self.dirnx, self.dirny]

				elif keys[pygame.K_DOWN]:
					if not self.dirny == -1:
						self.dirnx = 0
						self.dirny = 1
						self.turns[self.head.pos[:]] = [self.dirnx, self.dirny]
	
		for i, c in enumerate(self.body):
			p = c.pos[:]
			if p in self.turns:
				turn = self.turns[p]
				c.move(turn[0], turn[1])
				if i == len(self.body)-1:
					self.turns.pop(p)

				# Hitting the boundaries of the screen
			else:
				if c.dirnx == -1 and c.pos[0] <= 0: death_end() #c.pos = (c.rows-1,c.pos[1])
				elif c.dirnx == 1 and c.pos[0] >= c.rows-1: death_end()#c.pos = (0,c.pos[1])
				elif c.dirny == 1 and c.pos[1] >= c.rows-1: death_end()#c.pos = (c.pos[0], 0)
				elif c.dirny == -1 and c.pos[1] <= 0: death_end()#c.pos = (c.pos[0],c.rows-1)
				else: c.move(c.dirnx,c.dirny)


# This is what makes the snake return to the center of the screen 
# And reverts it to just the head of the snake
	def reset(self, pos):
		self.head = cube(pos)
		self.body = [] # Gets rid of all cubes on the snake
		self.body.append(self.head) # Creates a head for the snake
		self.dirnx = 0
		self.dirny = 1
# This section is what adds the cubes to the tail of the snake
	def addCube(self):
		tail = self.body[-1] # The last cube in the snake
		dx, dy = tail.dirnx, tail.dirny

		if dx == 1 and dy == 0: # If the snake is traveling to the right,
			self.body.append(cube((tail.pos[0]-1,tail.pos[1]))) # Add a cube to the left
		elif dx == -1 and dy == 0: # If the snake is traveling to the left,
			self.body.append(cube((tail.pos[0]+1,tail.pos[1]))) # Add a cube to the right
		elif dx == 0 and dy == 1: # If the snake is traveling down, 
			self.body.append(cube((tail.pos[0],tail.pos[1]-1))) # Add a cube to the top
		elif dx == 0 and dy == -1: # If the snake is traveling upwards,
			self.body.append(cube((tail.pos[0],tail.pos[1]+1))) # Add a cube to the bottom

		self.body[-1].dirnx = dx # dx = the x coordinate of the last cube
		self.body[-1].dirny = dy # dy = the y coordinate of the last cube


	def draw(self, surface):
		for i, c in enumerate(self.body):
			if i ==0:
				c.draw(surface, True)
			else:
				c.draw(surface)
def drawGrid(w, rows, surface):
	sizeBtwn = w // rows
	x = 0
	y = 0
	for l in range(rows):
		x += sizeBtwn
		y += sizeBtwn

		pygame.draw.line(surface, (64,64,64), (x, 0), (x, w))
		pygame.draw.line(surface, (64,64,64), (0, y), (w, y))

def redrawWindow(surface):
	global rows, width, s, snack
	surface.fill((0,0,0))
	drawGrid(width, rows, surface)
	s.draw(surface)
	snack.draw(surface)
	pygame.display.update()

def randomSnack(rows, items):
	positions = items.body
	while True:
		x = random.randrange(rows)
		y = random.randrange(rows)
		if len(list(filter(lambda z:z.pos == (x,y), positions))) > 0:
			continue
		else:
			break
	return (x,y)


def message_box(subject, content):
			
	root = tk.Tk()
	root.attributes("-topmost", True)
	root.withdraw()
	messagebox.showinfo(subject, content)
	try:
		root.destroy()
	except:
		pass
def death_end():
	print('Score: ', len(s.body))
	message_box("You lost! :(", "Your score was %s. Play again?" % len(s.body))
	s.reset((10,10))
#Main Function:
def main():
	global width, rows, s, snack
	width = 500
	rows = 20
	win = pygame.display.set_mode((width, width))
	s = snake((0,255,128), (10,10))
	snack = cube(randomSnack(rows, s), color=(255,0,10))
	flag = True

	clock = pygame.time.Clock()

	while flag:
		pygame.time.delay(50)
		clock.tick(10)
		s.move()
		if s.body[0].pos == snack.pos:
			i = 0
			while i < snack.points:
				s.addCube()
				i += 1
			numPoints = random.randrange(1,3)
			if numPoints == 1:
				snack = cube(randomSnack(rows, s), color=(255,0,10))
			if numPoints == 2: 
				snack = cube(randomSnack(rows, s), color=(128,0,128))
			snack.points = numPoints

		for x in range(len(s.body)):
			if s.body[x].pos in list(map(lambda x:x.pos, s.body[x+1:])):
			# the lamda generates a list of the non-head parts of the body
			# if the head is in the same spot as a part of the body, the game ends
				death_end()
				break


		redrawWindow(win)



	pass


main()