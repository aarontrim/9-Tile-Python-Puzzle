import pygame
import numpy as np
import random


class PuzzlePiece():
    def __init__(self, surface, x, y):
        self.surface = surface
        self.trueSurface = surface
        self.trueX = x
        self.trueY = y
        self.curX = x
        self.curY = y
        self.blank = False

    def move_n(self, n):
        x, y = self.n_to_xy(n)
        self.curX = x
        self.curY = y

    def move_XY(self, x, y):        
        self.curX = x
        self.curY = y

    def n_to_xy(self, n):
        return [n % length, n / length]

    def within_image(self, x, y):
        iX = self.curX * (width/length)
        iY = self.curY * (height/length)
        iW = self.surface.get_width()
        iH = self.surface.get_height()
        if(x >= iX and x <= iX + iW and y >= iY and y <= iY + iH):
            return True
        return False

    def get_draw_coords(self):
        return (self.curX * width/length, self.curY * height/length)

    def dump_stats(self):
        print("TrueX = " + str(self.trueX))
        print("TrueY = " + str(self.trueY))
        print("curX = " + str(self.curX))
        print("curY = " + str(self.curY))


def didyouwin():
    ticks = 0
    for tile in puzzleimgs:
        if(tile.trueX == tile.curX and tile.trueY == tile.curY):
            ticks += 1
    if ticks == numsquares:     
        return True
    
    return False

def adjacent_to_blank(n):
    for index, item in enumerate(puzzleimgs):
        if item.blank:
            bX, bY = [item.curX, item.curY]
            tX, tY = [puzzleimgs[n].curX, puzzleimgs[n].curY]
            if (np.abs(bX - tX) + np.abs(bY - tY) == 1):
                return True
            return False

def swap_with_blank(n):
    for index, item in enumerate(puzzleimgs):
        if item.blank:
            x, y = [puzzleimgs[index].curX, puzzleimgs[index].curY]
            item.move_XY(puzzleimgs[n].curX, puzzleimgs[n].curY)
            puzzleimgs[n].move_XY(x, y)
            break

def show_blank():
    for item in puzzleimgs:
        if item.blank:
            item.surface = item.trueSurface
            break


#Number of squares to play with, must be an integer with a integer square root
numsquares = 9

pygame.init()

gamedisplay = pygame.display.set_mode((360, 360))
pygame.display.set_caption("Puzzle Game")

clock = pygame.time.Clock()

ended = False

puzzleimg = pygame.image.load("thesenate.jpg")
height = puzzleimg.get_width()
width = puzzleimg.get_height()
length = int(np.sqrt(numsquares))


'''Crop image into tiles'''
puzzleimgs = []
for i in range(length):
    row = []
    for j in range(length):
        cropped = pygame.Surface((height/length, width/length))
        cropped.blit(puzzleimg, (0,0), (j*width/length,i*height/length,height/length, width/length))
        row.append(PuzzlePiece(cropped, j, i))
    puzzleimgs.append(row)
puzzleimgs = [item for sublist in puzzleimgs for item in sublist]


'''Randomize the order'''
randomized = list(range(numsquares))
random.shuffle(randomized)
for index, item in enumerate(randomized):
    puzzleimgs[index].move_n(item)
    '''Make one blank'''
    if item == 0:
        puzzleimgs[index].blank = True
        puzzleimgs[index].surface = pygame.Surface((height/length, width/length))

'''Play the game'''
while not ended:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            ended = True
        elif event.type == pygame.MOUSEBUTTONUP:
            for index, tile in enumerate(puzzleimgs):
                if tile.within_image(event.pos[0], event.pos[1]):
                    if not tile.blank:
                        if adjacent_to_blank(index):
                            swap_with_blank(index)
                            if didyouwin():
                                show_blank()

    gamedisplay.fill((255,255,255)) 
    gamedisplay.fill((0,0,0))   
    
    for i in range(numsquares):
        gamedisplay.blit(puzzleimgs[i].surface, puzzleimgs[i].get_draw_coords())

    pygame.display.update()
    clock.tick(60)

pygame.quit()
quit()