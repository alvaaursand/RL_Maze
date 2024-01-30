from agent import CuriosityAgent
from mazeGenerator import *
from movement import *
import threading
#get the window size of this computer

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

agent = CuriosityAgent(cols * rows, 4, Move(grid_cells, cols, rows, start_cell, goal_cell))
agent_state = cols * start_cell.y + start_cell.x

# Define button properties
button_color = pygame.Color('#455945')  # Button color
button_hover_color = pygame.Color('white')  # Button color when hovered over
button_position = (LARGER_WIDTH - 202, 90)  # Adjust as needed
button_size = (42, 42)  # Width, Height
button_rect = pygame.Rect(*button_position, *button_size)
button_image = pygame.image.load('./images/refresh.png')  # Load the button image
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

def draw_agent(surface, cell, color=(0, 0, 255), radius=TILE//4):
    x, y = cell.x * TILE + TILE // 2, cell.y * TILE + TILE // 2
    pygame.draw.circle(surface, color, (x, y), radius)
    
def draw_button(surface, position, size, color):
    pygame.draw.rect(surface, color, (*position, *size))
    surface.blit(button_image, (position[0] + size[0] // 2 - button_image.get_width() // 2, position[1] + size[1] // 2 - button_image.get_height() // 2))

def reset_maze():
    global grid_cells, mazeMatrix, maze_complete
    maze_complete = True
    grid_cells = generate_maze()  # Generate a new maze
    mazeMatrix = [[0] * cols for _ in range(rows)]  # Reset the maze matrix

    
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

training_progress = ""
training_started = False
training_completed = False
training_episodes = 20

def train_agent_in_thread(agent, episodes):
    global training_started, training_completed, training_progress
    training_started = True
    print("In thread")
    # Call the train method of the agent
    agent.train(episodes)

    print("Training completed.")
    training_completed = True
    training_started = False
    
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
            if button_rect.collidepoint(mouse_pos):
                if button_rect.collidepoint(mouse_pos) and not training_started:
                    # Start training in a separate thread
                    training_started = True
                    
                elif training_completed:
                    # The training has been completed, prepare for solving the maze
                    print("Training completed!")
                    """agent_present = True
                    agent_state = cols * start_cell.y + start_cell.x
                    agent.maze.current_cell = start_cell"""
    
    draw_start_and_goal(maze_display)
    if maze_complete:
        for cell in grid_cells:
            cell.draw(maze_display)
        if training_started:
            # Start training in a separate thread
            #training_started = True
            print("Starting training...")
            training_thread = threading.Thread(target=train_agent_in_thread, args=(agent, training_episodes))
            training_thread.start()
            training_started = False   
            print("Training finished") 
    
        
    else:
        # The rest of the game loop when not training
        # Draw the maze and handle game logic
        if not maze_complete:
            # Maze generation logic here
            maze_display.blit(lightsaber_image, (current_cell.x * TILE, current_cell.y * TILE))
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
                    print("Maze generation complete!")
            # Draw the cells and update mazeMatrix
            for cell in grid_cells:
                cell.draw(maze_display)
                # Update the mazeMatrix to mark visited cells
                if cell.visited:
                    mazeMatrix[cell.y][cell.x] = 1    

        if agent_present:
            # Get the agent's next action
            agent_action = agent.act(agent_state)
            new_state, reward, done, _ = agent.maze.step(agent_action)
            agent.update(agent_state, agent_action, reward, new_state, done)

            agent_state = new_state

            # Update agent's position for rendering
            agent_cell_x = agent_state % cols
            agent_cell_y = agent_state // cols
            agent_x, agent_y = agent_cell_x * TILE, agent_cell_y * TILE
            maze_display.blit(agent_image, (agent_x, agent_y))

            if done:  # The agent has reached the goal
                print("Agent has reached the goal!")
                agent_present = False  # Stop the agent's movement
                # Perform any additional actions needed when the goal is reached
        
        # Other game logic and drawing functions
    
        
                

        """if training_completed and not agent_present:
            reset_maze()"""
            

        # Update the display with everything that was drawn
    DISPLAY.blit(maze_display, (maze_x, maze_y))
    draw_button(DISPLAY, button_position, button_size, button_color)
        
    pygame.display.flip()
    clock.tick(30)  # Speed to visualize the generation    
        
 