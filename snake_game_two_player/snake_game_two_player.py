import random
import turtle as t

#Background
t.bgcolor('yellow')
t.bgpic('Background3.gif')
t.title('2-Player Snake Game')

#Snake 1 Properties
snake1 = t.Turtle()
snake1.shape('square')
snake1.color('blue')
snake1.speed(0)
snake1.penup()
snake1.hideturtle()

#Snake 2 Properties
snake2 = t.Turtle()
snake2.color('green')
snake2.shape('square')
snake2.penup()
snake2.speed(0)
snake2.hideturtle()


#Apple Properties
apple = t.Turtle()
t.register_shape('Apple.gif')
apple.shape('Apple.gif')
apple.color('green')
apple.penup()
apple.hideturtle()
apple.speed(0)

#Initialization
game_started = False
text_turtle = t.Turtle()
text_turtle.write('Press SPACE to start', align='center',font=('Arial', 16, 'bold'))
text_turtle.ht()

#Score
score_1 = t.Turtle()
score_1.ht()
score_1.speed(0)

score_2 = t.Turtle()
score_2.ht()
score_2.speed(0)

#Setting Borders
def outside_window(snake):
  left_wall = -t.window_width() / 2
  right_wall = t.window_width() / 2
  top_wall = t.window_height() / 2
  bottom_wall = -t.window_height() / 2
  (x, y) = snake.pos()
  outside = \
    x< left_wall or \
    x> right_wall or \
    y< bottom_wall or \
    y> top_wall
  return outside

#Game Over Screen
def game_over():
  t.penup()
  t.hideturtle()
  t.write('GAME OVER', align='center', font=('Arial', 25, 'normal'))
    
#Display Score
def display_score(current_score1, current_score2):
  score_1.clear()
  score_1.penup()
  x = (t.window_width() / 2) - 60
  y = (t.window_height() / 2) - 60
  score_1.setpos(x, y)
  score_1.write (str(current_score1), align='right', font=('Arial', 40, 'bold'))

  score_2.clear()
  score_2.penup()
  a = (t.window_width() / 2) - 240
  b = (t.window_height() / 2) - 60
  score_2.setpos(a, b)
  score_2.write (str(current_score2), align='left', font=('Arial', 40, 'bold'))
    
#Placing Apple
def place_apple():
  apple.ht()
  apple.setx(random.randint(-200, 200))
  apple.sety(random.randint(-200, 200))
  apple.st()

#Game Start
def start_game():
  global game_started
  if game_started:
    return
  game_started = True

  score1 = 0
  score2=0
  text_turtle.clear()

  snake1_speed = 2
  snake1_length = 3
  snake1.shapesize(1, snake1_length, 1)
  snake1.showturtle()

  snake2_speed = 2
  snake2_length = 3
  snake2.shapesize(1, snake2_length, 1)
  snake2.setheading(180)
  snake2.showturtle()

  display_score(score1, score2)
  place_apple()
  

  while True:
    snake1.forward(snake1_speed)
    snake2.forward(snake2_speed)
    
    if snake1.distance(apple) < 20:
      place_apple()
      snake1_length+=1
      snake1.shapesize(1, snake1_length, 1)

      score1+=1
      display_score(score1, score2)

    elif snake2.distance(apple) < 20:
      place_apple()
      snake2_length+=1
      snake2.shapesize(1, snake2_length, 1)

      score2+=1
      display_score(score1, score2)

    if outside_window(snake1) or outside_window(snake2):
      game_over()
      break

#Caterpillar 1 Controls
def move_up():
  if snake1.heading() == 0 or snake1.heading() == 180:
    snake1.setheading(90)

def move_down():
  if snake1.heading() == 0 or snake1.heading() == 180:
    snake1.setheading(270)

def move_left():
  if snake1.heading() == 90 or snake1.heading() == 270:
    snake1.setheading(180)

def move_right():
  if snake1.heading() == 90 or snake1.heading() == 270:
    snake1.setheading(0)


#Caterpillar 2 Controls 
def snake2_move_up():
  if snake2.heading() == 0 or snake2.heading() == 180:
    snake2.setheading(90)

def snake2_move_down():
  if snake2.heading() == 0 or snake2.heading() == 180:
    snake2.setheading(270)

def snake2_move_left():
  if snake2.heading() == 90 or snake2.heading() == 270:
    snake2.setheading(180)

def snake2_move_right():
  if snake2.heading() == 90 or snake2.heading() == 270:
    snake2.setheading(0)


#Listening to Player 1 Input
t.onkey(start_game, 'space')
t.onkey(move_up, 'Up')
t.onkey(move_right, 'Right')
t.onkey(move_down, 'Down')
t.onkey(move_left, 'Left')

#Listening to Player 2 Input
t.onkey(snake2_move_up, 'w')
t.onkey(snake2_move_right, 'd')
t.onkey(snake2_move_down, 's')
t.onkey(snake2_move_left, 'a')

t.listen()

t.mainloop



    
