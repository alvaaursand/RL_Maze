# dynamicMaze.py
import numpy as np
import random
from queue import Queue

def is_solvable(maze, start, goal):
    directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]
    visited = set()
    queue = Queue()
    queue.put(start)
    visited.add(start)

    while not queue.empty():
        x, y = queue.get()
        if (x, y) == goal:
            return True
        for dx, dy in directions:
            nx, ny = x + dx, y + dy
            if 0 <= nx < maze.shape[0] and 0 <= ny < maze.shape[1] and maze[nx, ny] == 0 and (nx, ny) not in visited:
                queue.put((nx, ny))
                visited.add((nx, ny))
    return False

def update_maze(maze, agent_pos, goal_pos):
    maze_width, maze_height = maze.shape
    for _ in range(random.randint(1, 5)):
        x, y = random.randint(0, maze_width - 1), random.randint(0, maze_height - 1)

        if (x, y) != agent_pos and (x, y) != goal_pos:
            maze[x, y] = 1 - maze[x, y]

        if not is_solvable(maze, agent_pos, goal_pos):
            maze[x, y] = 1 - maze[x, y]

    if maze[agent_pos] == 1:
        for dx, dy in [(1, 0), (0, 1), (-1, 0), (0, -1)]:
            nx, ny = agent_pos[0] + dx, agent_pos[1] + dy
            if 0 <= nx < maze_width and 0 <= ny < maze_height and maze[nx, ny] == 0:
                agent_pos = (nx, ny)
                break

    return maze, agent_pos

def generate_dynamic_maze(size=(10, 10), start=(0, 0), goal=(9, 9)):
    maze = np.zeros(size)
    agent_pos = start
    goal_pos = goal
    maze, agent_pos = update_maze(maze, agent_pos, goal_pos)
    print(maze)
    print(agent_pos)
    return maze


# This code will not run when imported, only when executed directly
if __name__ == '__main__':
    maze = generate_dynamic_maze()
    print(maze)
