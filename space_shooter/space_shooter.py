import turtle
import math
import random

import os
os.environ["PYGAME_HIDE_SUPPORT_PROMPT"] = "1"

try:
    import pygame
    pygame.mixer.init()
    SOUND_ENABLED = True
except Exception:
    SOUND_ENABLED = False


SHOOT_SOUND = "assets/laser.mp3"
ENEMY_DEATH_SOUND = "assets/zombie_death.mp3"


def load_sound(path):
    if not SOUND_ENABLED or not os.path.exists(path):
        return None

    try:
        return pygame.mixer.Sound(path)
    except Exception:
        return None


laser_sfx = load_sound(SHOOT_SOUND)
zombie_death_sfx = load_sound(ENEMY_DEATH_SOUND)


# =========================
# Asset Paths
# =========================
PLAYER_IMG = "assets/Spaceship.gif"
ENEMY_IMG = "assets/Invaders.gif"
LASER_IMG = "assets/Laser.gif"
BG_IMG = "assets/Space.gif"

# =========================
# Screen Setup
# =========================
wp = turtle.Screen()
wp.setup(width=700, height=700)
wp.title("Space Shooter")
wp.bgcolor("black")
wp.bgpic(BG_IMG)
wp.tracer(0)

# Register Shapes
turtle.register_shape(PLAYER_IMG)
turtle.register_shape(ENEMY_IMG)
turtle.register_shape(LASER_IMG)

# =========================
# Constants
# =========================
BORDER_LEFT = -300
BORDER_RIGHT = 300
BORDER_TOP = 300
BORDER_BOTTOM = -300

PLAYER_Y = -250
PLAYER_SPEED = 18

ENEMY_START_SPEED = 3
ENEMY_DROP = 35
NUMBER_OF_ENEMIES = 5

LASER_SPEED = 22

# =========================
# Game State
# =========================
player = None
laser = None
score_pen = None
message_pen = None
border_pen = None

enemies = []

score = 0
enemy_speed = ENEMY_START_SPEED
laser_state = "ready"
game_running = False


# =========================
# Sound
# =========================
def play_sound(sound, volume=0.5):
    if sound:
        sound.set_volume(volume)
        sound.play()


# =========================
# Helpers
# =========================
def make_turtle():
    pen = turtle.Turtle()
    pen.speed(0)
    pen.penup()
    pen.hideturtle()
    return pen


def draw_border():
    global border_pen

    border_pen = make_turtle()
    border_pen.color("white")
    border_pen.pensize(3)
    border_pen.goto(BORDER_LEFT, BORDER_BOTTOM)
    border_pen.pendown()

    for _ in range(4):
        border_pen.forward(600)
        border_pen.left(90)

    border_pen.penup()


def update_score():
    score_pen.clear()
    score_pen.goto(-290, 280)
    score_pen.color("white")
    score_pen.write(
        f"Score: {score}",
        align="left",
        font=("Arial", 16, "bold")
    )


def show_message(title, subtitle=""):
    message_pen.clear()
    message_pen.goto(0, 30)
    message_pen.color("red")
    message_pen.write(
        title,
        align="center",
        font=("Comic Sans MS", 42, "bold")
    )

    if subtitle:
        message_pen.goto(0, -25)
        message_pen.color("white")
        message_pen.write(
            subtitle,
            align="center",
            font=("Arial", 16, "bold")
        )


# =========================
# Menu
# =========================
menu_pen = make_turtle()


def draw_button(x, y, width, height, text):
    menu_pen.goto(x, y)
    menu_pen.color("white")
    menu_pen.pensize(4)
    menu_pen.pendown()

    for _ in range(2):
        menu_pen.forward(width)
        menu_pen.left(90)
        menu_pen.forward(height)
        menu_pen.left(90)

    menu_pen.penup()
    menu_pen.goto(x + width / 2, y + 8)
    menu_pen.write(
        text,
        align="center",
        font=("Comic Sans MS", 24, "bold")
    )


def start_menu():
    global game_running

    game_running = False

    wp.clear()
    wp.setup(width=700, height=700)
    wp.title("Space Shooter")
    wp.bgcolor("black")
    wp.bgpic(BG_IMG)
    wp.tracer(0)

    menu_pen.clear()
    menu_pen.penup()

    menu_pen.goto(0, 100)
    menu_pen.color("white")
    menu_pen.write(
        "Space Shooter",
        align="center",
        font=("Comic Sans MS", 40, "bold")
    )

    menu_pen.goto(0, 55)
    menu_pen.write(
        "Arrow Keys to move     Space to shoot",
        align="center",
        font=("Arial", 14, "normal")
    )

    draw_button(-100, 0, 200, 55, "Play")
    draw_button(-100, -90, 200, 55, "Quit")

    wp.onclick(handle_menu_click)
    wp.update()


def handle_menu_click(x, y):
    if -100 <= x <= 100 and 0 <= y <= 55:
        setup_game()
    elif -100 <= x <= 100 and -90 <= y <= -35:
        wp.bye()


# =========================
# Game Setup
# =========================
def setup_game():
    global player, laser, score_pen, message_pen
    global enemies, score, enemy_speed, laser_state, game_running

    wp.clear()
    wp.setup(width=700, height=700)
    wp.title("Space Shooter")
    wp.bgcolor("black")
    wp.bgpic(BG_IMG)
    wp.tracer(0)

    score = 0
    enemy_speed = ENEMY_START_SPEED
    laser_state = "ready"
    game_running = True
    enemies = []

    draw_border()

    score_pen = make_turtle()
    message_pen = make_turtle()
    update_score()

    player = turtle.Turtle()
    player.shape(PLAYER_IMG)
    player.penup()
    player.speed(0)
    player.goto(0, PLAYER_Y)
    player.setheading(90)
    player.dx = 0

    for _ in range(NUMBER_OF_ENEMIES):
        enemy = turtle.Turtle()
        enemy.shape(ENEMY_IMG)
        enemy.penup()
        enemy.speed(0)
        enemy.goto(random.randint(-220, 220), random.randint(100, 250))
        enemies.append(enemy)

    laser = turtle.Turtle()
    laser.shape(LASER_IMG)
    laser.penup()
    laser.speed(0)
    laser.setheading(90)
    laser.goto(0, -400)
    laser.hideturtle()

    bind_keys()

    wp.update()
    game_loop()


# =========================
# Controls
# =========================
def move_left():
    if game_running:
        player.dx = -PLAYER_SPEED


def move_right():
    if game_running:
        player.dx = PLAYER_SPEED


def stop_player():
    if game_running:
        player.dx = 0


def shoot_laser():
    global laser_state

    if not game_running:
        return

    if laser_state == "ready":
        play_sound(laser_sfx, 0.35)
        laser_state = "shoot"
        laser.goto(player.xcor(), player.ycor() + 25)
        laser.showturtle()


def restart_game():
    if game_running:
        return

    setup_game()


def bind_keys():
    wp.listen()

    wp.onkeypress(move_left, "Left")
    wp.onkeypress(move_right, "Right")
    wp.onkeyrelease(stop_player, "Left")
    wp.onkeyrelease(stop_player, "Right")

    wp.onkey(shoot_laser, "space")
    wp.onkey(restart_game, "r")


# =========================
# Game Logic
# =========================
def move_player():
    x = player.xcor() + player.dx

    if x < -280:
        x = -280
    elif x > 280:
        x = 280

    player.setx(x)


def move_laser():
    global laser_state

    if laser_state == "shoot":
        laser.sety(laser.ycor() + LASER_SPEED)

        if laser.ycor() > BORDER_TOP - 20:
            laser.hideturtle()
            laser.goto(0, -400)
            laser_state = "ready"


def move_enemies():
    global enemy_speed

    should_drop = False

    for enemy in enemies:
        enemy.setx(enemy.xcor() + enemy_speed)

        if enemy.xcor() > 270 or enemy.xcor() < -270:
            should_drop = True

    if should_drop:
        enemy_speed *= -1

        for enemy in enemies:
            enemy.sety(enemy.ycor() - ENEMY_DROP)


def is_collision(t1, t2, distance=25):
    return math.sqrt(
        math.pow(t1.xcor() - t2.xcor(), 2) +
        math.pow(t1.ycor() - t2.ycor(), 2)
    ) < distance


def reset_enemy(enemy):
    enemy.goto(random.randint(-220, 220), random.randint(120, 260))


def check_laser_enemy_collision():
    global score, laser_state

    if laser_state != "shoot":
        return

    for enemy in enemies:
        if is_collision(laser, enemy, 30):
            play_sound(zombie_death_sfx, 0.5)

            laser.hideturtle()
            laser.goto(0, -400)
            laser_state = "ready"

            reset_enemy(enemy)

            score += 1
            update_score()
            break


def check_player_enemy_collision():
    for enemy in enemies:
        if is_collision(player, enemy, 35):
            end_game()
            return True

        if enemy.ycor() < PLAYER_Y + 25:
            end_game()
            return True

    return False


def end_game():
    global game_running

    game_running = False

    player.hideturtle()
    laser.hideturtle()

    for enemy in enemies:
        enemy.hideturtle()

    show_message("GAME OVER", "Press R to restart")
    wp.update()


def game_loop():
    if not game_running:
        return

    move_player()
    move_enemies()
    move_laser()

    check_laser_enemy_collision()

    if check_player_enemy_collision():
        return

    wp.update()
    wp.ontimer(game_loop, 20)


# =========================
# Start Game
# =========================
start_menu()
wp.mainloop()