import pygame
import random

colors = [
    (0, 0, 0),
    (120, 37, 179),
    (100, 179, 179),
    (80, 34, 22),
    (80, 134, 22),
    (180, 34, 22),
    (180, 34, 122),
]


class Figure:
    # This class represents the different figures that are in this game
    x = 0
    y = 0

    # This double list contains all possible figures
    # The numbers in each list are considered to be on a 4x4 grid
    # The grid looks like this:
    #   0   1   2   3
    #   4   5   6   7
    #   8   9   10  11
    #   12  13  14  15
    figures = [
        [[1, 5, 9, 13], [4, 5, 6, 7]],
        [[4, 5, 9, 10], [2, 6, 5, 9]],
        [[6, 7, 9, 10], [1, 5, 6, 10]],
        [[1, 2, 5, 9], [0, 4, 5, 6], [1, 5, 9, 8], [4, 5, 6, 10]],
        [[1, 2, 6, 10], [5, 6, 7, 9], [2, 6, 10, 11], [3, 5, 6, 7]],
        [[1, 4, 5, 6], [1, 4, 5, 9], [4, 5, 6, 9], [1, 5, 6, 9]],
        [[1, 2, 5, 6]],
    ]

    # We randomly pick a type and colour
    def __init__(self, x, y):
        self.x = x  # Starting position on the board
        self.y = y  # Starting position on the board
        self.type = random.randint(0, len(self.figures) - 1)  # Random value from the array
        self.color = random.randint(1, len(colors) - 1)  # Random value from the figures array
        self.rotation = 0

    def image(self):
        return self.figures[self.type][self.rotation]

    def rotate(self):
        self.rotation = (self.rotation + 1) % len(self.figures[self.type])


class Tetris:
    # contains the game logic
    level = 2
    score = 0
    state = "start"
    # This contains the game field when are playing
    field = []
    height = 0
    width = 0
    # Position of the game field
    x = 100  # original: 100
    y = 60  # original: 60
    zoom = 20  # original:
    players = 0
    # figure = None
    figure = [None]

    def __init__(self, height, width, numberOfPlayers):
        self.height = height
        self.width = width
        self.field = []
        self.score = 0
        self.state = "start"
        self.players = numberOfPlayers
        self.figure *= numberOfPlayers
        # Creating the gameBoard according to the preferred size
        for i in range(self.height):
            new_line = []
            for j in range(self.width):
                new_line.append(0)
            self.field.append(new_line)

    def new_figure(self, players):
        if players == 1:
            self.figure[0] = Figure(3, 0)
        elif players == 2:
            # Then we need an array of players that can be looped through containing the respective figure for each player
            # Starting positions: P1 (3,0), P2 (width-3, 0)
            self.figure[0] = Figure(3, 0)
            self.figure[1] = Figure (self.width - 3, 0)
        elif players == 3:
            # Starting positions: P1 (3,0), P2 (11, 0), P3(width-3,0)
            self.figure[0] = Figure(3, 0)
            self.figure[1] = Figure(8, 0)
            self.figure[2] = Figure(self.width - 3, 0)
        else:
            # Only up to four players supported
            # Starting positions: P1 (3,0), P2 (11, 0), P3(19, 0), P4(width-3, 0)
            self.figure[0] = Figure(3, 0)
            self.figure[1] = Figure(8, 0)
            self.figure[2] = Figure(15, 0)
            self.figure[3] = Figure(self.width - 3, 0)

    # Check if the currently moving object is intersecting with another object
    def intersects(self, index):
        intersection = False
        for i in range(4):
            for j in range(4):
                if i * 4 + j in self.figure[index].image():
                    if i + self.figure[index].y > self.height - 1 or \
                            j + self.figure[index].x > self.width - 1 or \
                            j + self.figure[index].x < 0 or \
                            self.field[i + self.figure[index].y][j + self.figure[index].x] > 0:
                        intersection = True
        return intersection

    # Do we have a full line on the game field then we need to break it and raise the score
    # Goes from the bottom to the top
    def break_lines(self):
        lines = 0
        for i in range(1, self.height):
            zeros = 0
            for j in range(self.width):
                if self.field[i][j] == 0:
                    zeros += 1
            if zeros == 0:
                lines += 1
                for i1 in range(i, 1, -1):
                    for j in range(self.width):
                        self.field[i1][j] = self.field[i1 - 1][j]
        self.score += lines ** 2

    def go_space(self):
        while not self.intersects():
            self.figure.y += 1
        self.figure.y -= 1
        self.freeze()

    def go_down(self):
        for i in range(len(self.figure)):
            self.figure[i].y += 1
            if self.intersects(i):
                self.figure[i].y -= 1
                self.freeze(i)

    # If we intersect while we are going down, we have reached the end
    # we need to freeze the figure
    def freeze(self, index):
        for i in range(4):
            for j in range(4):
                if i * 4 + j in self.figure[index].image():
                    self.field[i + self.figure[index].y][j + self.figure[index].x] = self.figure[index].color
        self.break_lines()
        self.new_figure(self.players)
        if self.intersects(index):
            self.state = "gameover"

    def go_side(self, dx, index):
        old_x = self.figure[index].x
        self.figure[index].x += dx
        if self.intersects(index):
            self.figure[index].x = old_x

    def rotate(self):
        old_rotation = self.figure.rotation
        self.figure.rotate()
        if self.intersects():
            self.figure.rotation = old_rotation


# Initialize the game engine
pygame.init()

# Define some colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GRAY = (128, 128, 128)

# original: (400,500)
size = (800, 1000)
screen = pygame.display.set_mode(size)

pygame.display.set_caption("Tetris")

# Loop until the user clicks the close button.
done = False
clock = pygame.time.Clock()
fps = 25

# original: Tetris(20,10) Todo: Adapt the gameBoardSize depending on the amount of people playing
number_of_players = 3;
# Gameboard size depending on the number of players: 1) 20x10 2) 26x16 3) 29x19) 4) 32x22
game = Tetris(number_of_players * 3 + 20 if number_of_players > 1 else 20, number_of_players * 3 + 10 if number_of_players > 1 else 10, number_of_players)
counter = 0

pressing_down = False

# game loop
while not done:
    #TODO: Could lead to problems but needs to be tested (maybe check all figures?)
    if game.figure[0] is None:
        game.new_figure(number_of_players)
        print(game.figure)
    counter += 1
    if counter > 100000:
        counter = 0

    if counter % (fps // game.level // 2) == 0 or pressing_down:
        if game.state == "start":
            game.go_down()

    # Track the users keyboard input
    #TODO: Control of the bricks only works for one player so far
    # the rest just goes down without moving
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                game.figure[0].rotate()  # Figure index
            if event.key == pygame.K_DOWN:
                pressing_down = True
            if event.key == pygame.K_LEFT:
                game.go_side(-1, 0)   # Second argument is figure index
            if event.key == pygame.K_RIGHT:
                game.go_side(1, 0)
            if event.key == pygame.K_SPACE:
                game.go_space()
            if event.key == pygame.K_ESCAPE:
                game.__init__(20, 10)

    if event.type == pygame.KEYUP:
        if event.key == pygame.K_DOWN:
            pressing_down = False

    screen.fill(WHITE)

    # Drawing the game board -> pygame stuff
    for i in range(game.height):
        for j in range(game.width):
            pygame.draw.rect(screen, GRAY, [game.x + game.zoom * j, game.y + game.zoom * i, game.zoom, game.zoom], 1)
            if game.field[i][j] > 0:
                pygame.draw.rect(screen, colors[game.field[i][j]],
                                 [game.x + game.zoom * j + 1, game.y + game.zoom * i + 1, game.zoom - 2, game.zoom - 1])

    # Draw game board -> pygame stuff
    if game.figure[0] is not None:
        for i in range(4):
            for j in range(4):
                p = i * 4 + j
                for o in range(len(game.figure)):
                    if p in game.figure[o].image():
                        pygame.draw.rect(screen, colors[game.figure[o].color],
                                        [game.x + game.zoom * (j + game.figure[o].x) + 1,
                                        game.y + game.zoom * (i + game.figure[o].y) + 1,
                                        game.zoom - 2, game.zoom - 2])

    font = pygame.font.SysFont('Calibri', 25, True, False)
    font1 = pygame.font.SysFont('Calibri', 65, True, False)
    text = font.render("Score: " + str(game.score), True, BLACK)
    text_game_over = font1.render("Game Over", True, (255, 125, 0))
    text_game_over1 = font1.render("Press ESC", True, (255, 215, 0))

    screen.blit(text, [0, 0])
    if game.state == "gameover":
        screen.blit(text_game_over, [20, 200])
        screen.blit(text_game_over1, [25, 265])

    pygame.display.flip()
    clock.tick(fps)

pygame.quit()
