"""
    Clone of Minesweeper
    ====================
    Written in Python using Pygame as a learning project.
    Author: Brady Smith
            brady_smith@outlook.com
            github.com/BradySmith
"""

import pygame
from random import randint

# Game Variables
GRID_SIZE = 15
CELL_SIZE = 20
MINE_COUNT = 20
TIME = 0

# Calculated Variables for Setup
MENU_BAR_HEIGHT = 30
MENU_BAR_WIDTH = GRID_SIZE * CELL_SIZE
MAX_SCREEN_HEIGHT = GRID_SIZE * CELL_SIZE + MENU_BAR_HEIGHT
MIN_SCREEN_HEIGHT = MENU_BAR_HEIGHT
MAX_SCREEN_WIDTH = MENU_BAR_WIDTH
MIN_SCREEN_WIDTH = 0
MAX_COL_COUNT = GRID_SIZE - 1
MAX_ROW_COUNT = GRID_SIZE - 1

# Defined Colours 
black   = (   0,   0,   0)
white   = ( 255, 255, 255)
lightgrey = (238, 233, 233)
green   = (   0, 100,   0)
blue    = ( 100, 149, 237)
darkblue =(   0,   0, 205)
red     = ( 255,   0,   0)
purple  = (  25,  25, 112)
darkred = ( 102,   0,   0)
iceblue = (   0, 204, 204)
grey    = ( 128, 128, 128)

# Various 2d arrays used to track the status of the game
Cells_Rects = [[0 for x in range(GRID_SIZE)] for x in range(GRID_SIZE)]
Cells_Colour = [[0 for x in range(GRID_SIZE)] for x in range(GRID_SIZE)]
Minefield = [[0 for x in range(GRID_SIZE)] for x in range(GRID_SIZE)]
Revealed_Cells = [[1 for x in range(GRID_SIZE)] for x in range(GRID_SIZE)]

# Boilerplate for Pygame
pygame.init()
size = [MAX_SCREEN_WIDTH, MAX_SCREEN_HEIGHT]
screen = pygame.display.set_mode(size) 
pygame.display.set_caption("Minesweeper")


"""
Initializes the minefield and sets the proximity values of all grids
"""
def seedMines():
    for i in range(0, MINE_COUNT):
        mine = randint(0,((GRID_SIZE*GRID_SIZE)-1))
        mine_x = mine // GRID_SIZE
        temp = mine_x * GRID_SIZE
        mine_y = mine - temp
        if ( Minefield[mine_x][mine_y] == 0):
            Minefield[mine_x][mine_y] = 9 
        else:
            i = i-1
    for x in range(0, GRID_SIZE):
        for y in range(0, GRID_SIZE):
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
def intializeCells():
    cell_x = 0
    cell_y = MIN_SCREEN_HEIGHT
    for row in range(0, GRID_SIZE):
        cell_x = 0
        for col in range(0, GRID_SIZE):
            Cells_Rects[col][row] = pygame.Rect(cell_x, cell_y, CELL_SIZE, CELL_SIZE)
            Cells_Colour[col][row] = blue
            pygame.draw.rect(screen, Cells_Colour[col][row], Cells_Rects[col][row])
            cell_x += CELL_SIZE
            Revealed_Cells[col][row] = 1 
        cell_y += CELL_SIZE

""" 
    Draw the cell we just passed in using the generated values and colours
"""
def drawCells(x, y):
    for row in range(0, GRID_SIZE):
        for col in range(0, GRID_SIZE):
            if (row == y and col == x):
                pygame.draw.rect(screen, Cells_Colour[col][row], Cells_Rects[col][row])
    drawGrid()

""" 
    Draw a grid over all the cells
"""            
def drawGrid():
    x = CELL_SIZE
    y = MIN_SCREEN_HEIGHT
    for row in range(0, GRID_SIZE):
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

    if (inChar == 1):
        renderChar(char, darkblue, x, y)
    elif (inChar == 2):
        renderChar(char, green, x, y)
    elif (inChar == 3):
        renderChar(char, red, x, y)
    elif (inChar == 4):
        renderChar(char, purple, x, y)
    elif (inChar == 5):
        renderChar(char, darkred, x, y)
    elif (inChar == 6):
        renderChar(char, iceblue, x, y)
    elif (inChar == 7):
        renderChar(char, black, x, y)
    elif (inChar == 8):
        renderChar(char, grey, x, y)
    else:
        renderChar(char, white, x, y)
    
def renderChar(inChar, colour, x, y):
    myFont = pygame.font.SysFont("None", 25)
    renderChar = myFont.render(str(inChar), 0, (colour))
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
    drawCells(x, y)
    displayChar(grid, x, y)
    return True

""" 
    Function that is called when a blank square (represented by 0) is clicked on
""" 
def blankGridWasHit(x, y):
    grid = Minefield[x][y]
    setGridColor(x, y, white) 
    drawCells(x, y)
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
    drawCells(x, y)
    displayChar(grid, x, y)

""" 
    Function that pulls apart the mouse input and assigns it to the correct function
    on left button click
"""
def leftMouseButton(pos):
    mouse_x = pos[0]
    mouse_y = pos[1]
    mouse_y = mouse_y - MIN_SCREEN_HEIGHT
    mouse_x = mouse_x // CELL_SIZE
    mouse_y = mouse_y // CELL_SIZE
    result = gridClicked(mouse_x, mouse_y)
    if result == True:
        return result
    
""" 
    Function that pulls apart the mouse input and assigns it to the correct function
    on right button click
"""
def rightMouseButton(pos):
    print("rightmousebutton")
    mouse_x = pos[0]
    mouse_y = pos[1]
    mouse_y = mouse_y - MIN_SCREEN_HEIGHT
    mouse_x = mouse_x // CELL_SIZE
    mouse_y = mouse_y // CELL_SIZE
    gridMarked(mouse_x, mouse_y)

""" 
    Function that returns whether or not a row has been revealed or not
"""
def coordinateIsRevealed(x, y):
    return Revealed_Cells[x][y]

""" 
    Function that checks to see if the coordinates are out of bounds
"""
def coordinateIsOutOfBounds(x, y):
    return x > MAX_COL_COUNT or x < MIN_SCREEN_WIDTH or y > MAX_ROW_COUNT or y < 0

""" 
    Is called on a left mouseclick - uses integer division to figure out which grid to access
    and then change the block colour and set the appropriate character
""" 
def gridClicked(x, y):
    if (coordinateIsOutOfBounds(x, y)):
        return
    elif (coordinateIsRevealed(x, y) != 1):
        return
    else:
        Revealed_Cells[x][y] = 0
        grid = Minefield[x][y]
        if (grid > 8):
            mineWasHit(x, y, grid)
            return True
        elif (grid == 0):
            blankGridWasHit(x, y)
        else:
            proximityGridWasHit(x, y)

""" 
    Is called on a right mouseclick - allows the user to mark a grid
"""   
def gridMarked(x, y):
    print("gridmarked")
    global MINE_COUNT
    if (coordinateIsOutOfBounds(x, y)):
        print(x)
        print(y)
        print("out of bounds bitch")
        return
    else:
        print("grid in bounds")
        if (Revealed_Cells[x][y] == 0):     # Grid has been revealed already so we can't do anything to it
            return
        elif (Revealed_Cells[x][y] == 1):   # Grid doesn't have anything on it so let's mark it - !
            drawCells(x, y)
            renderChar("!", white, x, y)
            Revealed_Cells[x][y] = 2
            MINE_COUNT -= 1
        elif (Revealed_Cells[x][y] == 2):   # Grid has been marked let's change it to a questionable - ?
            drawCells(x, y)
            renderChar("?", black, x, y)
            Revealed_Cells[x][y] = 3
            MINE_COUNT += 1
        elif (Revealed_Cells[x][y] == 3):   # Grid has been marked questionable so let's set it back to a blank
            drawCells(x, y)
            renderChar(" ", black, x, y)
            Revealed_Cells[x][y] = 1   

"""
    Display the Game Over Screen
"""   
def gameOverScreen():
    print ("endgame")
    loop = False
    while loop==False:
        screen.fill(black)
        for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    return False
                elif event.type == pygame.MOUSEBUTTONUP:
                    if event.button == 1:
                        loop = True
        pygame.display.flip()
        pygame.time.delay(100)
    return True

"""
    Start the game
"""    
def startGame():
    intializeCells()
    seedMines()
    drawGrid()
    loop = False
    TIMER = 1
    pygame.time.set_timer(TIMER, 1000)
    while loop==False:
        if pygame.event.get(TIMER):
            global TIME
            TIME += 1
        drawMenuBar(TIME)
        for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    return False
                elif event.type == pygame.MOUSEBUTTONUP:
                    pos = pygame.mouse.get_pos()
                    if event.button == 1:   # Left button click detected
                        result = leftMouseButton(pos)
                        if result == True:
                            loop = True
                    elif event.button == 3: # Right button click detected
                        rightMouseButton(pos)
        pygame.display.flip()
        pygame.time.delay(100)
    return True

"""
    Display the Title Screen
"""        
def titleScreen():
    global MINE_COUNT
    title_width = 200
    title_height = 250
    
    button_width = 120
    button_height = 35
    button_border = 6
    
    border = 5
    
    loop = False
    drawGrid()
    drawMenuBar(TIME)
    while loop==False:
        titleFont = pygame.font.Font('freesansbold.ttf', 25)
        buttonFont = pygame.font.Font('freesansbold.ttf', 18)
        menuBackground_border = pygame.Rect((MAX_SCREEN_WIDTH - title_width) // 2, ((MAX_SCREEN_HEIGHT - title_height) // 2) + (MENU_BAR_HEIGHT // 2), title_width, title_height)
        pygame.draw.rect(screen, black, menuBackground_border)
        menuBackground_box = pygame.Rect(((MAX_SCREEN_WIDTH - title_width) // 2) + border, 
                                         (((MAX_SCREEN_HEIGHT - title_height) // 2) + (MENU_BAR_HEIGHT // 2)) + border, 
                                         title_width - border*2, title_height - border*2)
        pygame.draw.rect(screen, lightgrey, menuBackground_box)
        title = titleFont.render('Minesweeper', True, black)
        titlePos = title.get_rect()
        titlePos.center = (MAX_SCREEN_WIDTH // 2, menuBackground_box.centery - (title_height * 0.35))
        screen.blit(title, titlePos)
        
        beginner = pygame.Rect(menuBackground_box.centerx - (button_width // 2), menuBackground_box.centery - 10, button_width, button_height)
        pygame.draw.rect(screen, black, beginner)
        beginner_border = pygame.Rect(menuBackground_box.centerx - (button_width // 2) + (button_border/2), menuBackground_box.centery - 10 + (button_border/2), 
                                      button_width - button_border, button_height - button_border)
        pygame.draw.rect(screen, white, beginner_border)
        begginerText = buttonFont.render('Beginner', True, black)
        beginnerRect = begginerText.get_rect()
        beginnerRect.center = beginner.center
        screen.blit(begginerText, beginnerRect)
        
        intermediate = pygame.Rect(menuBackground_box.centerx - (button_width // 2), menuBackground_box.centery + 30, button_width, button_height)
        pygame.draw.rect(screen, black, intermediate)
        intermediate_border = pygame.Rect(menuBackground_box.centerx - (button_width // 2) + (button_border/2), menuBackground_box.centery + 30 + (button_border/2), 
                                      button_width - button_border, button_height - button_border)
        pygame.draw.rect(screen, white, intermediate_border)
        intermediateText = buttonFont.render('Intermediate', True, black)
        intermediateRect = intermediateText.get_rect()
        intermediateRect.center = intermediate.center
        screen.blit(intermediateText, intermediateRect)
        
        expert = pygame.Rect(menuBackground_box.centerx - (button_width // 2), menuBackground_box.centery + 70, button_width, button_height)
        pygame.draw.rect(screen, black, expert)
        expert_border = pygame.Rect(menuBackground_box.centerx - (button_width // 2) + (button_border/2), menuBackground_box.centery + 70 + (button_border/2), 
                                          button_width - button_border, button_height - button_border)
        pygame.draw.rect(screen, white, expert_border)
        expertText = buttonFont.render('Expert', True, black)
        expertRect = expertText.get_rect()
        expertRect.center = expert.center
        screen.blit(expertText, expertRect)
        
        for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    return False
                elif event.type == pygame.MOUSEBUTTONUP:
                    pos = pygame.mouse.get_pos()
                    if event.button == 1:   # Left button click detected
                        mouse_x = pos[0]
                        mouse_y = pos[1]
                        if (mouse_x > beginnerRect.centerx-(button_width/2) and 
                            mouse_x < beginnerRect.centerx+(button_width/2) and
                            mouse_y > beginnerRect.centery-(button_height/2) and
                            mouse_y < beginnerRect.centery+(button_height/2)):
                            print ("beginner")
                            MINE_COUNT = 5
                            loop = True
                        elif (mouse_x > intermediateRect.centerx-(button_width/2) and 
                            mouse_x < intermediateRect.centerx+(button_width/2) and
                            mouse_y > intermediateRect.centery-(button_height/2) and
                            mouse_y < intermediateRect.centery+(button_height/2)):
                            print ("intermediate")
                            MINE_COUNT = 10
                            loop = True
                        elif (mouse_x > expertRect.centerx-(button_width/2) and 
                            mouse_x < expertRect.centerx+(button_width/2) and
                            mouse_y > expertRect.centery-(button_height/2) and
                            mouse_y < expertRect.centery+(button_height/2)):
                            print ("expert")
                            MINE_COUNT = 20
                            loop = True

        pygame.display.flip()
        pygame.time.delay(100)
    return True

def drawMenuBar(time):
    box_size = 50
    border_size = 2
    top_offset = 3
    combined = border_size + top_offset
    minecounterbox_x = (MENU_BAR_WIDTH // 2) - (box_size // 2)
    
    # Draw the actual bar
    bar = pygame.Rect(0, 0, MENU_BAR_WIDTH, MENU_BAR_HEIGHT)
    pygame.draw.rect(screen, grey, bar)
    
    # Draw the timer box
    timer_border = pygame.Rect(top_offset, top_offset, box_size, (MENU_BAR_HEIGHT-(top_offset*2)))
    timer_box = pygame.Rect(combined, top_offset+border_size, box_size-(border_size*2), (MENU_BAR_HEIGHT-(combined*2)))
    pygame.draw.rect(screen, black, timer_border)
    pygame.draw.rect(screen, white, timer_box)
    
    # Draw the minecounter box
    minecounter_border = pygame.Rect(minecounterbox_x, top_offset, box_size, (MENU_BAR_HEIGHT-6))
    minecounter_box = pygame.Rect(minecounterbox_x+border_size, combined, box_size-(border_size*2), (MENU_BAR_HEIGHT-(combined*2)))
    pygame.draw.rect(screen, black, minecounter_border)
    pygame.draw.rect(screen, white, minecounter_box)
    
    # Update the minecount
    menufont = pygame.font.Font('freesansbold.ttf', 20)
    mineSurf = menufont.render(str(MINE_COUNT), True, black)
    mineRect = mineSurf.get_rect()
    mineRect.center = (MENU_BAR_WIDTH // 2, combined+((MENU_BAR_HEIGHT-(combined*2))/2))
    screen.blit(mineSurf, mineRect)
    
    # Update the timer
    timerSurf = menufont.render(str(TIME), True, black)
    timerRect = timerSurf.get_rect()
    timerRect.center = ((combined+box_size/2), combined+((MENU_BAR_HEIGHT-(combined*2))/2))
    screen.blit(timerSurf, timerRect)    
            
""" 
    Main method
""" 
def main():
    screen.fill(blue)
    
    result = titleScreen()
    if result==False:
        return
    
    result = startGame()
    if result==False:
        return
    
    result = gameOverScreen()
    if result==False:
        return
    pygame.quit()

if __name__ == '__main__':
    main()
