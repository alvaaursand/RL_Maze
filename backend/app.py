from mazeGenerator import *

pygame.init()
sc = pygame.display.set_mode(RES)
clock = pygame.time.Clock()

# Generate the initial maze grid
grid_cells = [Cell(col, row) for row in range(rows) for col in range(cols)]
current_cell = grid_cells[0]
start_cell = grid_cells[0]  # Start cell is at [0,0]
goal_cell = grid_cells[-1]   # Goal cell is at [cols-1, rows-1]
stack = []

# Initialize the mazeMatrix
mazeMatrix = [[0] * cols for _ in range(rows)]

while True:
    sc.fill(pygame.Color('darkslategray'))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit()

    # Draw the cells and update mazeMatrix
    for cell in grid_cells:
        cell.draw(sc)

        # Update the mazeMatrix to mark visited cells
        if cell.visited:
            mazeMatrix[cell.y][cell.x] = 1

    # Mark the start cell as green
    pygame.draw.rect(sc, pygame.Color('green'), (start_cell.x * TILE, start_cell.y * TILE, TILE, TILE))
    
    # Mark the goal cell as red
    pygame.draw.rect(sc, pygame.Color('red'), (goal_cell.x * TILE, goal_cell.y * TILE, TILE, TILE))

    current_cell.visited = True
    # Draw the current cell if you have a special way to mark it
    if hasattr(current_cell, 'draw_current_cell'):
        current_cell.draw_current_cell(sc)
    else:
        # Draw a circle at the current cell
        circle_center = (current_cell.x * TILE + TILE // 2, current_cell.y * TILE + TILE // 2)
        pygame.draw.circle(sc, pygame.Color('blue'), circle_center, TILE // 4)

    next_cell = current_cell.check_neighbors(grid_cells)
    if next_cell:
        next_cell.visited = True
        stack.append(current_cell)
        remove_walls(current_cell, next_cell)
        current_cell = next_cell
    elif stack:
        current_cell = stack.pop()

    pygame.display.flip()
    clock.tick(30)  # Slower speed to visualize the generation

