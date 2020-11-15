import pygame

WIDTH = 800
SCREEN = pygame.display.set_mode((WIDTH, WIDTH))
pygame.display.set_caption("Sudoku Solver")


class Square:
    def __init__(self, row, col, width, total_rows):
        self.row = row
        self.col = col
        self.x = row * width
        self.y = col * width
        self.color = (255, 255, 255)
        self.neighbors = []
        self.width = width
        self.total_rows = total_rows

    # Draw itself as a square
    def draw(self, window):
        pygame.draw.rect(window, self.color, (self.x, self.y, self.width, self.width))


# Create grid as list and append nodes
def make_grid(rows, width):
    grid = []
    gap = width // rows
    for i in range(rows):
        grid.append([])
        for j in range(rows):
            square = Square(i, j, gap, rows)
            grid[i].append(square)
    return grid


# Draw the outline on window
def draw_grid(window, rows, width):
    gap = width // rows
    for i in range(rows):
        if i % 3 == 0:
            pygame.draw.line(window, (0, 0, 0), (0, i * gap), (width, i * gap), 5)
        else:
            pygame.draw.line(window, (0, 0, 0), (0, i * gap), (width, i * gap), 1)
    for j in range(rows):
        if j % 3 == 0:
            pygame.draw.line(window, (0, 0, 0), (j * gap, 0), (j * gap, width), 5)
        else:
            pygame.draw.line(window, (0, 0, 0), (j * gap, 0), (j * gap, width), 1)


# Draw grid squares
def draw(window, grid, rows, width):
    window.fill((255, 255, 255))

    for row in grid:
        for node in row:
            node.draw(window)

    draw_grid(window, rows, width)
    pygame.display.update()


def get_click_pos(pos, rows, width):
    gap = width // rows
    y, x = pos

    row = y // gap
    col = x // gap

    return row, col


def solve(brd):
    find = find_empty(brd)
    if not find:
        return True
    else:
        row, col = find

    for i in range(1, 10):
        if valid(brd, i, (row, col)):
            brd[row][col] = i

            if solve(brd):
                return True

            brd[row][col] = 0

    return False


def valid(brd, num, pos):
    # Check row
    for i in range(len(brd[0])):
        if brd[pos[0]][i] == num and pos[1] != i:
            return False

    # Check column
    for i in range(len(brd)):
        if brd[i][pos[1]] == num and pos[0] != i:
            return False

    # Check square
    square_x = pos[1] // 3
    square_y = pos[0] // 3

    for i in range(square_y * 3, square_y * 3 + 3):
        for j in range(square_x * 3, square_x * 3 + 3):
            if brd[i][j] == num and (i, j) != pos:
                return False

    return True


def find_empty(brd):
    for i in range(len(brd)):
        for j in range(len(brd[0])):
            if brd[i][j] == 0:
                return i, j  # row/col

    return None


def main(window, width):
    grid = make_grid(9, width)
    alive = True

    while alive:
        draw(window, grid, 9, width)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                alive = False
            if pygame.mouse.get_pressed()[0]:  # LMB
                pos = pygame.mouse.get_pos()
                row, col = get_click_pos(pos, 9, width)
                node = grid[row][col]
                print(node)

main(SCREEN, WIDTH)
