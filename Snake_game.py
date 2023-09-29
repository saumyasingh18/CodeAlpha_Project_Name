#Task 3 - Snake Game
#Date- 25/09/2023
#Programmer- Saumya singh (saumyasingh635@gmail.com)

from turtle import Turtle, Screen
import time
import random
score=0
high_score=0
delay=0.1
#setting up the screen 
screen=Screen()
screen.title("Snake Game")
screen.setup(width=600,height=600)
screen.bgcolor("DarkGreen")
screen.tracer(0)
time.sleep(10)

#snake body
snake=Turtle()
snake.speed(0)
snake.shape("circle")
snake.color("CadetBlue2")
snake.penup()
snake.goto(0,0)
snake.direction ="Stop"

#food
food=Turtle()
food.speed(0)
food.shape("circle")
food.color("red")
food.penup()
food.goto(0,100)

#score board
scoreboard=Turtle()
scoreboard.speed(0)
scoreboard.color("yellow")
scoreboard.penup()
scoreboard.goto(0,260)
scoreboard.write("Score:0 High Score:0",align="center",font="Arial")

def goup():
    if snake.direction!="down":
         snake.direction = "up"
 
 
def godown():
    if snake.direction != "up":
        snake.direction = "down"
 
 
def goleft():
    if snake.direction != "right":
        snake.direction = "left"

def goright():
    if snake.direction != "left":
        snake.direction = "right"
def move():
    if snake.direction == "up":
        y = snake.ycor()
        snake.sety(y+20)
    if snake.direction == "down":
        y = snake.ycor()
        snake.sety(y-20)
    if snake.direction == "left":
        x = snake.xcor()
        snake.setx(x-20)
    if snake.direction == "right":
        x = snake.xcor()
        snake.setx(x+20)
 
screen.listen()
screen.onkeypress(goup, "Up")
screen.onkeypress(godown, "Down")
screen.onkeypress(goleft, "Left")
screen.onkeypress(goright, "Right")

segments=[]
while True:
    screen.update()
    if snake.xcor()>290 or snake.xcor()< -290 or snake.ycor()>290 or snake.ycor()< -290 :
        time.sleep(1)
        snake.goto(0, 0)
        snake.direction = "Stop"
        for segment in segments:
            segment.goto(1000, 1000)
        segments.clear()
        score = 0
        delay = 0.1
        scoreboard.clear()
        scoreboard.write("Score : {} High Score : {} ".format(
            score, high_score), align="center", font=("candara", 24, "bold"))
    if snake.distance(food) < 20:
        x = random.randint(-270, 270)
        y = random.randint(-270, 270)
        food.goto(x, y)
         # Adding segment
        new_segment = Turtle()
        new_segment.speed(0)
        new_segment.shape("square")
        new_segment.color("CadetBlue4") 
        new_segment.penup()
        segments.append(new_segment)
        delay -= 0.001
        score += 10
        if score > high_score:
            high_score = score
        scoreboard.clear()
        scoreboard.write("Score : {} High Score : {} ".format(
            score, high_score), align="center", font=("candara", 24, "bold"))
     # Checking for head collisions with body segments
    for index in range(len(segments)-1, 0, -1):
        x = segments[index-1].xcor()
        y = segments[index-1].ycor()
        segments[index].goto(x, y)
    if len(segments) > 0:
        x = snake.xcor()
        y = snake.ycor()
        segments[0].goto(x, y)
    move()  
    for segment in segments:
        if segment.distance(snake) < 20:
            time.sleep(1)
            snake.goto(0, 0)
            snake.direction = "stop"
            colors = random.choice(['red', 'blue', 'green'])
            shapes = random.choice(['square', 'circle'])
            for segment in segments:
                segment.goto(1000, 1000)
            segments.clear()
 
            score = 0
            delay = 0.1
            screen.clear()
            screen.write("Score : {} High Score : {} ".format(
                score, high_score), align="center", font=("candara", 24, "bold"))
    time.sleep(delay)

screen.mainloop()