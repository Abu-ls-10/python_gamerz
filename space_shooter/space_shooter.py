import turtle
import os
import math
import random
import winsound
from turtle import*
import functools





   
wp = turtle.Screen()


#Register Shapes
turtle.register_shape("invaders.gif")
turtle.register_shape("pass.gif")
turtle.register_shape("brrs.gif")
turtle.register_shape("prp.gif")


# Constants
enemyspeed = 3
laserspeed = 20
laserstate = "ready"




def setup_game():
    global laserstate
    #Make Background
    wp.bgcolor("black")
    wp.title("Space Shooter")
    wp.bgpic("golden.gif")


    #Outline
    #Make outline
    border_pen = turtle.Turtle()
    border_pen.speed(0)
    border_pen.color("white")
    border_pen.penup()
    border_pen.setposition(-300,-300)
    border_pen.pendown()
    border_pen.pensize(3)
    for side in range(4):
        border_pen.fd(600)
        border_pen.lt(90)
    border_pen.hideturtle()
    #Scoreboard
    #Make scoreboard
    score_pen = turtle.Turtle()
    score = 0
    score_pen.speed(0)
    score_pen.color("White")
    score_pen.penup()
    score_pen.setposition(-290,280)
    scorestring = "Score: %s" %score
    score_pen.write(scorestring, False, align="left", font= ("Arial", 14, "normal"))
    score_pen.hideturtle()
    
    #SpaceShip
    #Make SpaceShip
    player = turtle.Turtle()
    player.color("red")
    player.shape("pass.gif")
    player.penup()
    player.speed(0)
    player.setposition(0,-250)
    player.setheading(90)
    player.speed = 0
    #Make enemy
    #Number of Enemies
    number_of_enemies = 5

    enemies = []

    for i in range(number_of_enemies):
        enemies.append(turtle.Turtle())
    for enemy in enemies:
        enemy.color("yellow")
        enemy.shape("invaders.gif")
        enemy.penup()
        enemy.speed(0)
        x = random.randint(-200,200)
        y = random.randint(100,250)
        enemy.setposition(x,y)
        
    #Laser
    #Make Laser
    laser = turtle.Turtle()
    laser.color("white")
    laser.shape("prp.gif")
    laser.penup()
    laser.speed()
    #laser.shapesize(0.5,0.5)
    laser.setheading(90)
    laser.hideturtle()
    #Configure Laser State
    laserstate = "ready"
    

    move_left_bound = functools.partial(move_left, player)
    move_right_bound = functools.partial(move_right, player)
    shoot_laser_bound = functools.partial(shoot_laser, player, laser)
    
    #Make arrow keys work

    wp.listen()
    wp.onkey(move_left_bound, "Left")
    wp.onkey(move_right_bound, "Right")
    wp.onkey(shoot_laser_bound, "space")
    
    
    return (player, enemies, laser, score, score_pen)

#Making Movement

def move_left(player):
        player.speed = -15
      

def move_right(player):
        player.speed = 15
        x = player.xcor()
        x +=player.speed
        player.setx(x)

def move_player(player):
        x = player.xcor()
        x +=player.speed
        if x < -280:
                x=-280
        if x > 280:
                x=280
        player.setx(x)


        

def shoot_laser(player, laser):
    global laserstate
    if laserstate == "ready":
        winsound.PlaySound("ls.wav", winsound.SND_ASYNC)
        laserstate = "shoot"
        #Move laser above player
        x = player.xcor()
        y = player.ycor() +10
        laser.setposition(x,y)
        laser.showturtle()

def isCollision(t1, t2):
        distance = math.sqrt(math.pow(t1.xcor()- t2.xcor(),2)+math.pow(t1.ycor()-t2.ycor(),2))

        if distance < 15:
                return True
        else:
                return False








#Make Game Loop
def start_game(player, enemies, laser, score, score_pen):
    print ("Game Started")
    global enemyspeed, laserstate
    Game_ended = False
    while True:
        if Game_ended == True:
            break
        #print (laser.xcor(),laser.ycor())
                
            
        move_player(player)
            
        for enemy in enemies:


            #Move Enemy
            x = enemy.xcor()
            x += enemyspeed
            enemy.setx(x)

            #Move the enemy back
            if enemy.xcor() >280:
               for e in enemies:
                   y = e.ycor()
                   y -= 40
                   e.sety(y)
                   enemyspeed *= -1
                            
            if enemy.xcor() <-280:
                for e in enemies:
                      y = e.ycor()
                      y -= 40
                      e.sety(y)
                      enemyspeed *= -1

             #Check for collision
            if isCollision(laser,enemy):
               winsound.PlaySound("EXP.wav", winsound.SND_ASYNC)
               #Reset Laser
               laser.hideturtle()
               laserstate = "ready"
               laser.setposition(0,-400)
               #Reset Enemy
               x = random.randint(-200,200)
               y = random.randint(100,250)
               enemy.setposition(x,y)
               #Add points
               score += 1
               scorestring = "Score: %s" %score
               score_pen.clear()
               score_pen.write(scorestring, False, align="left", font= ("Arial", 14, "normal"))

                            
            if isCollision(player,enemy):
               player.hideturtle()
               enemy.hideturtle()
               print ("GAME OVER")
               Game_ended = True
               break 

        #Make Laser Move
        if laserstate == "shoot":
           y = laser.ycor()
           y += laserspeed
           laser.sety(y)

        #Identifying if the laser is at the top
        if laser.ycor() > 275:
            laser.hideturtle()
            laserstate = "ready"

    line_pen = turtle.Turtle()
    line_pen.penup()
    line_pen.setposition(0,0)
    line_pen.color("red")
    line_pen.pendown()
    line_pen.write("GAME OVER", align = "center", font = ("Comic Sans MS", 50, "bold"))
    line_pen.ht()
    
        
   
    #wp.clear()
    #start_menu2()




text = turtle.Turtle()



close = turtle.Turtle()

close.ht()



    

    





def onTextClick(x,y):
    print("x={}, y={}".format(x,y))
    if (x >=-100 and x<=100) and (y >=0 and y <=50):
        wp.clear()
        (player, enemies, laser, score, score_pen) = setup_game()
        start_game(player, enemies, laser, score, score_pen)
    elif x > -104 and x < 104 and y> -83 and y <-26:
        turtle.Screen().exitonclick()




def start_menu2():
    line = turtle.Turtle()

    wp.bgpic("brrss.gif")
    #Make Play Button
    line.penup()
    line.speed(0)
    line.setposition(-100,0)
    line.pendown()
    line.pensize(8)
    line.color("black")
    for i in range(2):
        line.forward(200)
        line.left(90)
        line.forward(50)
        line.left(90)
        line.hideturtle()
    line.penup()

    line.setposition(-100,-30)
    line.speed(0)
    line.pendown()
    for i in range(2):
        line.forward(200)
        line.right(90)
        line.forward(50)
        line.right(90)
        
    text.penup()
    text.speed(0)
    text.setposition(14,75)
    text.color("black")
    text.pendown()
    text.write("Space Shooters", align = "center", font = ("Comic Sans MS", 40, "bold", "italic"))
    text.penup()
    text.setposition(0,2)
    text.pensize(5)
    text.pendown()
    text.write("Play", align = "center", font=("Comic Sans MS", 30, "bold", "italic"))
    text.ht()
    #Making Quit Button
    line.penup()
    line.goto(-10,-78)
    line.pendown()
    line.write("Quit", align = "center", font = ("Comic Sans MS", 30,"bold", "italic"))
      
  

    wp.onclick(onTextClick)
        

  
    




start_menu2()


#Make Quit Button





    



#(-290,280)

