"""
Week 4: Pong
Author: Vu Tran
Website: http://vu-tran.com/

A simple Pong game made in Python.

BONUS: I've added a simple mode to play against an AI. Hope you enjoy it!

"""

import simplegui, random

# Configurations
FRAME_WIDTH = 600
FRAME_HEIGHT = 400
PAD_WIDTH = 8
PAD_HEIGHT = 80
BALL_RADIUS = 20

class PongGame:
    def __init__(self, width, height, pad_width, pad_height, ball_radius):
        """Initializes the class

        <Pong> self
        <int> width             The width of the board
        <int> height            The height of the board
        <int> pad_width         The pad width
        <int> pad_height        The pad height
        <int> ball_radius       The ball radius
        """
        # Set board/pad sizes, ball radius
        self.width = width
        self.height = height
        self.pad_width = pad_width
        self.pad_height = pad_height
        self.ball_radius = ball_radius
        # Create the frame
        self.frame = simplegui.create_frame("Pong", self.width, self.height)
        self.frame.set_canvas_background("black")
        self.frame.set_draw_handler(self.draw)
        self.frame.set_keydown_handler(self.on_keydown)
        self.frame.set_keyup_handler(self.on_keyup)
        self.restart_button = self.frame.add_button('Restart', self.on_restart)
        self.with_ai_button = self.frame.add_button('Play with AI', self.on_with_ai)
        # Create the lines
        self.lines = Lines(width, height, pad_width, pad_height)
        # Create the ball
        self.ball = Ball(ball_radius, self.get_center())
        # Create the paddles
        self.pad_left = Paddle(self.pad_width, self.pad_height, 0, ((self.height - self.pad_height) / 2), "blue")
        self.pad_left.set_constraints(0, self.height)
        self.pad_left.bind_keys(("w", "s"))
        self.pad_right = self.create_secondary_paddle()
        # Create the score board
        self.scoreboard = Scoreboard(self.get_center())
        # Starts the frame
        self.start()
    def start(self):
        """Starts the game

        <Pong> self
        """
        self.frame.start()
    def create_secondary_paddle(self):
        """Creates a normal secondary paddle and returns it

        <PongGame> self
        """
        paddle = Paddle(self.pad_width, self.pad_height, self.width - self.pad_width, ((self.height - self.pad_height) / 2), "red")
        paddle.set_constraints(0, self.height)
        paddle.bind_keys(("up", "down"))
        return paddle
    def create_ai_paddle(self):
        """Creates an AI secondary paddle and returns it

        <PongGame> self
        """
        paddle = PaddleAI(self.pad_width, self.pad_height, self.width - self.pad_width, ((self.height - self.pad_height) / 2), "gray")
        paddle.set_constraints(0, self.height)
        paddle.set_ball(self.ball)
        return paddle
    def reset(self):
        """Resets the game

        <Pong> self
        """
        # resets the scores
        self.scoreboard.reset()
        # resets paddle positions
        self.pad_left.reset()
        self.pad_right.reset()
        # respawn the ball
        self.ball.spawn(self.get_center())
    def on_restart(self):
        """Restarts the game

        <Pong> self
        """
        # create a normal paddle
        self.pad_right = self.create_secondary_paddle()
        # reset the game
        self.reset()
    def on_with_ai(self):
        """Starts a new game with the AI

        <Pong> self
        """
        # creates an AI paddle
        # sets the ball so the AI can track the ball
        self.pad_right = self.create_ai_paddle()
        self.pad_right.set_ball(self.ball)
        # reset the game
        self.reset()
    def on_keyup(self, key):
        """Starts the game

        <Pong> self
        """
        self.pad_left.on_keyup(key)
        self.pad_right.on_keyup(key)
    def on_keydown(self, key):
        """Starts the game

        <Pong> self
        """
        self.pad_left.on_keydown(key)
        self.pad_right.on_keydown(key)
    def get_center(self):
        """Retrieves the board's center position

        <Pong> self
        """
        return [self.width / 2, self.height / 2]
    def detect_collisions(self):
        """Checks if the ball has hit something

        <PongGame> self
        <canvas> canvas
        """
        # retrieve the current position of the ball
        ball_pos = self.ball.get_pos()
        # if the ball has entered the left gutter
        if ball_pos[0] < self.ball.radius + self.pad_width:
            # check if the ball is within the left paddle's verticle constraints
            if ball_pos[1] >= self.pad_left.get_top() and ball_pos[1] <= self.pad_left.get_bottom():
                # reflect the ball's x-axis
                self.ball.reflect_x()
                self.ball.increase_speed()
        elif ball_pos[0] >= self.width - self.ball_radius - self.pad_width:
            # check if the ball is within the right paddle's verticle constraints
            if ball_pos[1] >= self.pad_right.get_top() and ball_pos[1] <= self.pad_right.get_bottom():
                # reflect the ball's x-axis
                self.ball.reflect_x()
                self.ball.increase_speed()
        # if the current x pos is less than the left wall
        if ball_pos[0] < self.ball.radius:
            # player 2 scored
            self.scoreboard.score(1)
            # respawn the ball
            self.ball.spawn(self.get_center(), "right")
        # else, if the current x pos is greater than the right wall
        elif ball_pos[0] >= self.width - self.ball.radius:
            # player 1 scored
            self.scoreboard.score(0)
            # respawn the ball
            self.ball.spawn(self.get_center(), "left")
        # if the current y pos is less than the top wall
        if ball_pos[1] < self.ball.radius:
            self.ball.reflect_y()
        # if the current y pos is greater than the bottom wall
        elif ball_pos[1] >= self.height - self.ball.radius:
            self.ball.reflect_y()
    def draw(self, canvas):
        """The canvas draw handler function

        <Pong> self
        <canvas> canvas
        """
        # draw the lines
        self.lines.draw(canvas)
        # checks if the ball has hit a wall
        self.detect_collisions()
        # draw the ball
        self.ball.draw(canvas)
        # draw the paddles
        self.pad_left.draw(canvas)
        self.pad_right.draw(canvas)
        # draw the scoreboard
        self.scoreboard.draw(canvas)

class Lines:
    def __init__(self, width, height, pad_width, pad_height):
        """Creates the new table lines

        <Lines> self
        <int> width             The width of the board
        <int> height            The height of the board
        <int> pad_width         The pad width
        <int> pad_height        The pad height
        """
        # Set board and pad sizes
        self.width = width
        self.height = height
        self.pad_width = pad_width
        self.pad_height = pad_height
    def draw(self, canvas):
        """Renders the table lines

        <Pong> self
        <canvas> canvas
        """
        # center line
        canvas.draw_line([self.width / 2, 0], [self.width / 2, self.height], 1, "white")
        # left pad line
        canvas.draw_line([self.pad_width, 0], [self.pad_width, self.height], 1, "white")
        # right pad line
        canvas.draw_line([self.width - self.pad_width, 0], [self.width - self.pad_width, self.height], 1, "white")

class Scoreboard:
    def __init__(self, center):
        self.center = center
        self.font_size = 32
        self.font_face = 'monospace';
        # calculate the text positions for the given players
        self.text_positions = [
            [self.center[0] / 2, 50],
            [self.center[0] / 2 + self.center[0], 50]
        ]
        # reset the scores
        self.reset()
    def reset(self):
        """Resets the scoreboard

        <Scoreboard> self
        """
        # create empty list to hold player scores
        self.scores = [0, 0];
    def get_score_pos(self, player_num):
        """Retrieve the position [x, y] of the score for the given player ("left" or "right")

        <Scoreboard> self
        <int> player_num
        """
        return self.text_positions[player_num]
    def score(self, player_num):
        """Increment the score for the given player

        <Scoreboard> self
        <int> player_num
        """
        self.scores[player_num] = self.scores[player_num] + 1
    def get_score(self, player_num):
        """Retrieves the given player's score

        <Scoreboard> self
        <int> player_num
        """
        return self.scores[player_num]
    def draw(self, canvas):
        """Draws the score board

        <Scoreboard> self
        <canvas> canvas
        """
        canvas.draw_text(str(self.get_score(0)), self.get_score_pos(0), self.font_size, 'white', self.font_face)
        canvas.draw_text(str(self.get_score(1)), self.get_score_pos(1), self.font_size, 'white', self.font_face)

class Ball:
    def __init__(self, radius, position):
        """Creates a new ball and draws it on the given canvas

        <Ball> self
        <int> ball_radius       The ball radius
        <list> position         The initial position to spawn the ball
        """
        self.radius = radius
        self.speed = 1.0
        # spawns the ball
        self.spawn(position)
    def get_radius(self):
        return self.radius
    def set_pos(self, pos):
        self.pos = pos
    def get_pos(self):
        return self.pos
    def set_velocity(self, velocity):
        self.velocity = velocity
    def get_velocity(self):
        return self.velocity
    def reflect_x(self):
        # retrieve the old velocity
        vel = self.get_velocity()
        # reflect the x-axis
        vel[0] = -1 * vel[0]
    def reflect_y(self):
        # retrieve the old velocity
        vel = self.get_velocity()
        # reflect the y-axis
        vel[1] = -1 * vel[1]
    def increase_speed(self):
        """Increases the ball's speed

        <Ball> self
        <float> speed
        """
        self.speed = self.speed * 1.1
    def spawn(self, position, direction = None):
        """Spawns the ball at the given position and generates a velocity

        <Ball> self
        <int> position          The position in which to spawn the ball
        <string> direction      Set initial velocity to go "left" or "right"
        """
        # reset the speed
        self.speed = 1
        new_vel = [(random.randint(120, 240) / 60), -1 * (random.randint(60, 180) / 60)]
        modifier = 1
        # If no direction is set
        if direction == None:
            # randomly set the direction modifier
            modifier = random.choice([-1, 1])
        elif direction == "left":
            modifier = -1
        # sets the x-axis direction based on the direction modifier
        new_vel[0] = modifier * new_vel[0]
        self.set_pos(position)
        self.set_velocity(new_vel)
    def update_pos(self):
        """Updates the current position with the new position.

        Applies the velocity to old position

        Returns the new position
        """
        # retrieve the current pos
        old_pos = self.get_pos()
        # retrieve the current vel
        vel = self.get_velocity()
        # apply the velocity to the current pos to get the new pos (applies the ball speed)
        new_pos = [old_pos[0] + (vel[0] * self.speed), old_pos[1] + (vel[1] * self.speed)]
        # sets the new position
        self.set_pos(new_pos)
        # returns the new position
        return new_pos
    def draw(self, canvas):
        """Draws the ball

        <Ball> self
        <canvas> canvas
        """
        # updates the current position
        new_pos = self.update_pos()
        # draws the circle at the new position
        canvas.draw_circle(new_pos, self.radius, 1, "white", "white")


class Paddle:
    def __init__(self, width, height, x, y, color):
        """Creates a new padding of width/height

        <Paddle> self
        <int> width
        <int> height
        <int> x
        <int> y
        <string> color
        """
        self.width = width
        self.height = height
        self.init_x = x
        self.init_y = y
        self.color = color
        self.key_up = None
        self.key_down = None
        self.speed = 3
        self.reset()
    def reset(self):
        """Resets the paddles to the center of the gutter

        <Paddle> self
        """
        self.velocity = [0, 0]
        self.x = self.init_x
        self.y = self.init_y
    def set_constraints(self, min_y, max_y):
        """Sets the y-axis constraints for the paddle

        <Paddle> self
        <int> min
        <int> max
        """
        self.min_y = min_y
        self.max_y = max_y
    def update_points(self):
        """
        Updates and returns the paddle's points

        <Paddle> self
        """
        # calculate the new y pos
        # apply the constraints to the paddle positions
        # take the max of: 0, and the calculated position
        # then, take the min of: the calculated position, and the diff of constraint height and paddle height
        new_y = min(self.max_y - self.height, max(self.min_y, self.y + self.velocity[1] * self.speed))
        # calculate the new pos
        new_pos = [
            [self.x, new_y],
            [self.x + self.width, new_y],
            [self.x + self.width, new_y + self.height],
            [self.x, new_y + self.height]
        ]
        self.y = new_y
        # return the new position
        return new_pos
    def get_points(self):
        """Returns the current position of the paddle

        <Paddle> self
        """
        return [
            [self.x, self.y], # top left
            [self.x + self.width, self.y], # top right
            [self.x + self.width, self.y + self.height], # bottom right
            [self.x, self.y + self.height] # bottom left
        ]
    def get_y_values(self):
        """Retrieve the Y values of the paddle

        <Paddle> self
        """
        values = []
        # retrieve the points
        points = self.get_points()
        # retrieve all y values
        for p in points:
            # add the point's y-axis
            values.append(p[1])
        return values
    def get_top(self):
        """Retrieve the top Y-axis of the paddle

        <Paddle> self
        """
        values = self.get_y_values()
        return min(values)
    def get_bottom(self):
        """Retrieve the bottom Y-axis of the paddle

        <Paddle> self
        """
        return max(self.get_y_values())
    def bind_keys(self, keys):
        """Bind the keys (up, and down)

        <Paddle> self
        <tuple> keys            The up and down keys to bind to the given paddle
        """
        self.key_up = keys[0]
        self.key_down = keys[1]
    def on_keyup(self, key):
        """Reset the velocity (stops moving)

        <Paddle> self
        <int> key
        """
        self.velocity[1] = 0
    def on_keydown(self, key):
        """Moves the paddle down when the "down" key is pressed

        <Paddle> self
        <int> key
        """
        if not self.key_up == None and key == simplegui.KEY_MAP[self.key_up]:
            self.velocity[1] = -1
        if not self.key_down == None and key == simplegui.KEY_MAP[self.key_down]:
            self.velocity[1] = 1
    def draw(self, canvas):
        """Draws the paddle

        <Paddle> self
        <canvas> canvas
        """
        # update the points
        new_points = self.update_points()
        # draws the polygon
        canvas.draw_polygon(new_points, 1, self.color, self.color)

class PaddleAI(Paddle):
    def set_ball(self, ball):
        """Sets the ball

        <Paddle> paddle
        <Ball> ball
        """
        self.ball = ball
    def update_points(self):
        """Updates the position of the paddle based on the ball

        <Paddle> self
        """
        # sets the new y position as the ball's y position
        ball_pos = self.ball.get_pos()
        ball_rad = self.ball.get_radius()
        new_y = min(self.max_y - self.height, max(self.min_y, ball_pos[1] - ball_rad * 2))
        # calculate the new pos
        new_pos = [
            [self.x, new_y],
            [self.x + self.width, new_y],
            [self.x + self.width, new_y + self.height],
            [self.x, new_y + self.height]
        ]
        self.y = new_y
        # return the new position
        return new_pos

# Start a new game
pong = PongGame(FRAME_WIDTH, FRAME_HEIGHT, PAD_WIDTH, PAD_HEIGHT, BALL_RADIUS)
