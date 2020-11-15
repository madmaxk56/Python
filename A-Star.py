# A-Star Pathfinding Algorithm
# Author: Max Krider
# Date: July 2020

# Pygame and PriorityQue Imports
from queue import PriorityQueue
import pygame

# Window Creation
WIDTH = 800
SCREEN = pygame.display.set_mode((WIDTH, WIDTH))
pygame.display.set_caption("A* Pathfinder")

# RGB Color Format Constants
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
PURPLE = (128, 0, 128)
ORANGE = (255, 165, 0)
GREY = (128, 128, 128)
TURQUOISE = (64, 244, 208)


# Each individual square as a node
class Node:
    # Initiation
    def __init__(self, row, col, width, total_rows):
        self.row = row
        self.col = col
        self.x = row * width
        self.y = col * width
        self.color = GREY
        self.neighbors = []
        self.width = width
        self.total_rows = total_rows

    # Returns position as tuple
    def get_pos(self):
        return self.row, self.col

    # Returns status as boolean via color
    def is_mapped(self):
        return self.color == BLUE

    def is_frontier(self):
        return self.color == GREEN

    def is_wall(self):
        return self.color == BLACK

    def is_home(self):
        return self.color == RED

    def is_destination(self):
        return self.color == YELLOW

    # Resets grid
    def reset(self):
        self.color = GREY

    # Sets status via color
    def make_mapped(self):
        self.color = BLUE

    def make_frontier(self):
        self.color = GREEN

    def make_wall(self):
        self.color = BLACK

    def make_home(self):
        self.color = RED

    def make_destination(self):
        self.color = YELLOW

    def make_path(self):
        self.color = TURQUOISE

    # Draw itself as a square
    def draw(self, window):
        pygame.draw.rect(window, self.color, (self.x, self.y, self.width, self.width))

    # Appends neighbors in 4-directions only if they are traversable
    def update_neighbors(self, grid):
        self.neighbors = []
        if self.row < self.total_rows - 1 and not grid[self.row + 1][self.col].is_wall():  # Under
            self.neighbors.append(grid[self.row + 1][self.col])

        if self.row > 0 and not grid[self.row - 1][self.col].is_wall():  # Above
            self.neighbors.append(grid[self.row - 1][self.col])

        if self.col < self.total_rows - 1 and not grid[self.row][self.col + 1].is_wall():  # Right of
            self.neighbors.append(grid[self.row][self.col + 1])

        if self.col > 0 and not grid[self.row][self.col - 1].is_wall():  # Left of
            self.neighbors.append(grid[self.row][self.col - 1])

    # For node comparison. Will be always less than
    def __lt__(self, other):
        return False


# Create grid as list and append nodes
def make_grid(rows, width):
    grid = []
    gap = width // rows
    for i in range(rows):
        grid.append([])
        for j in range(rows):
            node = Node(i, j, gap, rows)
            grid[i].append(node)
    return grid


# Draw the outline on window
def draw_grid(window, rows, width):
    gap = width // rows
    for i in range(rows):
        pygame.draw.line(window, WHITE, (0, i * gap), (width, i * gap))
        for j in range(rows):
            pygame.draw.line(window, WHITE, (j * gap, 0), (j * gap, width))


# Draw grid squares
def draw(window, grid, rows, width):
    window.fill(WHITE)

    for row in grid:
        for node in row:
            node.draw(window)

    draw_grid(window, rows, width)
    pygame.display.update()


# Find square based on mouse pixel click
def get_click_pos(pos, rows, width):
    gap = width // rows
    y, x = pos

    row = y // gap
    col = x // gap

    return row, col


# A* Heuristic Function
def h(p1, p2):
    x1, y1 = p1
    x2, y2 = p2
    return abs(x2 - x1) + abs(y2 - y1)


# Highlight shortest path after solve
def build_shortest_path(last_node, current, draws):
    while current in last_node:
        current = last_node[current]
        current.make_path()
        draws()


# Clears pathing
def path_clear(grid, rows):
    for i in range(rows):
        for j in range(rows):
            node = grid[i][j]
            if not node.is_wall() and not node.is_home() and not node.is_destination():
                node.reset()


# A* Algorithm
def a_star(draws, grid, home, destination):
    count = 0
    open_set = PriorityQueue()
    open_set.put((0, count, home))
    last_node = {}
    g_score = {node: float("inf") for row in grid for node in row}
    g_score[home] = 0

    f_score = {node: float("inf") for row in grid for node in row}
    f_score[home] = h(home.get_pos(), destination.get_pos())

    open_set_hash = {home}

    while not open_set.empty():
        # Escape events for both keyboard and mouse
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return False

        # Get Node Object
        current = open_set.get()[2]
        open_set_hash.remove(current)

        # Shortest Path Found
        if current == destination:
            build_shortest_path(last_node, destination, draws)
            destination.make_destination()
            return True

        # Calculating neighboring F and G score values. Best path is stored
        for neighbor in current.neighbors:
            g_score_temp = g_score[current] + 1

            if g_score_temp < g_score[neighbor]:
                last_node[neighbor] = current
                g_score[neighbor] = g_score_temp
                f_score[neighbor] = g_score_temp + h(neighbor.get_pos(), destination.get_pos())

                if neighbor not in open_set_hash:
                    count += 1
                    open_set.put((f_score[neighbor], count, neighbor))
                    open_set_hash.add(neighbor)
                    neighbor.make_frontier()

        # Anonymous Function usage
        draws()

        if current != home:
            current.make_mapped()

    return False


# Main function
def main(window, width):
    rows = 50
    grid = make_grid(rows, width)

    # Start and End points
    home = None
    destination = None

    # Run until interrupt
    alive = True
    while alive:
        draw(window, grid, rows, width)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                alive = False
            # LMB sets square values
            if pygame.mouse.get_pressed()[0]:  # LMB
                pos = pygame.mouse.get_pos()
                row, col = get_click_pos(pos, rows, width)
                node = grid[row][col]
                if not home and node != destination:
                    home = node
                    home.make_home()
                elif not destination and node != home:
                    destination = node
                    destination.make_destination()
                elif node != home and node != destination:
                    node.make_wall()

            # RMB resets pressed square
            elif pygame.mouse.get_pressed()[2]:
                pos = pygame.mouse.get_pos()
                row, col = get_click_pos(pos, rows, width)
                node = grid[row][col]
                node.reset()
                if node == home:
                    home = None
                elif node == destination:
                    destination = None

            # Keyboard Event
            if event.type == pygame.KEYDOWN:
                # Spacebar to start algorithm
                if event.key == pygame.K_SPACE and home and destination:
                    for row in grid:
                        for node in row:
                            node.update_neighbors(grid)

                    # Anonymous Function call in A*
                    a_star(lambda: draw(window, grid, rows, width), grid, home, destination)

                # Escape to clear
                if event.key == pygame.K_ESCAPE:
                    home = None
                    destination = None
                    grid = make_grid(rows, width)

                # reset pathing
                if event.key == pygame.K_r:
                    path_clear(grid, rows)
    pygame.quit()


# Code to Run
main(SCREEN, WIDTH)
