import time
import turtle


def little_heart():
    for i in range(200):
        turtle.right(1)
        turtle.forward(2)


love = input('Please enter a sentence of love,otherwise the default is "I Love You":\n')
me = input("Please enter pen name, otherwise the default do not execute:\n")
if love == "":
    love = "I Love you"
turtle.setup(width=900, height=500)
turtle.color("red", "pink")
turtle.pensize(3)
turtle.speed(5)
turtle.up()
turtle.hideturtle()
turtle.goto(0, -180)
turtle.showturtle()
turtle.down()
turtle.speed(5)
turtle.begin_fill()
turtle.left(140)
turtle.forward(224)
little_heart()
turtle.left(120)
little_heart()
turtle.forward(224)
turtle.end_fill()
turtle.pensize(5)
turtle.up()
turtle.hideturtle()
turtle.goto(0, 0)
turtle.showturtle()
turtle.color("#CD5C5C", "pink")
turtle.write(love, font=("gungsuh", 30), align="center")
turtle.up()
turtle.hideturtle()
if me != "":
    turtle.color("black", "pink")
    time.sleep(2)
turtle.goto(180, -180)
turtle.showturtle()
turtle.write(me, font=(20,), align="center", move=True)
window = turtle.Screen()
window.exitonclick()
