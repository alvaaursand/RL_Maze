from mazeGenerator import Cell

class Maze:
    def __init__(self, grid_cells, cols, rows, start_cell=None, goal_cell=None):
        # Ensure that grid_cells is a list of Cell instances
        assert all(isinstance(cell, Cell) for cell in grid_cells), "grid_cells must be a list of Cell instances"
        
        self.grid_cells = grid_cells
        self.cols = cols
        self.rows = rows
        self.start_cell = start_cell if start_cell is not None else self.grid_cells[0]
        self.goal_cell = goal_cell if goal_cell is not None else self.grid_cells[-1]
        self.current_cell = self.start_cell

    @property
    def goal_position(self):
        # Ensure that self.goal_cell is indeed a Cell instance
        assert isinstance(self.goal_cell, Cell), "self.goal_cell must be a Cell instance"
        return (self.goal_cell.x, self.goal_cell.y)
    
    def check_cell(self, x, y):
        if x < 0 or x >= self.cols or y < 0 or y >= self.rows:
            return None
        find_index = lambda x, y: x + y * self.cols
        return self.grid_cells[find_index(x, y)]


    def move_up(self):
        new_cell = self.check_cell(self.current_cell.x, self.current_cell.y - 1)
        if new_cell is not None:
            self.current_cell = new_cell

    def move_right(self):
        new_cell = self.check_cell(self.current_cell.x + 1, self.current_cell.y)
        if new_cell is not None:
            self.current_cell = new_cell

    def move_down(self):
        new_cell = self.check_cell(self.current_cell.x, self.current_cell.y + 1)
        if new_cell is not None:
            self.current_cell = new_cell

    def move_left(self):
        new_cell = self.check_cell(self.current_cell.x - 1, self.current_cell.y)
        if new_cell is not None:
            self.current_cell = new_cell

    def step(self, action):
        if action == 0: 
            self.move_up()
        elif action == 1: 
            self.move_right()
        elif action == 2: 
            self.move_down()
        elif action == 3: 
            self.move_left()

        next_state = self.grid_cells.index(self.current_cell)
        reward = 0 
        done = self.current_cell == self.goal_cell
        if done: 
            reward = 1

        return next_state, reward, done, self.current_cell

    def reset(self):
        self.current_cell = self.start_cell
        return self.grid_cells.index(self.current_cell)
