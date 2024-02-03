from grid import Cell

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
        if new_cell is not None and 'up' in self.current_cell.legal_moves:
            self.current_cell = new_cell
            return self.current_cell
        return None

    def move_right(self):
        new_cell = self.check_cell(self.current_cell.x + 1, self.current_cell.y)
        if new_cell is not None and 'right' in self.current_cell.legal_moves:
            self.current_cell = new_cell
            return self.current_cell
        return None

    def move_down(self):
        new_cell = self.check_cell(self.current_cell.x, self.current_cell.y + 1)
        if new_cell is not None and 'down' in self.current_cell.legal_moves:
            self.current_cell = new_cell
            return self.current_cell
        return None

    def move_left(self):
        new_cell = self.check_cell(self.current_cell.x - 1, self.current_cell.y)
        if new_cell is not None and 'left' in self.current_cell.legal_moves:
            self.current_cell = new_cell
            return self.current_cell
        return None

    def step(self, action):
        # Define action mappings to directions
        action_directions = {0: 'up', 1: 'right', 2: 'down', 3: 'left'}
        current_direction = action_directions.get(action)

        # Initialize reward and done flag
        reward = 0
        done = False

        # Perform the action if it's legal
        if current_direction in self.current_cell.legal_moves:
            new_cell = None
            if action == 0:
                new_cell = self.move_up()
            elif action == 1:
                new_cell = self.move_right()
            elif action == 2:
                new_cell = self.move_down()
            elif action == 3:
                new_cell = self.move_left()
            
            if new_cell is not None:
                self.current_cell = new_cell
                if self.current_cell.visited:
                    reward = -0.2  # Penalize for revisiting a cell
                else:
                    reward = -0.1  # Standard penalty for a move
                    self.current_cell.visited = True  # Mark the cell as visited
                if self.current_cell == self.goal_cell:
                    reward = 1  # Reward for reaching the goal
                    done = True
        else:
            # If the move is not legal, don't change the cell
            pass
        next_state = self.grid_cells.index(self.current_cell)
        self.current_cell = self.grid_cells[next_state] 
        reward = -0.01
        done = self.current_cell == self.goal_cell
        if done: 
            reward = 5

        next_state = self.grid_cells.index(self.current_cell)
        return next_state, reward, done, self.current_cell




    def reset(self):
        self.current_cell = self.start_cell
        for cell in self.grid_cells:
            cell.visits = 0 
        for cell in self.grid_cells:
            cell.visited = False
        return self.grid_cells.index(self.current_cell)
