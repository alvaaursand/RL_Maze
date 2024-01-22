from mazeGenerator import *

LARGE_RES = LARGER_WIDTH, LARGER_HEIGHT = 1402, 1102

pygame.init()
DISPLAY = pygame.display.set_mode(LARGE_RES)
pygame.display.set_caption("Dynamic Maze")
bg = pygame.image.load('images/bg.jpg').convert()
bg = pygame.transform.scale(bg, LARGE_RES)

clock = pygame.time.Clock()

# Generate the initial maze grid
grid_cells = [Cell(col, row) for row in range(rows) for col in range(cols)]
current_cell = grid_cells[0]
start_cell = grid_cells[0]  # Start cell is at [0,0]
goal_cell = grid_cells[-1]   # Goal cell is at [cols-1, rows-1]
stack = []

# Initialize the mazeMatrix
mazeMatrix = [[0] * cols for _ in range(rows)]

# Define button properties
button_color = pygame.Color('#455945')  # Button color
button_hover_color = pygame.Color('white')  # Button color when hovered over
button_position = (LARGER_WIDTH - 230, 144)  # Adjust as needed
button_size = (47, 47)  # Width, Height

button_rect = pygame.Rect(*button_position, *button_size)
button_image = pygame.image.load('./images/refresh.png')  # Load the button image
button_image = pygame.transform.scale(button_image, (37, 37))


# Load the lightsaber image
lightsaber_image = pygame.image.load('./images/lightsaber.png')
lightsaber_image = pygame.transform.scale(lightsaber_image, (TILE, TILE))
lightsaber_visible = False

maze_complete = False  # Flag to track if the maze is complete

def draw_button(surface, position, size, color):
    pygame.draw.rect(surface, color, (*position, *size))
    surface.blit(button_image, (position[0] + size[0] // 2 - button_image.get_width() // 2, position[1] + size[1] // 2 - button_image.get_height() // 2))

def reset_maze():
    global grid_cells, start_cell, goal_cell, mazeMatrix, maze_complete, lightsaber_visible
    grid_cells = generate_maze()  # Generate a new maze
    start_cell = grid_cells[0]    # Reset start cell
    goal_cell = grid_cells[-1]    # Reset goal cell
    mazeMatrix = [[0] * cols for _ in range(rows)]  # Reset the maze matrix
    maze_complete = False  # Reset the maze completion flag
    lightsaber_visible = False  # Make the lightsaber invisible

while True:
    DISPLAY.blit(bg, (0, 0))
    maze_display = pygame.Surface(RES)
    maze_display.fill(pygame.Color('black'))

    mouse_click = False

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit()
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                mouse_click = True
                mouse_pos = pygame.mouse.get_pos()
                if button_rect.collidepoint(mouse_pos):
                    reset_maze()  # Reset and generate a new maze
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit()

    # Draw the cells and update mazeMatrix
    for cell in grid_cells:
        cell.draw(maze_display)

        # Update the mazeMatrix to mark visited cells
        if cell.visited:
            mazeMatrix[cell.y][cell.x] = 1

    # Draw right arrows
    arrow_size = TILE // 3
    # Adjusted coordinates for the start arrow to point to the left
    start_arrow = [(start_cell.x * TILE, start_cell.y * TILE),
                (start_cell.x * TILE + arrow_size, start_cell.y * TILE + TILE // 2),
                (start_cell.x * TILE , start_cell.y * TILE + TILE)]
    goal_arrow = [(goal_cell.x * TILE + TILE - arrow_size, goal_cell.y * TILE),
                (goal_cell.x * TILE + TILE, goal_cell.y * TILE + TILE // 2),
                (goal_cell.x * TILE + TILE - arrow_size, goal_cell.y * TILE + TILE)]

    # Marking the start and goal cell
    pygame.draw.polygon(maze_display, pygame.Color('white'), start_arrow)
    pygame.draw.polygon(maze_display, pygame.Color('white'), goal_arrow)

    current_cell.visited = True

    if not maze_complete and current_cell != start_cell:  # Check if maze generation is still in progress and not at the start cell
        # Draw the lightsaber image at the current cell's position
        maze_display.blit(lightsaber_image, (current_cell.x * TILE, current_cell.y * TILE))
        lightsaber_visible = True  # Lightsaber is now visible
    else:
        lightsaber_visible = False  # Lightsaber is in its original position or maze generation is complete, make it invisible

    next_cell = current_cell.check_neighbors(grid_cells)
    if next_cell:
        next_cell.visited = True
        stack.append(current_cell)
        remove_walls(current_cell, next_cell)
        current_cell = next_cell
    elif stack:
        current_cell = stack.pop()

    maze_x = (LARGER_WIDTH - WIDTH) // 2
    maze_y = (LARGER_HEIGHT - HEIGHT) // 2
    DISPLAY.blit(maze_display, (maze_x, maze_y))

    if button_rect.collidepoint(pygame.mouse.get_pos()):
        button_current_color = button_hover_color
    else:
        button_current_color = button_color
    
    # Draw the button
    draw_button(DISPLAY, button_position , button_size, button_color)

    pygame.display.flip()
    clock.tick(30)# Speed to visualize the generation
