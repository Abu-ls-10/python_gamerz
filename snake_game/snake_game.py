import random
import turtle as t

# Background
t.bgcolor('limegreen')
t.bgpic('assets/Background.gif')
t.title('Snake Game')
t.tracer(0)

# Snake Properties
snake = t.Turtle()
snake.shape('square')
snake.color('blue')
snake.speed(0)
snake.penup()
snake.hideturtle()

snake_body = []

# Apple Properties
apple = t.Turtle()
t.register_shape('assets/Apple.gif')
apple.shape('assets/Apple.gif')
apple.color('green')
apple.penup()
apple.hideturtle()
apple.speed(0)

# Initialization
game_started = False
game_running = False
score = 0
snake_speed = 120

text_turtle = t.Turtle()
text_turtle.write('Press SPACE to start', align='center', font=('Arial', 16, 'bold'))
text_turtle.ht()

# Score
score_turtle = t.Turtle()
score_turtle.ht()
score_turtle.speed(0)

# Game Over Turtle
game_over_turtle = t.Turtle()
game_over_turtle.ht()
game_over_turtle.penup()


def outside_window():
    left_wall = -t.window_width() / 2
    right_wall = t.window_width() / 2
    top_wall = t.window_height() / 2
    bottom_wall = -t.window_height() / 2

    x, y = snake.pos()

    return x < left_wall or x > right_wall or y < bottom_wall or y > top_wall


def game_over():
    global game_running
    game_running = False

    game_over_turtle.goto(0, 0)
    game_over_turtle.write('GAME OVER', align='center', font=('Arial', 25, 'normal'))


def display_score(current_score):
    score_turtle.clear()
    score_turtle.penup()

    x = (t.window_width() / 2) - 60
    y = (t.window_height() / 2) - 60

    score_turtle.setpos(x, y)
    score_turtle.write(str(current_score), align='right', font=('Arial', 40, 'bold'))


def place_apple():
    apple.ht()
    apple.setx(random.randint(-220, 220))
    apple.sety(random.randint(-220, 220))
    apple.st()


def create_body_segment():
    segment = t.Turtle()
    segment.shape('square')
    segment.color('blue')
    segment.speed(0)
    segment.penup()
    segment.hideturtle()
    snake_body.append(segment)


def move_snake():
    global score

    if not game_running:
        return

    # Move body segments from tail to front
    for i in range(len(snake_body) - 1, 0, -1):
        x = snake_body[i - 1].xcor()
        y = snake_body[i - 1].ycor()
        snake_body[i].goto(x, y)

    # First body segment follows the head
    if len(snake_body) > 0:
        snake_body[0].goto(snake.xcor(), snake.ycor())

    # Move head
    snake.forward(20)

    # Apple collision
    if snake.distance(apple) < 20:
        place_apple()
        create_body_segment()
        snake_body[-1].showturtle()

        score += 1
        display_score(score)

    # Wall collision
    if outside_window():
        game_over()
        return

    # Body collision
    for segment in snake_body:
        if snake.distance(segment) < 10:
            game_over()
            return

    t.update()
    t.ontimer(move_snake, snake_speed)


def start_game():
    global game_started, game_running, score

    if game_started:
        return

    game_started = True
    game_running = True
    score = 0

    text_turtle.clear()

    snake.goto(0, 0)
    snake.setheading(0)
    snake.showturtle()

    # Starting body length
    for _ in range(3):
        create_body_segment()

    for i, segment in enumerate(snake_body):
        segment.goto(-20 * (i + 1), 0)
        segment.showturtle()

    display_score(score)
    place_apple()

    t.update()
    move_snake()


# Controls
def move_up():
    if snake.heading() != 270:
        snake.setheading(90)


def move_down():
    if snake.heading() != 90:
        snake.setheading(270)


def move_left():
    if snake.heading() != 0:
        snake.setheading(180)


def move_right():
    if snake.heading() != 180:
        snake.setheading(0)


# Listening to User Input
t.onkey(start_game, 'space')
t.onkey(move_up, 'Up')
t.onkey(move_right, 'Right')
t.onkey(move_down, 'Down')
t.onkey(move_left, 'Left')

t.listen()
t.mainloop()