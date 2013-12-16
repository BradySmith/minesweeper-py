import sys
import pygame
from random import randint

# Game Variables
GRID_SIZE = 15
CELL_SIZE = 20
MINE_COUNT = 20

# Calculated Variables for Setup
MAX_Y = GRID_SIZE * CELL_SIZE
MIN_Y = 0
MAX_X = GRID_SIZE * CELL_SIZE
MIN_X = 0

# Defined Colours 
black   = (   0,   0,   0)
white   = ( 255, 255, 255)
blue    = ( 100, 149, 237)

# Various 2d arrays used to track the status of the game
Cells = [[0 for x in range(GRID_SIZE)] for x in range(GRID_SIZE)]
Cells_Colour = [[0 for x in range(GRID_SIZE)] for x in range(GRID_SIZE)]
Mines = [[0 for x in range(GRID_SIZE)] for x in range(GRID_SIZE)]

# Boilerplate for Pygame
pygame.init()
size = [MAX_X, MAX_Y]
screen = pygame.display.set_mode(size) 
pygame.display.set_caption("Minesweeper")

""" Intialize Minefield
"""
def seedMines(size):
    # TODO: Calculate proximity to mines
    for i in range(0, MINE_COUNT):
        mine = randint(0,((GRID_SIZE*GRID_SIZE)-1))
        mine_x = mine // GRID_SIZE
        temp = mine_x * GRID_SIZE
        mine_y = mine - temp
        if ( Mines[mine_x][mine_y] != -1):
            Mines[mine_x][mine_y] = -1
        else:
            i = i-1

""" Intialize all Cells to their starting value
       * Set all cell colours to blue
       * Set all touples in a 2d array
"""
def intializeCells(size):
    cell_x = 0
    cell_y = 0
    for row in range(0, size):
        cell_x = 0
        for col in range(0, size):
            Cells[col][row] = pygame.Rect(cell_x, cell_y, CELL_SIZE, CELL_SIZE)
            Cells_Colour[col][row] = blue
            pygame.draw.rect(screen, Cells_Colour[col][row], Cells[col][row])
            cell_x += CELL_SIZE
        cell_y += CELL_SIZE

""" Draw cells using the generated values and colours
"""
def drawCells(size, x, y):
    for row in range(0, size):
        for col in range(0, size):
            if (Cells_Colour[col][row] != white):
                pygame.draw.rect(screen, Cells_Colour[col][row], Cells[col][row])
            if (row == y and col == x):
                Cells_Colour[col][row] = white
                pygame.draw.rect(screen, Cells_Colour[col][row], Cells[col][row])

""" Draw a grid over all the cells
"""            
def drawGrid(size):
    x = CELL_SIZE
    y = CELL_SIZE
    for row in range(0, size):
        pygame.draw.line(screen, black, (x, MAX_Y), (x, MIN_Y) )
        pygame.draw.line(screen, black, (MIN_X, y), (MAX_X, y) )
        x += CELL_SIZE
        y += CELL_SIZE

""" Displays the passed in character at the given point on the grid
""" 
def displayChar(inChar, x, y):
    char = inChar
    if (inChar == -1):
        char = "@"
    myFont = pygame.font.SysFont("None", 25)
    renderChar = myFont.render(str(char), 0, (black))
    rect = renderChar.get_rect()
    rect.center = Cells[x][y].center
    screen.blit(renderChar, rect)

""" Is called on a mouseclick and figures out what to put where
       Basically if mouseclick detected get the position and use
       integer division to change the block colour and set the appropriate
       character
""" 
def gridClicked(pos):
    mouse_x = pos[0]
    mouse_y = pos[1]
    mouse_x = mouse_x // CELL_SIZE
    mouse_y = mouse_y // CELL_SIZE
    drawCells(GRID_SIZE, mouse_x, mouse_y)
    drawGrid(GRID_SIZE)
    displayChar(Mines[mouse_x][mouse_y], mouse_x, mouse_y)   

""" Main method
""" 
def main():
    screen.fill(white)
    intializeCells(GRID_SIZE)
    seedMines(GRID_SIZE)
    drawGrid(GRID_SIZE)
    done = False
    while done==False:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True
            elif event.type == pygame.MOUSEBUTTONUP:
                pos = pygame.mouse.get_pos()
                gridClicked(pos)
        pygame.display.flip() 
    pygame.quit()

if __name__ == '__main__':
    main()
