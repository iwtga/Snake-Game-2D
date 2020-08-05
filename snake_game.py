import turtle
import time
import random

# Delay Time on each Screen Refresh
delay = 0.1

# Score Variables
score = 0
high_score = 0

# Setting Up The Window
wn = turtle.Screen()                        # Creating the Window
wn.title("SnakeGame by @Error509")      # Text visible on Title Bar
wn.setup(width=800, height=800)             # Dimensions of the Window
wn.tracer(0)

# Snake Head
head = turtle.Turtle()     # Creating an Instance of Turtle
head.speed(0)
head.shape("square")       # Snake Head Shape
head.color("black")        # Snake Head Colour
head.penup()
head.goto(0, 0)            # Initializes Snake Head At the Center Of the Screen
head.direction = 'stop'    # Head Doesn't point anywhere initially
head.hideturtle()          # Hiding Head Initially on Main Menu

# Snake Food
food = turtle.Turtle()     # Creating Instance of Turtle
food.speed(0)
food.shape("circle")       # Shape of Food Pallet
food.color("red")          # Colour of Food Pallet
food.penup()
food.goto(0, 100)          # First Food Pallet Position on the Positive Y-axis
food.hideturtle()          # Hides The Food Pallet on the Main Menu

# Score Board
pen = turtle.Turtle()      # Turtle Instance used to Write the Scoreboard
pen.speed(0)
pen.hideturtle()           # The Turtle shouldn't be visible
pen.penup()
pen.shape('square')        # Anything Shape is fine as the turtle wont be visible
pen.color('black')         # Colour of the Text Displaying the Score
pen.goto(0, 360)           # Position Of the Score Board
pen.write("Score: 0 Highscore: 0", align='center', font=('Arial', 24, 'normal'))    # Initial Score Board

# Snake Body
segments = []       # List to hold all the body segments

# Game State (intro, ingame)
game_state = 'intro'        # 'intro' indicates user is on Main Menu


# Function to Change Game State from Main Menu To Ingame
def start_game():
    global game_state       # global used as 'game_state' is outside function scope
    game_state = 'ingame'


# Functions to Change Direction of the Heads
def go_up():
    if head.direction != 'down':
        head.direction = 'up'


def go_down():
    if head.direction != 'up':
        head.direction = 'down'


def go_right():
    if head.direction != 'left':
        head.direction = 'right'


def go_left():
    if head.direction != 'right':
        head.direction = 'left'


# Function To Move Head according to its direction attribute. Distance covered per refresh is 20 pixels.
def move():
    if head.direction == 'up':
        head.sety(head.ycor() + 20)
    if head.direction == 'down':
        head.sety(head.ycor() - 20)
    if head.direction == 'right':
        head.setx(head.xcor() + 20)
    if head.direction == 'left':
        head.setx(head.xcor() - 20)


# Game Over Function is called when the snake touches the window boundary or collides with itself
def game_over():
    global delay, score, segment
    head.direction = 'stop'     # Make the Head direct to nothing
    time.sleep(1)               # Freezes Screen for 1 second
    for segment in segments:    # Loops through each segment of the snake
        segment.goto(2000, 2000)        # Moves each segment to outside the window as segments cant be cleared
    segments.clear()        # clears the segments list
    head.goto(0, 0)         # Makes the Turtle head go to the middle of the field
    score = 0               # Resets score to zero
    score_write()           # Calls The Write Score Function
    delay = 0.1             # Sets Refresh Delay Back to 0.1 seconds


# Function Called When Food Pallet is eaten. It Updates the 'score' and 'high_score' variables.
def score_inc():
    global score, high_score
    score += 1
    if score > high_score:
        high_score += 1


# Writes The Score On the Screen
def score_write():
    pen.clear()     # Clears The Previous Displayed Score
    # Displays the updated Score
    pen.write(f'Score: {score} Highscore: {high_score}', align='center', font=('Arial', 24, 'normal'))


# Key Bindings
wn.listen()             # Makes the window Listen to the keys pressed by the user

# Following Instructions Calls the functions depending on the key pressed by the user
wn.onkeypress(start_game, 'p')
wn.onkeypress(go_up, 'w')
wn.onkeypress(go_down, 's')
wn.onkeypress(go_left, 'a')
wn.onkeypress(go_right, 'd')

# Main Game Loop
while True:
    wn.update()                             # Refreshes the Window

    if game_state == 'intro':               # Checks if The Game State is on the Main Menu
        wn.bgpic('MainMenu.gif')            # If So displays the main menu image
        pen.clear()                         # The Score Board text if present
    elif game_state == 'ingame':            # Checks if the game state is in-game
        wn.bgpic('GrassBackground.gif')     # If so changes the background image
        head.showturtle()                   # Shows Turtle head that was hidden
        food.showturtle()                   # Shows Food Pallet That was hidden
        score_write()                       # calls the 'score_write' function

    # Checks for Collision with FOOD
    if head.distance(food) < 20:

        score_inc()         # Calls score_inc Function
        score_write()       # Calls score_write Function

        # Spawns The New Food Pallet at a random position making sure it doesnt overlap with snake body
        flag = 0    # initializing flag for the while loop
        # Initializing x and y co-ordinates of new food pallet
        x = 0
        y = 0
        while flag == 0:
            flag = 1
            # Creates Random x and y Co-ordinates
            x = random.randint(-380, 380)
            y = random.randint(-380, 350)   # Positive y co-ordinate bound is 350 so as to not spawn food on Score Board
            for segment in segments:        # Loops through each segment of the snake
                if segment.distance(x, y) < 20:     # Checks if the position of random food pallet overlaps with segment
                    flag = 0                # Set flag to 0 so that the while loops runs again
                    break                   # Break the for loop as no more looping is required
        food.goto(x, y)                     # Moves the food pallet to a new random position

        # Creates Segments of Snake on Collision With FOOD
        new_segment = turtle.Turtle()       # Creates a segment instance
        new_segment.speed(0)
        new_segment.shape('square')         # Shape of snake segment
        new_segment.color('grey')           # Color of Snake segment
        new_segment.penup()
        segments.append(new_segment)        # Append the new Snake Segment to the segments list

        delay -= 0.001      # Increases Speed Of Snake with each food pallet eaten

    # Makes The Segments Follow the Head
    for i in range(len(segments)-1, 0, -1):
        segments[i].goto(segments[i-1].xcor(), segments[i-1].ycor())

    # Base Case of Segment Following(The First Segment)
    if len(segments) > 0:
        segments[0].goto(head.xcor(), head.ycor())

    move()      # Calls the move Function

    # Checks if Head Hits Body
    for segment in segments:    # Loops through each segment
        if head.distance(segment) < 20:     # Checks if the segment hits the head
            game_over()                     # Calls the game over function
            break

    # Checks if Head Hits Boundary
    if head.xcor() < -380 or head.xcor() > 380 or head.ycor() < -380 or head.ycor() > 380:
        game_over()             # Calls the Game over Function

    time.sleep(delay)           # Waits for delay amount of time before looping again


wn.mainloop()  # Keeps the Game Window Open
