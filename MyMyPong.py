import pygame
import sys
import time

from pygame import display

pygame.init()

WIDTH = 800
HEIGHT = 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
DISPLAYSURF = pygame.display.set_mode((WIDTH, HEIGHT))
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

PADDLE_HEIGHT = 100
PADDLE_WIDTH = 20

paddleLeft = 20
paddleTop = 20

BALL_SIZE = 10

SPEED_INCREASE = 0
BALL_SPEED_X = 3
BALL_SPEED_Y = 3

ballLeft = int(WIDTH/2)
ballTop = int(HEIGHT/2)

FPSCLOCK = pygame.time.Clock()
FPS = 60
clock = pygame.time.Clock()
score = 0
FONT = pygame.font.Font(None, 20)

paused = False   # ← NEW (pause flag)

def draw_screen(ballTop, ballLeft, paddleTop):
    DISPLAYSURF.fill(BLACK)
    pygame.draw.circle(DISPLAYSURF, WHITE, (ballLeft, ballTop), BALL_SIZE)
    pygame.draw.rect(DISPLAYSURF, WHITE, (paddleLeft, paddleTop, PADDLE_WIDTH, PADDLE_HEIGHT))

def make_text(text, color, left, top):
    textSurface = FONT.render(text, True, color)
    textRect = textSurface.get_rect()
    textRect.topleft = (left, top)
    return textSurface, textRect

def reset_game():
    return 20, 20, int(WIDTH/2), int(HEIGHT/2), 0, 3, 3


def game_over():
    gameOverSurf, gameOverRect = make_text("GAME OVER", WHITE, WIDTH // 2 - 60, HEIGHT // 2 - 20)
    DISPLAYSURF.blit(gameOverSurf, gameOverRect)
    pygame.display.update()
    pygame.time.wait(1000)
    reset_game()

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                pygame.quit()
                sys.exit()
            if event.key == pygame.K_r:
                paddleLeft, paddleTop, ballLeft, ballTop, score, BALL_SPEED_X, BALL_SPEED_Y = reset_game()
            if event.key == pygame.K_p:
                paused = not paused

    if not paused:
        keys = pygame.key.get_pressed()
        if keys[pygame.K_UP] and paddleTop>0:
            paddleTop -= 4
        if keys[pygame.K_DOWN] and paddleTop<HEIGHT-PADDLE_HEIGHT:
            paddleTop += 4

        ballRect = pygame.Rect(ballLeft - BALL_SIZE, ballTop - BALL_SIZE, BALL_SIZE * 2, BALL_SIZE * 2)
        paddleRect = pygame.Rect(paddleLeft, paddleTop, PADDLE_WIDTH, PADDLE_HEIGHT)

        ballLeft += BALL_SPEED_X
        ballTop += BALL_SPEED_Y

        if ballTop<=0:
            BALL_SPEED_Y *= -1

        if ballTop+BALL_SIZE>=HEIGHT:
            BALL_SPEED_Y *= -1

        if ballLeft>=WIDTH-BALL_SIZE:
            BALL_SPEED_X *= -1

        if paddleRect.colliderect(ballRect):
            score += 1
            ballLeft = paddleLeft + PADDLE_WIDTH + BALL_SIZE
            BALL_SPEED_X *= -1

            BALL_SPEED_X *= 1.2
            BALL_SPEED_Y *= 1.2

        if ballLeft <= 0:
            game_over()
            reset_game()

    draw_screen(ballTop, ballLeft, paddleTop)
    scoreSurf, scoreText = make_text(f"Score {score}", WHITE, 20, 20)
    DISPLAYSURF.blit(scoreSurf, scoreText)

    if paused:
        pauseSurf, pauseRect = make_text("PAUSED", WHITE, WIDTH // 2 - 60, HEIGHT // 2 - 20)
        DISPLAYSURF.blit(pauseSurf, pauseRect)

    pygame.display.update()
    FPSCLOCK.tick(60)