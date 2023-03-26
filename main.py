import pygame, random, sys

pygame.init()

WINDOWWIDTH = 800
WINDOWHEIGHT = 600
CELLSIZE = 20 # in pixel

fps = 12

tailLengthPerApple = 3 # how many cells the snake should grow after eating an apple

steer = False
# steer = True:
#   Key A - steer left
#   Key D - steer right
# steer = False:
#   Key W - Turn up
#   Key A - Turn left
#   Key s - Turn down
#   Key D - Turn right


# Colors

#             R    G    Bad
WHITE     = (255, 255, 255)
BLACK     = (  0,   0,   0)
RED       = (255,   0,   0)
GREEN     = (  0, 255,   0)
BLUEGREEN = (  0,  50, 100)
DARKGREEN = (  0, 100,   0)
DARKGRAY  = ( 50,  50,  50)
NEARBLACK = ( 20,  20,  20)
BGCOLOR   = NEARBLACK

UP = 'up'
DOWN = 'down'
LEFT = 'left'
RIGHT = 'right'

HEAD = 0 # syntactic sugar: index of the snake's head

assert WINDOWWIDTH % CELLSIZE == 0, "Window width must be a multiple of cell size."
assert WINDOWHEIGHT % CELLSIZE == 0, "Window height must be a multiple of cell size."
CELLWIDTH = int(WINDOWWIDTH / CELLSIZE)
CELLHEIGHT = int(WINDOWHEIGHT / CELLSIZE)



def main():
    global fpsCLOCK, DISPLAYSURF, BASICFONT

    fpsCLOCK = pygame.time.Clock()
    DISPLAYSURF = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT)) #,pygame.FULLSCREEN)
    BASICFONT = pygame.font.Font('freesansbold.ttf', 18)
    pygame.display.set_caption('Snake')
    pygame.mouse.set_visible(0)

    showStartScreen()
    while True:
        runGame()
        showGameOverScreen()


def runGame():
    global notdeleted,snakeCoords,startx,starty,direction,fps
    # set a random start point.
    startx = random.randint(20, CELLWIDTH - 10)
    starty = random.randint(20, CELLHEIGHT - 10)
    snakeCoords = [{'x': startx,'y': starty}]
    direction = RIGHT
    notdeleted = 3

    # start the apple in a random place.
    apple = getRandomLocation()

    while True: # main game loop
        for event in pygame.event.get(): # event handling loop
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.KEYDOWN:
                if steer:
                    if event.key == pygame.K_a:# and direction != RIGHT:
                        if direction == UP:
                            direction = LEFT
                        elif direction == RIGHT:
                            direction = UP
                        elif direction == DOWN:
                            direction = RIGHT
                        elif direction == LEFT:
                            direction = DOWN
                    if event.key == pygame.K_d:# and direction != LEFT:
                        if direction == UP:
                            direction = RIGHT
                        elif direction == RIGHT:
                            direction = DOWN
                        elif direction == DOWN:
                            direction = LEFT
                        elif direction == LEFT:
                            direction = UP
                else:
                    if event.key == pygame.K_w and direction != DOWN:
                        direction = UP
                    elif event.key == pygame.K_a and direction != RIGHT:
                        direction = LEFT
                    elif event.key == pygame.K_s and direction != UP:
                        direction = DOWN
                    elif event.key == pygame.K_d and direction != LEFT:
                        direction = RIGHT

                if event.key == pygame.K_UP:
                    fps += 1
                elif event.key == pygame.K_DOWN:
                    fps -= 1
                elif event.key == pygame.K_ESCAPE:
                    terminate()

        for snakeBody in snakeCoords[1:]:
            if snakeBody['x'] == snakeCoords[HEAD]['x'] and snakeBody['y'] == snakeCoords[HEAD]['y']:
                return # game over

        # move the snake by adding a segment in the direction it is moving
        if direction == UP:
            newHead = {'x': snakeCoords[HEAD]['x'], 'y': snakeCoords[HEAD]['y'] - 1}
        elif direction == DOWN:
            newHead = {'x': snakeCoords[HEAD]['x'], 'y': snakeCoords[HEAD]['y'] + 1}
        elif direction == LEFT:
            newHead = {'x': snakeCoords[HEAD]['x'] - 1, 'y': snakeCoords[HEAD]['y']}
        elif direction == RIGHT:
            newHead = {'x': snakeCoords[HEAD]['x'] + 1, 'y': snakeCoords[HEAD]['y']}
        snakeCoords.insert(0, newHead)


        # check if snake has eaten an apple
        if snakeCoords[HEAD]['x'] == apple['x'] and snakeCoords[HEAD]['y'] == apple['y']:
            notdeleted = tailLengthPerApple
            # don't remove snake's tail segment
            apple = getRandomLocation() # set a new apple somewhere
        else:
            if notdeleted <= 0:
                del snakeCoords[-1] # remove snake's tail segment
        notdeleted -= 1

        # check if the snake has hit itself or the edge
        if snakeCoords[HEAD]['x'] == -1 or snakeCoords[HEAD]['x'] == CELLWIDTH or snakeCoords[HEAD]['y'] == -1 or snakeCoords[HEAD]['y'] == CELLHEIGHT:
            return # Game Overs


        DISPLAYSURF.fill(BGCOLOR)
        drawGrid()
        drawSnake(snakeCoords)
        drawApple(apple)
        drawScore(len(snakeCoords) - 3)
        pygame.display.update()
        fpsCLOCK.tick(fps)

def drawPressKeyMsg():
    pressKeySurf = BASICFONT.render('Press a key to play.', True, GREEN)
    pressKeyRect = pressKeySurf.get_rect()
    pressKeyRect.topleft = (WINDOWWIDTH - 200, WINDOWHEIGHT - 30)
    DISPLAYSURF.blit(pressKeySurf, pressKeyRect)



# KRT 14/06/2012 rewrite event detection to deal with mouse use
def checkForKeyPress():
    for event in pygame.event.get():
        if event.type == pygame.QUIT:      #event is quit
            terminate()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:   #event is escape key
                terminate()
            else:
                return event.key   #key found return with it
    # no quit or key events in queue so return None
    return None


def showStartScreen():
    titleFont = pygame.font.Font('freesansbold.ttf', 100)
    titleSurf1 = titleFont.render('Snake', True, WHITE, DARKGREEN)
    titleSurf2 = titleFont.render('--Snake--', True, GREEN)

    degrees1 = 0
    degrees2 = 0

#KRT 14/06/2012 rewrite event detection to deal with mouse use
    pygame.event.get()  #clear out event queue

    while True:
        DISPLAYSURF.fill(BGCOLOR)
        rotatedSurf1 = pygame.transform.rotate(titleSurf1, degrees1)
        rotatedRect1 = rotatedSurf1.get_rect()
        rotatedRect1.center = (WINDOWWIDTH / 2, WINDOWHEIGHT / 2)
        DISPLAYSURF.blit(rotatedSurf1, rotatedRect1)

        rotatedSurf2 = pygame.transform.rotate(titleSurf2, degrees2)
        rotatedRect2 = rotatedSurf2.get_rect()
        rotatedRect2.center = (WINDOWWIDTH / 2, WINDOWHEIGHT / 2)
        DISPLAYSURF.blit(rotatedSurf2, rotatedRect2)

        drawPressKeyMsg()
#KRT 14/06/2012 rewrite event detection to deal with mouse use
        if checkForKeyPress():
            return
        pygame.display.update()
        fpsCLOCK.tick(fps)
        degrees1 += 3 # rotate by 3 degrees each frame
        degrees2 += 7 # rotate by 7 degrees each frame


def terminate():
    pygame.quit()
    sys.exit()


def getRandomLocation():
    return {'x': random.randint(0, CELLWIDTH - 2), 'y': random.randint(0, CELLHEIGHT - 2)}


def showGameOverScreen():
    gameOverFont = pygame.font.Font('freesansbold.ttf', 150)
    gameSurf = gameOverFont.render('Game', True, WHITE)
    overSurf = gameOverFont.render('Over', True, WHITE)
    gameRect = gameSurf.get_rect()
    overRect = overSurf.get_rect()
    gameRect.midtop = (WINDOWWIDTH / 2, 100)
    overRect.midtop = (WINDOWWIDTH / 2, gameRect.height + 10 + 125)

    DISPLAYSURF.blit(gameSurf, gameRect)
    DISPLAYSURF.blit(overSurf, overRect)
    drawPressKeyMsg()
    pygame.display.update()
    pygame.time.wait(500)
#KRT 14/06/2012 rewrite event detection to deal with mouse use
    pygame.event.get()  #clear out event queue
    while True:
        if checkForKeyPress():
            return
#KRT 12/06/2012 reduce processor loading in gameover screen.
        pygame.time.wait(100)

def drawScore(score):
    scoreSurf = BASICFONT.render('Score: %s' % (score), True, WHITE)
    scoreRect = scoreSurf.get_rect()
    scoreRect.topleft = (WINDOWWIDTH - 120, 10)
    DISPLAYSURF.blit(scoreSurf, scoreRect)


def drawSnake(snakeCoords):
    z = 0
    for coord in snakeCoords:
        z += 1
        if z == 4:
            pygame.draw.rect(DISPLAYSURF, BLUEGREEN, pygame.Rect(coord['x'] * CELLSIZE, coord['y'] * CELLSIZE, CELLSIZE, CELLSIZE))
            z = 0
        else:
            snakeSegmentRect = pygame.Rect(coord['x'] * CELLSIZE, coord['y'] * CELLSIZE, CELLSIZE, CELLSIZE)
            pygame.draw.rect(DISPLAYSURF, DARKGREEN, snakeSegmentRect)
    snakeSegmentRect = pygame.Rect(snakeCoords[HEAD]['x'] * CELLSIZE, snakeCoords[HEAD]['y'] * CELLSIZE, CELLSIZE, CELLSIZE)
    pygame.draw.rect(DISPLAYSURF, GREEN, snakeSegmentRect)


def drawApple(coord):
    x = coord['x'] * CELLSIZE
    y = coord['y'] * CELLSIZE
    appleRect = pygame.Rect(x, y, CELLSIZE, CELLSIZE)
    pygame.draw.rect(DISPLAYSURF, RED, appleRect)


def drawGrid():
    for x in range(0, WINDOWWIDTH, CELLSIZE): # draw vertical lines
        pygame.draw.line(DISPLAYSURF, BLACK, (x, 0), (x, WINDOWHEIGHT))
    for y in range(0, WINDOWHEIGHT, CELLSIZE): # draw horizontal lines
        pygame.draw.line(DISPLAYSURF, BLACK, (0, y), (WINDOWWIDTH, y))


if __name__ == '__main__':
    while True:
        main()
