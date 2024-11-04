import pygame
import math
import sys
import random
from pygame.locals import *
import os
import time

# Game Initialization
pygame.init()

# Game Window Alignment
os.environ['SDL_VIDEO_CENTERED'] = '1'

# Game Resolution
screen_width = 900
screen_height = 720
screen = pygame.display.set_mode((screen_width, screen_height))


# Text Formatting
def text_format(message, textfont, textsize, textcolour):
    newFont = pygame.font.Font((textfont), textsize)
    newText = newFont.render(message, 0, textcolour)
    return newText


# Colours
white = (255, 255, 255)
black = (0, 0, 0)
grey = (50, 50, 50)
red = (255, 0, 0)
green = (0, 255, 0)
blue = (0, 0, 255)
yellow = (255, 255, 0)
gold = (255, 215, 0)

# Game Font
font = 'Absolute_Zero.otf'

# Game Framerate
clock = pygame.time.Clock()
FPS = 30


### Background Animation ###
class Animation(pygame.sprite.Sprite):
    def __init__(self):
        super(Animation, self).__init__()

        self.images = []
        self.images.append(pygame.image.load(('Road1.png')).convert_alpha())
        self.images.append(pygame.image.load(('Road2.png')).convert_alpha())
        self.images.append(pygame.image.load(('Road3.png')).convert_alpha())
        self.images.append(pygame.image.load(('Road4.png')).convert_alpha())
        self.images.append(pygame.image.load(('Road5.png')).convert_alpha())
        self.images.append(pygame.image.load(('Road6.png')).convert_alpha())
        self.images.append(pygame.image.load(('Road7.png')).convert_alpha())
        self.images.append(pygame.image.load(('Road8.png')).convert_alpha())
        self.index = 0
        self.rect = pygame.Rect(0, 0, 900, 720)

    def update(self):
        if self.index >= len(self.images):
            self.index = 0
        self.image = self.images[self.index]
        pygame.time.wait(2)
        self.index += 1


### Sound Effects ###
def crash_sound():
    crash_s = pygame.mixer.Sound(('Crash.wav'))
    pygame.mixer.Sound.play(crash_s)


def coin_sound():
    coinCollect_sound = pygame.mixer.Sound(('Coin Collect.wav'))
    pygame.mixer.Sound.play(coinCollect_sound)


### Car ###
def car(x, y):
    carImage = pygame.image.load(('Car.png')).convert_alpha()
    car = pygame.transform.scale(carImage, (100, 200))
    screen.blit(car, (x, y))


### Coin ###
def coin(x, y):
    coin = []
    coinImage = pygame.image.load(('Coin.png')).convert_alpha()
    coin = pygame.transform.scale(coinImage, (60, 60))
    screen.blit(coin, (x, y))


### Roadblock ###
def roadblock(x, y):
    roadblockImage = pygame.image.load(('Roadblock.png')).convert_alpha()
    roadblock = pygame.transform.scale(roadblockImage, (100, 100))
    screen.blit(roadblock, (x, y))


### Make Collisions ###
def coin_collect(coinX, coinY, carX, carY):
    distance = math.sqrt((math.pow(coinX - carX, 2)) + (math.pow(coinY - carY, 2)))
    if distance < 80:
        coin_sound()
        return True
    else:
        return False


def crashed(roadblockX, roadblockY, carX, carY):
    distance = math.sqrt((math.pow(roadblockX - carX, 2)) + (math.pow(roadblockY - carY, 2)))
    if distance < 100:
        crash_sound()
        return True
    else:
        return False


def score(x, y, score_value):
    scoreImage = pygame.image.load(('Score Display.png')).convert_alpha()
    score_display = pygame.transform.scale(scoreImage, (380, 150))
    screen.blit(score_display, (250, -50))
    score = text_format('Score: ' + str(score_value), font, 35, gold)
    screen.blit(score, (x, y))


### Game Over ###
def game_over():
    game_text = text_format('Game Over!', font, 70, red)
    screen.blit(game_text, (150, 250))
    pygame.display.update()
    pygame.time.wait(3000)


### Game Controls ###
def controls_menu():
    esc_keyImage = pygame.image.load(('ESC Key.png')).convert_alpha()
    esc_key = pygame.transform.scale(esc_keyImage, (45, 45))
    text_esc = text_format('Main Menu', font, 15, white)
    screen.blit(esc_key, (805, 520))
    screen.blit(text_esc, (660, 530))

    spacebarImage = pygame.image.load(('Spacebar.png')).convert_alpha()
    space_key = pygame.transform.scale(spacebarImage, (45, 45))
    text_space = text_format('Pause Game', font, 15, white)
    screen.blit(space_key, (805, 460))
    screen.blit(text_space, (660, 480))

    right_keyImage = pygame.image.load(('Right Key.png')).convert_alpha()
    right_arrow = pygame.transform.scale(right_keyImage, (45, 45))
    text_right = text_format('Move Right', font, 15, white)
    screen.blit(right_arrow, (805, 590))
    screen.blit(text_right, (660, 600))

    left_keyImage = pygame.image.load(('Left Key.png')).convert_alpha()
    left_key = pygame.transform.scale(left_keyImage, (45, 45))
    text_left = text_format('Move Left', font, 15, white)
    screen.blit(left_key, (805, 660))
    screen.blit(text_left, (660, 670))


### Game Started ###
def game_start():
    # Score
    score_value = 0

    # Car Attributes
    car_vel = 7
    carX = 540
    carY = 500

    # Coin Attributes
    coin_vel = 10
    coinX = random.randint(100, 700)
    coinY = 0

    # Roadblock Attributes
    roadblock_vel = 10
    roadblockX = random.randint(100, 700)
    roadblockY = 0

    backg = Animation()
    backg_group = pygame.sprite.Group(backg)

    loop = 1

    while loop:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                loop = 0

        backg_group.update()
        screen.fill(black)
        backg_group.draw(screen)

        # Coin Movement
        coinY += coin_vel

        # Roadblock Movement
        roadblockY += roadblock_vel

        # End Game if Crashed
        collision = crashed(roadblockX, roadblockY, carX, carY)
        if collision:
            # pygame.mixer.music.stop()
            crash_sound()
            game_over()
            break

        # Re-generate Coins
        coin_collected = coin_collect(coinX, coinY, carX, carY)
        if coin_collected:
            if coinX == roadblockX:
                coinX = random.randint(100, 700)
            else:
                coinX = random.randint(100, 700)
            coinY = 0
            score_value += 1

        # Roadblock and Border
        if roadblockY + roadblock_vel > 700:
            roadblockX = random.randint(100, 700)
            roadblockY = 0

        # Coin and Border
        if coinY + coin_vel > 700:
            coinX = random.randint(100, 700)
            if coinX == roadblockX:
                coinX = random.randint(100, 700)
            coinY = 0

        keys_pressed = pygame.key.get_pressed()
        if keys_pressed[pygame.K_LEFT] and carX - car_vel > 100:
            carX -= car_vel

        elif keys_pressed[pygame.K_RIGHT] and carX + car_vel < 700:
            carX += car_vel

        elif keys_pressed[pygame.K_SPACE]:
            controls_menu()
            time.sleep(0.5)

        elif keys_pressed[pygame.K_ESCAPE]:
            screen.fill(black)
            main_menu()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

        coin(coinX, coinY)
        car(carX, carY)
        roadblock(roadblockX, roadblockY)
        score(310, 7, score_value)

        pygame.display.update()


### Main Menu ###
def main_menu():
    menu = True
    selected = "start"

    while menu:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    selected = "start"
                elif event.key == pygame.K_DOWN:
                    selected = "quit"
                elif event.key == pygame.K_RETURN:
                    if selected == "start":
                        print('GAME STARTED')
                        game_start()
                    elif selected == "quit":
                        pygame.quit()
                        quit()

        # Main Menu UI
        bg = pygame.image.load(('Menu.png'))
        menu_i = pygame.transform.scale(bg, (900, 720))
        screen.blit(menu_i, (0, 0), (0, 0, screen_width, screen_height))

        title = text_format('Car Game', font, 75, yellow)

        if selected == 'start':
            text_start = text_format('START', font, 55, white)
        else:
            text_start = text_format('START', font, 40, white)
        if selected == 'quit':
            text_quit = text_format('QUIT', font, 55, red)
        else:
            text_quit = text_format('QUIT', font, 40, red)

        title_rect = title.get_rect()
        start_rect = text_start.get_rect()
        quit_rect = text_quit.get_rect()

        # Main Menu Text
        screen.blit(title, (screen_width / 2 - (title_rect[2] / 2), 100))
        screen.blit(text_start, (screen_width / 2 - (start_rect[2] / 2), 480))
        screen.blit(text_quit, (screen_width / 2 - (quit_rect[2] / 2), 580))
        pygame.display.update()
        clock.tick(FPS)
        pygame.display.set_caption('Car Game')


# Initialize the Game
main_menu()

pygame.quit()
quit()
