import random, pygame, sys
from pygame.locals import *

pygame.init()

WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600
FPS=30

GRAY = (128, 128, 128)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
WHITE = (255, 255, 255)

BOARD_WIDTH = 15
BOARD_HEIGHT = 5

CELL_SIZE = 30

X_MARGIN = int((WINDOW_WIDTH-(CELL_SIZE*BOARD_WIDTH))/2)
Y_MARGIN = int((WINDOW_HEIGHT-(CELL_SIZE*BOARD_HEIGHT))/2)

FONT = pygame.font.Font('freesansbold.ttf', 20)
DISPLAY = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))

LEFT = 'left'
RIGHT = 'right'
UP = 'up'
DOWN = 'down'

def makeText(text, color, bgcolor, left, top):
    textSurface = FONT.render(text, True, color, bgcolor)
    textRect = textSurface.get_rect()
    textRect.topleft = (left, top)
    return textSurface, textRect

def getLeftTopOfBox(boxx, boxy):
    left = X_MARGIN + (boxx * CELL_SIZE)
    top = Y_MARGIN + (boxy * CELL_SIZE)
    return left, top


def getBoxAtPixel(mousex, mousey):
    for boxx in range(BOARD_WIDTH):
        for boxy in range(BOARD_HEIGHT):
            left, top = getLeftTopOfBox(boxx, boxy)
            boxRect = pygame.Rect(left, top, CELL_SIZE, CELL_SIZE)
            if boxRect.collidepoint(mousex, mousey):
                return boxx, boxy
    return None, None


def isValidMove(direction, player):
    if direction == LEFT:
        if player[0] - 1 >= 0:
            return True
        else:
            return False
    elif direction == RIGHT:
        if player[0] + 1 < BOARD_WIDTH:
            return True
        else:
            return False
    elif direction == UP:
        if player[1] - 1 >= 0:
            return True
        else:
            return False
    else:
        if player[1] + 1 < BOARD_HEIGHT:
            return True
        else:
            return False


def errorMessage(text):
    error_move_surf, error_move_rect = makeText(text, RED, GRAY, WINDOW_WIDTH / 2, 15)
    DISPLAY.blit(error_move_surf, error_move_rect)
    pygame.display.update()
    pygame.time.wait(500)


def drawBoard(player, exit, ):
    DISPLAY.fill(GRAY)
    for x in range(BOARD_WIDTH):
        for y in range(BOARD_HEIGHT):
            left, top = getLeftTopOfBox(x, y)
            pygame.draw.rect(DISPLAY, WHITE, (left, top, CELL_SIZE, CELL_SIZE), 1)
            if (x, y) == exit:
                pygame.draw.rect(DISPLAY, GREEN, (left+5, top+5, CELL_SIZE-10, CELL_SIZE-10))
            if (x, y) == player:
                pygame.draw.rect(DISPLAY, BLUE, (left+5, top+5, CELL_SIZE-10, CELL_SIZE-10))



def drawTraps(traps):
    for x in range(BOARD_WIDTH):
        for y in range(BOARD_HEIGHT):
            left, top = getLeftTopOfBox(x, y)
            if (x, y) in traps:
                pygame.draw.rect(DISPLAY, RED, (left + 5, top + 5, CELL_SIZE - 10, CELL_SIZE - 10))


def main():
    FPSCLOCK = pygame.time.Clock()

    lives = 3
    moves = 0


    player = (1, 1)
    traps = [(2, 2), (3, 4)]
    exit = (10, 4)

    game_state = "REVEAL"


    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if game_state == "PLAY":
                if event.type == KEYDOWN:
                    if event.key == K_ESCAPE:
                        pygame.quit()
                        sys.exit()
                    if event.key == K_r:
                        player = (0, 0)
                        lives = 3
                        moves = 0

                    elif event.key == K_LEFT:
                        if (player[0] - 1, player[1]) in traps:
                            if lives == 1:
                                errorMessage("Game Over!")
                                pygame.quit()
                                sys.exit()
                            else:
                                errorMessage("Stepped on trap!")
                                player = (0, 0)
                                lives -= 1
                        elif isValidMove(LEFT, player):
                            player = (player[0] - 1, player[1])
                            moves += 1
                        else:
                            errorMessage("Invalid move")

                    elif event.key == K_RIGHT:
                        if (player[0] + 1, player[1]) in traps:
                            if lives == 1:
                                errorMessage("Game Over!")
                                pygame.quit()
                                sys.exit()
                            else:
                                errorMessage("Stepped on trap!")
                                player = (0, 0)
                                lives -= 1
                        elif isValidMove(RIGHT, player):
                            player = (player[0] + 1, player[1])
                            moves += 1
                        else:
                            errorMessage("Invalid move")

                    elif event.key == K_UP:
                        if (player[0], player[1] - 1) in traps:
                            if lives == 1:
                                errorMessage("Game Over!")
                                pygame.quit()
                                sys.exit()
                            else:
                                errorMessage("Stepped on trap!")
                                player = (0, 0)
                                lives -= 1
                        elif isValidMove(UP, player):
                            player = (player[0], player[1] - 1)
                            moves += 1
                        else:
                            errorMessage("Invalid move")

                    elif event.key == K_DOWN:
                        if (player[0], player[1] + 1) in traps:
                            if lives == 1:
                                errorMessage("Game Over!")
                                pygame.quit()
                                sys.exit()
                            else:
                                errorMessage("Stepped on trap!")
                                player = (0, 0)
                                lives -= 1
                        elif isValidMove(DOWN, player):
                            player = (player[0], player[1] + 1)
                            moves += 1
                        else:
                            errorMessage("Invalid move")
            else:
                drawBoard(player, exit)
                drawTraps(traps)
                pygame.display.update()
                pygame.time.wait(1000)
                game_state = "PLAY"

        drawBoard(player, exit)
        pygame.display.update()
        FPSCLOCK.tick(FPS)



if __name__ == "__main__":
    main()