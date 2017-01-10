import pygame
import numpy as np
import random


class puzzlePiece():
	def __init__(self, surface, x, y):
		self.surface = surface
		self.trueSurface = surface
		self.trueX = x
		self.trueY = y
		self.curX = x
		self.curY = y
		self.blank = False

	def moveN(self, n):
		x, y = self.n_to_xy(n)
		self.curX = x
		self.curY = y

	def moveXY(self, x, y):		
		self.curX = x
		self.curY = y

	def n_to_xy(self, n):
		return [n % length, n / length]

	def withinImage(self, x, y):
		iX = self.curX * (width/length)
		iY = self.curY * (height/length)
		iW = self.surface.get_width()
		iH = self.surface.get_height()
		if(x >= iX and x <= iX + iW and y >= iY and y <= iY + iH):
			return True
		return False

	def getDrawCoords(self):
		return (self.curX * width/length, self.curY * height/length)

	def dumpStats(self):
		print "TrueX = " + str(self.trueX)
		print "TrueY = " + str(self.trueY)
		print "curX = " + str(self.curX)
		print "curY = " + str(self.curY)


def didYouWin():
	ticks = 0
	for tile in puzzleImgs:
		if(tile.trueX == tile.curX and tile.trueY == tile.curY):
			ticks += 1
	if ticks == numSquares:		
		print "SAMSIES!!!"
		return True
	
	return False

def adjacentToBlank(n):
	for index, item in enumerate(puzzleImgs):
		if item.blank:
			bX, bY = [item.curX, item.curY]
			tX, tY = [puzzleImgs[n].curX, puzzleImgs[n].curY]
			if (np.abs(bX - tX) + np.abs(bY - tY) == 1):
				return True
			return False

def swapWithBlank(n):
	for index, item in enumerate(puzzleImgs):
		if item.blank:
			x, y = [puzzleImgs[index].curX, puzzleImgs[index].curY]
			item.moveXY(puzzleImgs[n].curX, puzzleImgs[n].curY)
			puzzleImgs[n].moveXY(x, y)
			break

def showBlank():
	for item in puzzleImgs:
		if item.blank:
			item.surface = item.trueSurface
			break


'''Number of squares to play with, must be a square number'''
numSquares = 9



pygame.init()

gameDisplay = pygame.display.set_mode((360, 360))
pygame.display.set_caption("Puzzle Game")

clock = pygame.time.Clock()

ended = False

puzzleImg = pygame.image.load("thesenate.jpg")
height = puzzleImg.get_width()
width = puzzleImg.get_height()
length = int(np.sqrt(numSquares))


'''Crop image into tiles'''
puzzleImgs = []
for i in range(length):
	row = []
	for j in range(length):
		cropped = pygame.Surface((height/length, width/length))
		cropped.blit(puzzleImg, (0,0), (j*width/length,i*height/length,height/length, width/length))
		row.append(puzzlePiece(cropped, j, i))
	puzzleImgs.append(row)
puzzleImgs = [item for sublist in puzzleImgs for item in sublist]


'''Randomize the order'''
randomized = range(numSquares)
random.shuffle(randomized)
for index, item in enumerate(randomized):
	puzzleImgs[index].moveN(item)
	'''Make one blank'''
	if item == 0:
		puzzleImgs[index].blank = True
		puzzleImgs[index].surface = pygame.Surface((height/length, width/length))

'''Play the game'''
while not ended:
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			ended = True
		elif event.type == pygame.MOUSEBUTTONUP:
			for index, tile in enumerate(puzzleImgs):
					if tile.withinImage(event.pos[0], event.pos[1]):
						if not tile.blank:
							if adjacentToBlank(index):
								swapWithBlank(index)
								if didYouWin():
									showBlank()

	gameDisplay.fill((255,255,255))	
	gameDisplay.fill((0,0,0))	
	
	for i in range(numSquares):
		gameDisplay.blit(puzzleImgs[i].surface, puzzleImgs[i].getDrawCoords())

	pygame.display.update()
	clock.tick(60)

pygame.quit()
quit()