"""Program that creates Breakout and allows user to play interactively."""

import pygame as P
import random as R
import pygame.time as T


class Game:
    """Class for the actual game including set up and loop for the game."""
    # to get display, call P.display, P.event
    # Constants
    WIDTH = 400
    HEIGHT = 400
    SCREEN = None
    PADDLE_SPEED = 5
    BALL_SPEED = 3
    lives = None
    score = None
    started = False
    paused = False
    over = False
    won = False
    time = 0

    def initiate(self):
        """Initiates the game and sets up the screen."""
        P.init()
        Game.lives = 3
        Game.score = 0
        Game.SCREEN = P.display.set_mode((Game.WIDTH, Game.HEIGHT))
        self.play = Play()
        self.play.__init__()

    def game_loop(self):
        """Function for the main game loop."""
        clock = T.Clock()
        current_time = T.get_ticks()
        leftover = 0.0

        while True:
            self.play.draw()
            P.display.update()

            new_time = T.get_ticks()
            frame_time = (new_time - current_time) / 1000.0
            current_time = new_time
            clock.tick()
            leftover += frame_time
            while leftover > 0.01:
                self.play.update()
                leftover -= 0.01

            P.event.pump()
            for e in P.event.get():
                if e.type == P.QUIT:
                    exit()
                else:
                    self.play.handle_keys(e)


class Play:
    """Class for playing the game."""
    bricks = None
    b_rows = 7
    b_cols = 10

    def __init__(self):
        """Function that initiates the game and creates bricks."""
        self.paddle = Paddle()
        self.ball = Ball()
        Play.bricks = []
        for i in range(Play.b_cols):
            for j in range(Play.b_rows):
                    Play.bricks.append(Brick(P.Rect(i * 40, j * 10, 40, 10)))
        pass

    def draw(self):
        """Draws components of the game and also adds messages."""
        Game.SCREEN.fill((255, 255, 255))
        P.draw.rect(Game.SCREEN, (0, 0, 0),
                    P.Rect((0, Game.HEIGHT - 50, Game.WIDTH, 50)), 0)
        font = P.font.Font(None, 40)
        lives_label = font.render('Lives: ' + str(Game.lives), 1, (12, 32, 90))
        score_label = font.render('Score: ' + str(Game.score), 1, (12, 32, 90))
        P.draw.rect(Game.SCREEN, (100, 100, 100), self.paddle.rect, 0)
        for brick in Play.bricks:
            if brick.is_visible:
                P.draw.rect(Game.SCREEN, brick.color, brick.rect, 0)
        P.draw.rect(Game.SCREEN, (45, 45, 45), self.ball.rect, 0)
        Game.SCREEN.blit(lives_label, (0, Game.HEIGHT - 45))
        Game.SCREEN.blit(score_label, (150, Game.HEIGHT - 45))
        if not Game.started or Game.paused:
            msg = ''
            if not Game.started:
                msg = 'Press Space to start!'
            elif Game.paused:
                msg = 'Press Space to unpause.'
            if Game.over:
                font = P.font.Font(None, 20)
                if Game.won:
                    msg = "Congrats, you won the game! Press Space" + \
                        " to play again."
                else:
                    msg = "Game over! Score: " + str(Game.score) + \
                        " Press Space to play again."
            if Game.time < 50:
                start_prompt = font.render(msg,
                                           1, (12, 32, 90))
                start_prompt_pos = start_prompt.get_rect()
                surf = P.Surface(
                    Game.SCREEN.get_size()).get_rect()
                start_prompt_pos.centerx = surf.centerx
                start_prompt_pos.centery = surf.centery - 20
                Game.SCREEN.blit(start_prompt, start_prompt_pos)
                Game.time += 1
            elif Game.time < 100:
                Game.time += 1
            else:
                Game.time = 0

    def update(self):
        """updates game: including paddle moves and collision check."""
        keys_pressed = P.key.get_pressed()
        if not Game.paused and not Game.over:
            if keys_pressed[P.K_LEFT]:
                self.paddle.move_left()
                if not Game.started:
                    self.ball.move_left()
            if keys_pressed[P.K_RIGHT]:
                self.paddle.move_right()
                if not Game.started:
                    self.ball.move_right()
            if Game.started:
                self.ball.update()
                self.check_collision()

    def handle_keys(self, event):
        """Function that deals with key assignments and their effects."""
        if event.type == P.KEYDOWN:
            if event.key == P.K_LEFT and not Game.paused and not Game.over:
                self.paddle.move_left()
                if not Game.started:
                    self.ball.move_left()
            elif event.key == P.K_RIGHT and not Game.paused and not Game.over:
                self.paddle.move_right()
                if not Game.started:
                    self.ball.move_right()
            elif event.key == P.K_SPACE:
                if Game.over:
                    self.restart()
                elif not Game.started:
                    Game.started = True
                else:
                    Game.paused = not Game.paused
            elif event.key == P.K_1:
                for brick in Play.bricks:
                    if brick.is_visible:
                        brick.is_visible = False
                        Game.score += 1
                Game.won = True
                Game.over = True
                Game.started = False
                self.paddle.rect.centerx = Game.WIDTH / 2
                self.ball.rect.centerx = self.paddle.rect.centerx
                self.ball.rect.y = Game.HEIGHT - 70
                Ball.ball_speed_x = -Game.BALL_SPEED
                Ball.ball_speed_y = -Game.BALL_SPEED

    def restart(self):
        """Function that deals with restarting the game after gameover."""
        Game.over = False
        Game.paused = False
        Game.started = False
        Game.won = False
        Game.score = 0
        Game.lives = 3
        for brick in Play.bricks:
            if not brick.is_visible:
                brick.is_visible = True

    def check_collision(self):
        """Checks collision between objects in the game and gives effect."""
        col = False
        for brick in Play.bricks:
            if brick.is_visible and self.ball.rect.colliderect(brick.rect):
                col = True
                # ball going right
                if Ball.ball_speed_x > 0 and \
                        self.ball.rect.right > brick.rect.left and \
                        abs(self.ball.rect.right - brick.rect.left) < 10:
                    self.ball.rect.right = brick.rect.left
                    Ball.ball_speed_x = -Ball.ball_speed_x
                # ball going left
                elif Ball.ball_speed_x < 0 and \
                        self.ball.rect.left < brick.rect.right and \
                        abs(self.ball.rect.left - brick.rect.right) < 10:
                    self.ball.rect.left = brick.rect.right
                    Ball.ball_speed_x = -Ball.ball_speed_x
                # ball going up
                if Ball.ball_speed_y < 0 and \
                        self.ball.rect.top < brick.rect.bottom and \
                        abs(self.ball.rect.top - brick.rect.bottom) < 10:
                    self.ball.rect.top = brick.rect.bottom
                    Ball.ball_speed_y = -Ball.ball_speed_y
                #ball going down
                elif Ball.ball_speed_y > 0 and \
                        self.ball.rect.bottom > brick.rect.top and \
                        abs(self.ball.rect.bottom - brick.rect.top) < 10:
                    self.ball.rect.bottom = brick.rect.top
                    Ball.ball_speed_y = -Ball.ball_speed_y
                if col:
                    brick.is_visible = False
                    Game.score += 1
                    if self.check_win():
                        Game.won = True
                        Game.over = True
                        Game.started = False
                        self.ball.rect.centerx = self.paddle.rect.centerx
                        self.ball.rect.y = Game.HEIGHT - 70
                        Ball.ball_speed_x = -Game.BALL_SPEED
                        Ball.ball_speed_y = -Game.BALL_SPEED
                    return
        if self.ball.rect.x < 0:
            self.ball.rect.x = 0
            Ball.ball_speed_x = -Ball.ball_speed_x
        if self.ball.rect.x > (Game.WIDTH - 10):
            self.ball.rect.x = Game.WIDTH - 10
            Ball.ball_speed_x = -Ball.ball_speed_x
        if self.ball.rect.y < 0:
            self.ball.rect.y = 0
            Ball.ball_speed_y = -Ball.ball_speed_y
        if self.ball.rect.colliderect(self.paddle.rect):
            if Ball.ball_speed_x > 0 and \
                    self.ball.rect.right > self.paddle.rect.left and \
                    abs(self.ball.rect.right - self.paddle.rect.left) < 10:
                self.ball.rect.right = self.paddle.rect.left - \
                    (Game.PADDLE_SPEED + 1)
                Ball.ball_speed_x = -Ball.ball_speed_x
            # ball going left
            elif Ball.ball_speed_x < 0 and \
                    self.ball.rect.left < self.paddle.rect.right and \
                    abs(self.ball.rect.left - self.paddle.rect.right) < 10:
                self.ball.rect.left = self.paddle.rect.right + \
                    (Game.PADDLE_SPEED + 1)
                Ball.ball_speed_x = -Ball.ball_speed_x
            # ball going down
            if Ball.ball_speed_y > 0 and \
                    self.ball.rect.bottom > self.paddle.rect.top and \
                    abs(self.ball.rect.bottom - self.paddle.rect.top) < 10:
                self.ball.rect.bottom = self.paddle.rect.top
            Ball.ball_speed_y = - Ball.ball_speed_y
        if self.ball.rect.y > Game.HEIGHT:
            self.ball.rect.y = Game.HEIGHT - 70
            Game.lives -= 1
            Game.started = False
            self.ball.rect.centerx = self.paddle.rect.centerx
            Ball.ball_speed_x = -Game.BALL_SPEED
            Ball.ball_speed_y = -Game.BALL_SPEED
            if Game.lives == 0:
                Game.over = True

    def check_win(self):
        for brick in Play.bricks:
            if brick.is_visible:
                return False
        return True


class Paddle:
    """Class for the paddle."""
    def __init__(self):
        """Creates the paddle."""
        self.rect = P.Rect(((Game.WIDTH / 2) - 37.5, Game.HEIGHT - 60, 75, 10))

    def move_right(self):
        """Assigns right movement to the paddle."""
        if (self.rect.x + 75) < Game.WIDTH:
            self.rect = self.rect.move(Game.PADDLE_SPEED, 0)
        else:
            self.rect.x = Game.WIDTH - 75

    def move_left(self):
        """Assigns left movement to the paddle."""
        if self.rect.x > 0:
            self.rect = self.rect.move(-Game.PADDLE_SPEED, 0)
        else:
            self.rect.x = 0


class Brick:
    """Class for the brick."""
    def __init__(self, loc):
        """Sets up the bricks and assigns random colors to them."""
        self.rect = loc
        self.is_visible = True
        r = R.randint(0, 200)
        g = R.randint(0, 200)
        b = R.randint(0, 200)
        self.color = (r, g, b)


class Ball:
    """Class for the ball."""
    ball_speed_x = None
    ball_speed_y = None

    def __init__(self):
        """Sets up the ball and assigns ball a speed for each coordinate."""
        self.rect = P.Rect(((Game.WIDTH / 2) - 5, Game.HEIGHT - 70, 10, 10))
        Ball.ball_speed_x = -Game.BALL_SPEED
        Ball.ball_speed_y = -Game.BALL_SPEED

    def move_left(self):
        """Assigns left movement to the ball."""
        if (self.rect.x - 32) > 0:
            self.rect = self.rect.move(-Game.PADDLE_SPEED, 0)
        else:
            self.rect.x = 32

    def move_right(self):
        """Assigns right movement to the ball."""
        if (self.rect.x + 43) < Game.WIDTH:
            self.rect = self.rect.move(Game.PADDLE_SPEED, 0)
        else:
            self.rect.x = Game.WIDTH - 43

    def update(self):
        """Function that updates the ball's state."""
        self.rect.x += Ball.ball_speed_x
        self.rect.y += Ball.ball_speed_y

if __name__ == "__main__":
    game = Game()
    game.initiate()
    game.game_loop()
