import random
import turtle as t

# =========================
# Game Settings
# =========================
WIDTH = 700
HEIGHT = 600
MOVE_DISTANCE = 20
GAME_SPEED = 100

APPLE_MIN_X = -300
APPLE_MAX_X = 300
APPLE_MIN_Y = -240
APPLE_MAX_Y = 240

# =========================
# Screen Setup
# =========================
screen = t.Screen()
screen.setup(WIDTH, HEIGHT)
screen.bgcolor("yellow")
screen.bgpic("assets/Background3.gif")
screen.title("2-Player Snake Game")
screen.tracer(0)

# =========================
# Game State
# =========================
game_running = False
is_paused = False

score1 = 0
score2 = 0

snake1_body = []
snake2_body = []

# =========================
# Snake Heads
# =========================
snake1 = t.Turtle()
snake1.shape("square")
snake1.color("blue")
snake1.speed(0)
snake1.penup()
snake1.hideturtle()

snake2 = t.Turtle()
snake2.shape("square")
snake2.color("green")
snake2.speed(0)
snake2.penup()
snake2.hideturtle()

# =========================
# Apple
# =========================
apple = t.Turtle()
t.register_shape("assets/Apple.gif")
apple.shape("assets/Apple.gif")
apple.speed(0)
apple.penup()
apple.hideturtle()

# =========================
# Text Turtles
# =========================
text_turtle = t.Turtle()
text_turtle.hideturtle()
text_turtle.penup()

score_turtle = t.Turtle()
score_turtle.hideturtle()
score_turtle.penup()
score_turtle.speed(0)

message_turtle = t.Turtle()
message_turtle.hideturtle()
message_turtle.penup()


# =========================
# UI Functions
# =========================
def draw_start_screen():
    text_turtle.clear()
    text_turtle.color("black")

    text_turtle.goto(0, 70)
    text_turtle.write(
        "2-Player Snake Game",
        align="center",
        font=("Arial", 28, "bold")
    )

    text_turtle.goto(0, 25)
    text_turtle.write(
        "Press SPACE to start",
        align="center",
        font=("Arial", 17, "bold")
    )

    text_turtle.goto(0, -15)
    text_turtle.write(
        "Blue: Arrow Keys     Green: W A S D",
        align="center",
        font=("Arial", 13, "normal")
    )

    text_turtle.goto(0, -45)
    text_turtle.write(
        "P = Pause     R = Restart",
        align="center",
        font=("Arial", 13, "normal")
    )


def display_score():
    score_turtle.clear()

    score_turtle.goto(-WIDTH // 2 + 40, HEIGHT // 2 - 65)
    score_turtle.color("blue")
    score_turtle.write(
        f"Blue: {score1}",
        align="left",
        font=("Arial", 26, "bold")
    )

    score_turtle.goto(WIDTH // 2 - 40, HEIGHT // 2 - 65)
    score_turtle.color("green")
    score_turtle.write(
        f"Green: {score2}",
        align="right",
        font=("Arial", 26, "bold")
    )


def show_center_message(title, subtitle=""):
    message_turtle.clear()
    message_turtle.color("black")

    message_turtle.goto(0, 25)
    message_turtle.write(
        title,
        align="center",
        font=("Arial", 30, "bold")
    )

    if subtitle:
        message_turtle.goto(0, -20)
        message_turtle.write(
            subtitle,
            align="center",
            font=("Arial", 16, "normal")
        )


# =========================
# Snake Helpers
# =========================
def create_segment(color):
    segment = t.Turtle()
    segment.shape("square")
    segment.color(color)
    segment.speed(0)
    segment.penup()
    segment.hideturtle()
    return segment


def add_segment(body_list, color):
    segment = create_segment(color)
    body_list.append(segment)
    return segment


def hide_body(body_list):
    for segment in body_list:
        segment.hideturtle()


def setup_snake(head, body_list, color, start_x, start_y, heading):
    head.goto(start_x, start_y)
    head.setheading(heading)
    head.showturtle()

    body_list.clear()

    for i in range(3):
        segment = add_segment(body_list, color)

        if heading == 0:
            segment.goto(start_x - MOVE_DISTANCE * (i + 1), start_y)
        elif heading == 180:
            segment.goto(start_x + MOVE_DISTANCE * (i + 1), start_y)
        elif heading == 90:
            segment.goto(start_x, start_y - MOVE_DISTANCE * (i + 1))
        elif heading == 270:
            segment.goto(start_x, start_y + MOVE_DISTANCE * (i + 1))

        segment.showturtle()


def move_body(head, body_list):
    for i in range(len(body_list) - 1, 0, -1):
        body_list[i].goto(body_list[i - 1].pos())

    if body_list:
        body_list[0].goto(head.pos())


def grow_snake(body_list, color):
    segment = add_segment(body_list, color)

    if len(body_list) > 1:
        segment.goto(body_list[-2].pos())
    else:
        segment.goto(0, 0)

    segment.showturtle()


def wrap_around(head):
    half_w = WIDTH // 2
    half_h = HEIGHT // 2

    x = head.xcor()
    y = head.ycor()

    if x > half_w:
        head.setx(-half_w + MOVE_DISTANCE)
    elif x < -half_w:
        head.setx(half_w - MOVE_DISTANCE)

    if y > half_h:
        head.sety(-half_h + MOVE_DISTANCE)
    elif y < -half_h:
        head.sety(half_h - MOVE_DISTANCE)


# =========================
# Apple Helpers
# =========================
def is_position_on_snake(x, y):
    if snake1.isvisible() and snake1.distance(x, y) < 35:
        return True

    if snake2.isvisible() and snake2.distance(x, y) < 35:
        return True

    for segment in snake1_body + snake2_body:
        if segment.isvisible() and segment.distance(x, y) < 35:
            return True

    return False


def place_apple():
    while True:
        x = random.randrange(APPLE_MIN_X, APPLE_MAX_X, MOVE_DISTANCE)
        y = random.randrange(APPLE_MIN_Y, APPLE_MAX_Y, MOVE_DISTANCE)

        if not is_position_on_snake(x, y):
            apple.goto(x, y)
            apple.showturtle()
            break


# =========================
# Collision Helpers
# =========================
def hits_body(head, body_list):
    for segment in body_list:
        if segment.isvisible() and head.distance(segment) < 12:
            return True
    return False


def calculate_winner():
    if score1 > score2:
        return "BLUE WINS!"
    elif score2 > score1:
        return "GREEN WINS!"
    else:
        return "DRAW!"


def game_over():
    global game_running

    game_running = False
    show_center_message(calculate_winner(), "Press R to restart")
    screen.update()


def check_collisions():
    blue_crashed = False
    green_crashed = False

    # Head-to-head collision
    if snake1.distance(snake2) < 15:
        blue_crashed = True
        green_crashed = True

    # Blue crashes
    if hits_body(snake1, snake1_body[1:]):
        blue_crashed = True

    if hits_body(snake1, snake2_body):
        blue_crashed = True

    # Green crashes
    if hits_body(snake2, snake2_body[1:]):
        green_crashed = True

    if hits_body(snake2, snake1_body):
        green_crashed = True

    if blue_crashed or green_crashed:
        game_over()
        return True

    return False


# =========================
# Main Game Loop
# =========================
def move_snakes():
    global score1, score2

    if not game_running:
        return

    if is_paused:
        screen.ontimer(move_snakes, GAME_SPEED)
        return

    move_body(snake1, snake1_body)
    move_body(snake2, snake2_body)

    snake1.forward(MOVE_DISTANCE)
    snake2.forward(MOVE_DISTANCE)

    wrap_around(snake1)
    wrap_around(snake2)

    if snake1.distance(apple) < 20:
        score1 += 1
        grow_snake(snake1_body, "blue")
        display_score()
        place_apple()

    elif snake2.distance(apple) < 20:
        score2 += 1
        grow_snake(snake2_body, "green")
        display_score()
        place_apple()

    if check_collisions():
        return

    screen.update()
    screen.ontimer(move_snakes, GAME_SPEED)


# =========================
# Game Controls
# =========================
def start_game():
    global game_running, is_paused, score1, score2

    if game_running:
        return

    game_running = True
    is_paused = False

    score1 = 0
    score2 = 0

    text_turtle.clear()
    message_turtle.clear()
    score_turtle.clear()

    snake1.hideturtle()
    snake2.hideturtle()
    apple.hideturtle()

    hide_body(snake1_body)
    hide_body(snake2_body)

    snake1_body.clear()
    snake2_body.clear()

    setup_snake(snake1, snake1_body, "blue", -220, -80, 0)
    setup_snake(snake2, snake2_body, "green", 220, 80, 180)

    display_score()
    place_apple()

    screen.update()
    move_snakes()


def restart_game():
    global game_running, is_paused

    game_running = False
    is_paused = False

    snake1.hideturtle()
    snake2.hideturtle()
    apple.hideturtle()

    hide_body(snake1_body)
    hide_body(snake2_body)

    snake1_body.clear()
    snake2_body.clear()

    message_turtle.clear()
    score_turtle.clear()

    draw_start_screen()
    screen.update()


def toggle_pause():
    global is_paused

    if not game_running:
        return

    is_paused = not is_paused
    message_turtle.clear()

    if is_paused:
        show_center_message("PAUSED", "Press P to continue")

    screen.update()


# =========================
# Player 1 Controls
# =========================
def snake1_up():
    if snake1.heading() != 270:
        snake1.setheading(90)


def snake1_down():
    if snake1.heading() != 90:
        snake1.setheading(270)


def snake1_left():
    if snake1.heading() != 0:
        snake1.setheading(180)


def snake1_right():
    if snake1.heading() != 180:
        snake1.setheading(0)


# =========================
# Player 2 Controls
# =========================
def snake2_up():
    if snake2.heading() != 270:
        snake2.setheading(90)


def snake2_down():
    if snake2.heading() != 90:
        snake2.setheading(270)


def snake2_left():
    if snake2.heading() != 0:
        snake2.setheading(180)


def snake2_right():
    if snake2.heading() != 180:
        snake2.setheading(0)


# =========================
# Key Bindings
# =========================
screen.onkey(start_game, "space")
screen.onkey(restart_game, "r")
screen.onkey(toggle_pause, "p")

screen.onkey(snake1_up, "Up")
screen.onkey(snake1_right, "Right")
screen.onkey(snake1_down, "Down")
screen.onkey(snake1_left, "Left")

screen.onkey(snake2_up, "w")
screen.onkey(snake2_right, "d")
screen.onkey(snake2_down, "s")
screen.onkey(snake2_left, "a")

screen.listen()

draw_start_screen()
screen.update()
screen.mainloop()