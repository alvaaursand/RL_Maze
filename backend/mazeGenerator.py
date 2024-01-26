import pygame
from random import choice, randrange

RES = WIDTH, HEIGHT = 882, 642
TILE = 40
cols, rows = WIDTH // TILE, HEIGHT // TILE

class Cell:
    def __init__(self, x, y):
        self.x, self.y = x, y
        self.walls = {'top': True, 'right': True, 'bottom': True, 'left': True}
        self.visited = False
        self.thickness = 4

    def draw(self, sc):
        x, y = self.x * TILE, self.y * TILE

        if self.walls['top']:
            pygame.draw.line(sc, pygame.Color('#455945'), (x, y), (x + TILE, y), self.thickness)
        if self.walls['right']:
            pygame.draw.line(sc, pygame.Color('#455945'), (x + TILE, y), (x + TILE, y + TILE), self.thickness)
        if self.walls['bottom']:
            pygame.draw.line(sc, pygame.Color('#455945'), (x + TILE, y + TILE), (x , y + TILE), self.thickness)
        if self.walls['left']:
            pygame.draw.line(sc, pygame.Color('#455945'), (x, y + TILE), (x, y), self.thickness)

    def get_rects(self):
        rects = []
        x, y = self.x * TILE, self.y * TILE
        if self.walls['top']:
            rects.append(pygame.Rect( (x, y), (TILE, self.thickness) ))
        if self.walls['right']:
            rects.append(pygame.Rect( (x + TILE, y), (self.thickness, TILE) ))
        if self.walls['bottom']:
            rects.append(pygame.Rect( (x, y + TILE), (TILE , self.thickness) ))
        if self.walls['left']:
            rects.append(pygame.Rect( (x, y), (self.thickness, TILE) ))
        return rects

    def check_cell(self, x, y):
        find_index = lambda x, y: x + y * cols
        if x < 0 or x > cols - 1 or y < 0 or y > rows - 1:
            return False
        return self.grid_cells[find_index(x, y)]

    def check_neighbors(self, grid_cells):
        self.grid_cells = grid_cells
        neighbors = []
        top = self.check_cell(self.x, self.y - 1)
        right = self.check_cell(self.x + 1, self.y)
        bottom = self.check_cell(self.x, self.y + 1)
        left = self.check_cell(self.x - 1, self.y)
        if top and not top.visited:
            neighbors.append(top)
        if right and not right.visited:
            neighbors.append(right)
        if bottom and not bottom.visited:
            neighbors.append(bottom)
        if left and not left.visited:
            neighbors.append(left)
        return choice(neighbors) if neighbors else False
    
    # allows for the removal of a specific wall.
    def remove_wall(self, wall):
        if wall in self.walls:
            self.walls[wall] = False


def remove_walls(current, next):
    dx = current.x - next.x
    if dx == 1:
        current.walls['left'] = False
        next.walls['right'] = False
    elif dx == -1:
        current.walls['right'] = False
        next.walls['left'] = False
    dy = current.y - next.y
    if dy == 1:
        current.walls['top'] = False
        next.walls['bottom'] = False
    elif dy == -1:
        current.walls['bottom'] = False
        next.walls['top'] = False

def generate_maze():
    grid_cells = [Cell(col, row) for row in range(rows) for col in range(cols)]
    current_cell = grid_cells[0]
    stack = []
    break_count = 1

    while break_count != len(grid_cells):
        current_cell.visited = True
        next_cell = current_cell.check_neighbors(grid_cells)
        if next_cell:
            next_cell.visited = True
            break_count += 1
            stack.append(current_cell)
            remove_walls(current_cell, next_cell)
            current_cell = next_cell
        elif stack:
            current_cell = stack.pop()

    # Remove the left wall of the start cell and the right wall of the goal cell
    start_cell = grid_cells[0]  # Assuming the start cell is the first cell
    goal_cell = grid_cells[-1]  # Assuming the goal cell is the last cell
    start_cell.walls['left'] = False
    goal_cell.walls['right'] = False

    return grid_cells