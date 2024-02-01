import numpy as np
from agent import CuriosityAgent
from grid import *
from maze import *
import threading
#get the window size of this computer

class GUI:
    def __init__(self, display, maze_display, tile_size, agent_image):
        self.display = display
        self.maze_display = maze_display
        self.tile_size = tile_size
        self.agent_image = agent_image

    def update_gui(self, grid, agent_position):
        self.maze_display.fill(pygame.Color('black'))
        for cell in grid:
            cell.draw(self.maze_display)

        # Only draw the agent if agent_position is not None
        if agent_position is not None:
            agent_x, agent_y = agent_position  # Unpack the coordinates here
            self.maze_display.blit(self.agent_image, (agent_x * self.tile_size, agent_y * self.tile_size))
        
        self.display.blit(self.maze_display, (maze_x, maze_y))
        pygame.display.flip()
        
LARGE_RES = LARGER_WIDTH, LARGER_HEIGHT = 1202, 902

pygame.init()
DISPLAY = pygame.display.set_mode(LARGE_RES)
pygame.display.set_caption("Dynamic Maze")
bg = pygame.image.load('images/bg.jpg').convert()
bg = pygame.transform.scale(bg, LARGE_RES)
maze_display = pygame.Surface(RES)

clock = pygame.time.Clock()


maze_complete = False
agent_present = False


# Generate the initial maze grid
grid_cells = [Cell(col, row) for row in range(rows) for col in range(cols)]
current_cell = grid_cells[0]
start_cell = grid_cells[0]  # Start cell is at [0,0]
goal_cell = grid_cells[-1]   # Goal cell is at [cols-1, rows-1]
stack = []

# Initialize the mazeMatrix
mazeMatrix = [[0] * cols for _ in range(rows)]

agent = CuriosityAgent(cols * rows, 4, Maze(grid_cells, cols, rows, start_cell, goal_cell))
agent_state = cols * start_cell.y + start_cell.x
training_completed_event = threading.Event()
training_thread = None
thread_lock = threading.Lock()



# Define button properties
button_color = pygame.Color('#455945')  # Button color
button_hover_color = pygame.Color('white')  # Button color when hovered over
button_position = (LARGER_WIDTH - 202, 90)  # Adjust as needed
button_size = (42, 42)  # Width, Height
button_rect = pygame.Rect(*button_position, *button_size)
button_image = pygame.image.load('./images/play.png')  # Load the button image
button_image = pygame.transform.scale(button_image, (30, 30))
arrow_size = TILE // 3

maze_x = (LARGER_WIDTH - WIDTH) // 2
maze_y = (LARGER_HEIGHT - HEIGHT) // 2

# Load the lightsaber image
lightsaber_image = pygame.image.load('./images/lightsaber.png')
lightsaber_image = pygame.transform.scale(lightsaber_image, (TILE, TILE))

# Load the agent image
agent_image = pygame.image.load('./images/agent.png')
agent_image = pygame.transform.scale(agent_image, (TILE, TILE))

# Create an instance of GUI
gui = GUI(DISPLAY, maze_display, TILE, agent_image)

def draw_agent(surface, cell, color=(0, 0, 255), radius=TILE//4):
    x, y = cell.x * TILE + TILE // 2, cell.y * TILE + TILE // 2
    pygame.draw.circle(surface, color, (x, y), radius)
    
def draw_button(surface, position, size, color):
    pygame.draw.rect(surface, color, (*position, *size))
    surface.blit(button_image, (position[0] + size[0] // 2 - button_image.get_width() // 2, position[1] + size[1] // 2 - button_image.get_height() // 2))



"""def reset_maze():
    global grid_cells, mazeMatrix, maze_complete
    maze_complete = True
    grid_cells = generate_maze()  # Generate a new maze
    mazeMatrix = [[0] * cols for _ in range(rows)]  # Reset the maze matrix
"""
    
def draw_start_and_goal(maze_display):
    start_cell.walls['left'] = False
    goal_cell.walls['right'] = False
    # Adjusted coordinates for the start arrow to point to the left
    start_arrow = [(start_cell.x * TILE, start_cell.y * TILE),
                   (start_cell.x * TILE + arrow_size, start_cell.y * TILE + TILE // 2),
                   (start_cell.x * TILE, start_cell.y * TILE + TILE)]
    goal_arrow = [(goal_cell.x * TILE + TILE - arrow_size, goal_cell.y * TILE),
                  (goal_cell.x * TILE + TILE, goal_cell.y * TILE + TILE // 2),
                  (goal_cell.x * TILE + TILE - arrow_size, goal_cell.y * TILE + TILE)]
    # Marking the start and goal cell
    pygame.draw.polygon(maze_display, pygame.Color('white'), start_arrow)
    pygame.draw.polygon(maze_display, pygame.Color('white'), goal_arrow)

training_started = False
training_completed = False
training_episodes = 100
optimal_path = []

def train_agent_in_thread(agent, episodes, completion_event):
    global training_started, training_completed
    with thread_lock:  # Acquire the lock
        training_started = True
    print("In thread")
    # Call the train method of the agent
    agent.train(episodes)
    print(agent.q_table)
    with thread_lock:  # Release the lock
        training_completed = True
        training_started = False
    #optimal_path = agent.follow_optimal_path()
    completion_event.set()
    
while True:
    DISPLAY.blit(bg, (0, 0))
    maze_display.fill(pygame.Color('black'))
    mouse_click = False
    
    

    # Event handling loop
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit()
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            mouse_pos = pygame.mouse.get_pos()
            if button_rect.collidepoint(mouse_pos) and not training_started:
                # Start training in a separate thread
                training_started = True
    
    #new part
    if training_thread and training_completed_event.is_set():
        # Block until training thread finishes
        training_thread.join()
        # Reset the flag
        training_started = False
        training_thread = None  # Reset the thread variable
        # Reset the event for future use
        training_completed_event.clear()

    if not maze_complete:
        # Dynamic elements
        current_cell.visited = True
        next_cell = current_cell.check_neighbors(grid_cells)
        
        if next_cell:
            next_cell.visited = True
            stack.append(current_cell)
            remove_walls(current_cell, next_cell)
            current_cell = next_cell
        elif stack:
            current_cell = stack.pop()
            if current_cell == start_cell:
                maze_complete = True
                agent_present = True
                print("Maze generation complete!")
        # Draw the cells and update mazeMatrix
        for cell in grid_cells:
            cell.draw(maze_display)
            # Update the mazeMatrix to mark visited cells
            if cell.visited:
                mazeMatrix[cell.y][cell.x] = 1
        
        maze_display.blit(lightsaber_image, (current_cell.x * TILE, current_cell.y * TILE))

                
    else:
        
        for cell in grid_cells:
            cell.draw(maze_display)

        draw_start_and_goal(maze_display)
        
        button_color = button_hover_color if button_rect.collidepoint(pygame.mouse.get_pos()) else button_color
        draw_button(DISPLAY, button_position, button_size, button_color) 
        
        if training_started:
            print(mazeMatrix)
            # Start training in a separate thread
            print("Starting training...")
            training_thread = threading.Thread(target=train_agent_in_thread, args=(agent, training_episodes, training_completed_event))
            training_thread.start()
            training_started = False   
            
        elif training_completed:
            # The training has been completed, prepare for solving the maze
            #NULL IDE
            """agent_present = True
            agent_state = cols * start_cell.y + start_cell.x
            agent.maze.current_cell = start_cell
            agent_action = agent.act(agent_state)
            new_state, reward, done, _ = agent.maze.step(agent_action)
            agent.epsilon = 0 
            #agent.update(agent_state, agent_action, reward, new_state, done) #kommenterer ut for redundant

            agent_state = new_state"""
            
            training_completed = False
            #print(optimal_path)
            # The training has been completed, prepare for solving the maze
            
        
        if agent_present:
            # Get the agent's next action
            agent_action = agent.act(agent_state)
            new_state, reward, done, _ = agent.maze.step(agent_action)
            agent.update(agent_state, agent_action, reward, new_state, done)

            agent_state = new_state

            # Get agent's current position for GUI
            agent_cell_x, agent_cell_y = agent_state % cols, agent_state // cols

            # Update GUI with the current grid and agent position
            gui.update_gui(grid_cells, (agent_cell_x, agent_cell_y))

            pygame.time.delay(100) #adding delay on agent


            
    # Update the display with everything that was drawn
    DISPLAY.blit(maze_display, (maze_x, maze_y))
   

        
    pygame.display.flip()
    clock.tick(50)  # Speed to visualize the generation    
        
 