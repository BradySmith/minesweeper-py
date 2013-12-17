"""
    Clone of Minesweeper
    ====================
    Written in Python using Pygame as a learning project.
    Author: Brady Smith
            brady_smith@outlook.com
            github.com/BradySmith
"""

import sys
import pygame
from random import randint

# Game Variables
GRID_SIZE = 15
CELL_SIZE = 20
MINE_COUNT = 40

# Calculated Variables for Setup
MAX_SCREEN_HEIGHT = GRID_SIZE * CELL_SIZE
MIN_SCREEN_HEIGHT = 0
MAX_SCREEN_WIDTH = GRID_SIZE * CELL_SIZE
MIN_SCREEN_WIDTH = 0
MAX_COL_COUNT = GRID_SIZE - 1
MAX_ROW_COUNT = GRID_SIZE - 1

# Defined Colours 
black   = (   0,   0,   0)
white   = ( 255, 255, 255)
blue    = ( 100, 149, 237)
red     = ( 255,   0,   0)

# Various 2d arrays used to track the status of the game
Cells_Rects = [[0 for x in range(GRID_SIZE)] for x in range(GRID_SIZE)]
Cells_Colour = [[0 for x in range(GRID_SIZE)] for x in range(GRID_SIZE)]
Minefield = [[0 for x in range(GRID_SIZE)] for x in range(GRID_SIZE)]
Revealed_Cells = [[False for x in range(GRID_SIZE)] for x in range(GRID_SIZE)]

# Boilerplate for Pygame
pygame.init()
size = [MAX_SCREEN_WIDTH, MAX_SCREEN_HEIGHT]
screen = pygame.display.set_mode(size) 
pygame.display.set_caption("Minesweeper")

"""
Initializes the minefield and sets the proximity values of all grids
"""
def seedMines(size):
    # TODO: Calculate proximity to mines
    for i in range(0, MINE_COUNT):
        mine = randint(0,((GRID_SIZE*GRID_SIZE)-1))
        mine_x = mine // GRID_SIZE
        temp = mine_x * GRID_SIZE
        mine_y = mine - temp
        if ( Minefield[mine_x][mine_y] == 0):
            Minefield[mine_x][mine_y] = 9 
        else:
            i = i-1
    for x in range(0, size):
        for y in range(0, size):
            if (Minefield[x][y] > 8):
                if (x != MIN_SCREEN_WIDTH):
                    Minefield[x-1][y] = Minefield[x-1][y] + 1
                if (x != MAX_COL_COUNT):
                    Minefield[x+1][y] = Minefield[x+1][y] + 1
                if (y != MIN_SCREEN_HEIGHT):
                    Minefield[x][y-1] = Minefield[x][y-1] + 1
                if (y != MAX_ROW_COUNT):
                    Minefield[x][y+1] = Minefield[x][y+1] + 1
                if (y != MIN_SCREEN_HEIGHT and x != MIN_SCREEN_WIDTH):
                    Minefield[x-1][y-1] = Minefield[x-1][y-1] + 1
                if (y != MAX_ROW_COUNT and x != MAX_COL_COUNT):
                    Minefield[x+1][y+1] = Minefield[x+1][y+1] + 1
                if (y != MIN_SCREEN_HEIGHT and x != MAX_COL_COUNT):
                    Minefield[x+1][y-1] = Minefield[x+1][y-1] + 1
                if (y != MAX_ROW_COUNT and x != MIN_SCREEN_WIDTH):
                    Minefield[x-1][y+1] = Minefield[x-1][y+1] + 1

"""
Intialize all Cells_Rects to their starting value
    * Set all cell colours to blue
    * Set all touples in a 2d array
"""
def intializeCells(size):
    cell_x = 0
    cell_y = 0
    for row in range(0, size):
        cell_x = 0
        for col in range(0, size):
            Cells_Rects[col][row] = pygame.Rect(cell_x, cell_y, CELL_SIZE, CELL_SIZE)
            Cells_Colour[col][row] = blue
            pygame.draw.rect(screen, Cells_Colour[col][row], Cells_Rects[col][row])
            cell_x += CELL_SIZE
            Revealed_Cells[col][row] = False 
        cell_y += CELL_SIZE

""" 
    Draw the cell we just passed in using the generated values and colours
"""
def drawCells(size, x, y):
    for row in range(0, size):
        for col in range(0, size):
            if (row == y and col == x):
                pygame.draw.rect(screen, Cells_Colour[col][row], Cells_Rects[col][row])

""" 
    Draw a grid over all the cells
"""            
def drawGrid(size):
    x = CELL_SIZE
    y = CELL_SIZE
    for row in range(0, size):
        pygame.draw.line(screen, black, (x, MAX_SCREEN_HEIGHT), (x, MIN_SCREEN_HEIGHT) )
        pygame.draw.line(screen, black, (MIN_SCREEN_WIDTH, y), (MAX_SCREEN_WIDTH, y) )
        x += CELL_SIZE
        y += CELL_SIZE

""" 
    Displays the passed in character at the given point on the grid
""" 
def displayChar(inChar, x, y):
    char = inChar
    if (inChar > 8):
        char = "*"
    if (inChar == 0):
        char = " "
    myFont = pygame.font.SysFont("None", 25)
    renderChar = myFont.render(str(char), 0, (black))
    rect = renderChar.get_rect()
    rect.center = Cells_Rects[x][y].center
    screen.blit(renderChar, rect)

""" 
    Helper function to change the color of a given grid square
""" 
def setGridColor(x, y, color):
    Cells_Colour[x][y] = color

""" 
    Function that is called when a mine (represented by a value 9 or larger) is clicked on
""" 
def mineWasHit(x, y, grid):
    setGridColor(x, y, red) 
    drawCells(GRID_SIZE, x, y)
    drawGrid(GRID_SIZE)
    displayChar(grid, x, y)

""" 
    Function that is called when a blank square (represented by 0) is clicked on
""" 
def blankGridWasHit(x, y):
    grid = Minefield[x][y]
    setGridColor(x, y, white) 
    drawCells(GRID_SIZE, x, y)
    drawGrid(GRID_SIZE)
    displayChar(grid, x, y)
    
    # Cascade to all neighbour squares
    gridClicked(x-1, y)
    gridClicked(x+1, y)
    gridClicked(x, y+1)
    gridClicked(x, y-1)
    gridClicked(x-1, y-1)
    gridClicked(x+1, y+1)
    gridClicked(x-1, y+1)
    gridClicked(x+1, y-1)

""" 
    Function that is called when a square with proximity information is selected
"""
def proximityGridWasHit(x, y):
    grid = Minefield[x][y]
    setGridColor(x, y, white) 
    drawCells(GRID_SIZE, x, y)
    drawGrid(GRID_SIZE)
    displayChar(grid, x, y)

""" 
    Function that  pulls apart the mouse input and assigns it to the correct function
"""
def mouseHandler(pos):
    mouse_x = pos[0]
    mouse_y = pos[1]
    mouse_x = mouse_x // CELL_SIZE
    mouse_y = mouse_y // CELL_SIZE
    gridClicked(mouse_x, mouse_y) 

""" 
    Function that returns whether or not a row has been revealed or not
"""
def coordinateIsRevealed(x, y):
    return Revealed_Cells[x][y]

""" 
    Function that checks to see if the coordinates are out of bounds
"""
def coordinateIsOutOfBounds(x, y):
    return x > MAX_COL_COUNT or x < MIN_SCREEN_WIDTH or y > MAX_ROW_COUNT or y < MIN_SCREEN_HEIGHT

""" 
    Is called on a mouseclick and figures out what to put where
       Basically if mouseclick detected get the position and use
       integer division to change the block colour and set the appropriate
       character
""" 
def gridClicked(x, y):
    if (coordinateIsOutOfBounds(x, y)):
        return
    elif (coordinateIsRevealed(x, y)):
        return
    else:
        Revealed_Cells[x][y] = True
        grid = Minefield[x][y]
        if (grid > 8):
            mineWasHit(x, y, grid)
        elif (grid == 0):
            blankGridWasHit(x, y)
        else:
            proximityGridWasHit(x, y) 
            
""" 
    Main method
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
                mouseHandler(pos)
        pygame.display.flip() 
    pygame.quit()

if __name__ == '__main__':
    main()
