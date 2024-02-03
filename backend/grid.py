import pygame
from random import choice, randrange

RES = WIDTH, HEIGHT = 882, 642
TILE = 40
cols, rows = WIDTH // TILE, HEIGHT // TILE

class Cell:
    def __init__(self, x, y):
        self.x, self.y = x, y
        self.legal_moves = []
        self.walls = {'top': True, 'right': True, 'bottom': True, 'left': True}
        self.visited = False
        self.thickness = 4
        self.visits=0
    
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
    
    def update_legal_moves(self):
        self.legal_moves = []
        if not self.walls['top']:
            self.legal_moves.append('up')  # Can move up
        if not self.walls['right']:
            self.legal_moves.append('right')  # Can move right
        if not self.walls['bottom']:
            self.legal_moves.append('down')  # Can move down
        if not self.walls['left']:
            self.legal_moves.append('left')  # Can move left
    
    # allows for the removal of a specific wall.
    def remove_wall(self, wall):
        if wall in self.walls:
            self.walls[wall] = False
            self.update_legal_moves()
            
def remove_walls(current, next):
    dx = current.x - next.x
    if dx == 1:
        current.remove_wall('left')
        next.remove_wall('right')
    elif dx == -1:
        current.remove_wall('right')
        next.remove_wall('left')
    dy = current.y - next.y
    if dy == 1:
        current.remove_wall('top')
        next.remove_wall('bottom')
    elif dy == -1:
        current.remove_wall('bottom')
        next.remove_wall('top')


