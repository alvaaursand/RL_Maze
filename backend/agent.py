import logging
import numpy as np
from maze import Maze
from grid import *

        
class CuriosityAgent:
    def __init__(self, state_size, action_size, maze, gamma=0.99, learning_rate=0.01):
        self.state_size = state_size
        self.action_size = action_size
        self.q_table = np.zeros((state_size, action_size)) 
        self.gamma = gamma
        self.epsilon = 1  
        self.epsilon_decay = 0.995
        self.min_epsilon = 0.01
        self.learning_rate = learning_rate
        self.maze = Maze(maze.grid_cells, maze.cols, maze.rows, maze.start_cell, maze.goal_cell)

        self.grid_width = maze.cols
        self.grid_height = maze.rows
        # Initialize a logger
        self.logger = logging.getLogger("CuriosityAgent")
        self.logger.setLevel(logging.INFO)
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        ch = logging.StreamHandler()
        ch.setFormatter(formatter)
        self.logger.addHandler(ch)

     
    def state_to_coordinates(self, state):
        return state % self.maze.cols, state // self.maze.cols
    
    def calculate_distance_to_goal(self, x, y):
        goal_x, goal_y = self.maze.goal_position
        return abs(x - goal_x) + abs(y - goal_y)


    def act(self, state):
        # Calculate the valid actions from the current state
        valid_actions = self.get_valid_actions(state)

        # If there are no valid actions, return None or handle it as needed
        if not valid_actions:
            return None

        # Get unvisited and visited legal moves
        unvisited_moves = []
        visited_moves = []
        for action in valid_actions:
            new_x, new_y = self.calculate_new_position(state, action)
            if not self.maze.grid_cells[new_y * self.grid_width + new_x].visited:
                unvisited_moves.append(action)
            else:
                visited_moves.append(action)
                
        # Exploration vs exploitation with a preference for unvisited cells
        if np.random.rand() < self.epsilon:
            # If there are unvisited moves, choose randomly among them, otherwise choose any valid move
            return np.random.choice(unvisited_moves) if unvisited_moves else np.random.choice(valid_actions)
        else:
            # Choose the best action based on Q-values, with a preference for unvisited moves
            q_values = {action: self.q_table[state, action] for action in unvisited_moves} or \
                       {action: self.q_table[state, action] for action in valid_actions}
            return max(q_values, key=q_values.get)
    
    def calculate_new_position(self, state, action):
        # Translate action into new x and y coordinates
        x, y = self.state_to_coordinates(state)
        if action == 0:  # Move up
            y -= 1
        elif action == 1:  # Move right
            x += 1
        elif action == 2:  # Move down
            y += 1
        elif action == 3:  # Move left
            x -= 1
        return x, y 
    
    def get_valid_actions(self, state):
        x, y = self.state_to_coordinates(state)
        current_cell = self.maze.grid_cells[state]
        
        valid_actions = []
        # Use the legal_moves of the current cell to determine valid actions
        if 'up' in current_cell.legal_moves:  # Move up
            valid_actions.append(0)  # Append the action index for 'up'
        if 'right' in current_cell.legal_moves:  # Move right
            valid_actions.append(1)  # Append the action index for 'right'
        if 'down' in current_cell.legal_moves:  # Move down
            valid_actions.append(2)  # Append the action index for 'down'
        if 'left' in current_cell.legal_moves:  # Move left
            valid_actions.append(3)  # Append the action index for 'left'
        
        return valid_actions


    def update(self, state, action, reward, next_state, done):
        # Calculate the new coordinates based on the current state and action
        current_x, current_y = self.state_to_coordinates(state)
        next_x, next_y = self.state_to_coordinates(next_state)


        new_x, new_y = self.calculate_new_position(state, action)
        valid_actions = self.get_valid_actions(state)

        current_distance = self.calculate_distance_to_goal(current_x, current_y)
        next_distance = self.calculate_distance_to_goal(next_x, next_y)
        if next_distance < current_distance:
            reward += 0.2
        
        if not valid_actions:
            reward = -1  # Penalize the agent for getting stuck
        # Determine reward based on whether the goal is reached
        else: 
            if (new_x, new_y) == self.maze.goal_position:
                reward = 3  # Reward for reaching the goal
            elif self.maze.grid_cells[new_y * self.grid_width + new_x].visited:
                reward = -0.2  # Small negative reward for visiting a cell that has already been visited
            else:
                reward = -0.1  # Small negative reward for each step to encourage efficiency

        # Update the Q-table with the new state information
        q_value = self.q_table[state, action]
        next_q_values = self.q_table[next_state, :]
        target_q_value = reward + self.gamma * np.max(next_q_values) * (1 - done)
        td_error = target_q_value - q_value
        self.q_table[state, action] += self.learning_rate * td_error

        # Mark the cell as visited
        # Note: This should be the index in the grid, not the x, y coordinates
        self.maze.grid_cells[next_state].visited = True

    def move(self, action):
        if action == 0:  
            new_state = self.maze.move_up()
        elif action == 1:  
            new_state = self.maze.move_right()
        elif action == 2:  
            new_state = self.maze.move_down()
        elif action == 3:  
            new_state = self.maze.move_left()

        self.state = new_state
        return new_state 


    
    def train(self, episodes, max_steps_per_episode=5000): 
        for episode in range(episodes):
            state = self.maze.reset()
            #self.maze.current_cell = self.maze.start_cell  # Set agent to start position
            total_reward = 0
            done = False
            num_steps = 0
            print(f"Starting Episode {episode + 1}...")

            while not done and num_steps < max_steps_per_episode:
                action = self.act(state)
                next_state, reward, done, _ = self.maze.step(action)

                self.update(state, action, reward, next_state, done)
                state = next_state
                total_reward += reward
                num_steps += 1

                if done:  # Goal reached or episode terminated
                    print(f"Goal reached in {num_steps} steps or episode ended.")
                    break

            print(f"Episode {episode + 1}: Total Reward = {total_reward}, Steps = {num_steps}, Goal Reached = {done}")

            # Update Epsilon only here, after each episode
            self.epsilon = max(self.min_epsilon, self.epsilon * self.epsilon_decay)

            print(f"Epsilon updated to {self.epsilon}")

        print("Training complete.")


    def evaluate(self, state, episodes):
        total_rewards = []
        for _ in range(episodes):
            state = self.maze.reset()
            done = False
            total_reward = 0
            

            while not done:
                action = self.act(state, explore=False)
                next_state, reward, done = self.maze.step(action)
                total_reward += reward
                state = next_state

            total_rewards.append(total_reward)

        average_reward = np.mean(total_rewards)
        print("Average reward over {episodes} evaluation episodes: {average_reward}")
        return average_reward
    
    
    
    """ def follow_optimal_path(self):
        state = self.maze.start_cell.y * self.grid_width + self.maze.start_cell.x
        path = []
        
        while state != self.maze.goal_cell.y * self.grid_width + self.maze.goal_cell.x:
            # Update epsilon based on epsilon decay
            self.epsilon = max(self.min_epsilon, self.epsilon * self.epsilon_decay)

            # Get valid actions from the current state
            valid_actions = self.get_valid_actions(state)

            # Initialize a dictionary to store Q-values for valid actions
            q_values = {}

            for action in valid_actions:
                q_values[action] = self.q_table[state, action]

            # Choose the action with the Q-value closest to 0 (minimizing revisiting)
            action = min(q_values, key=lambda x: abs(q_values[x]))

            # Move to the next state based on the chosen action
            next_x, next_y = self.calculate_new_position(state, action)
            next_state = next_y * self.grid_width + next_x

            # Add the chosen action to the path
            path.append(action)

            # Update the current state
            state = next_state

        return path
"""