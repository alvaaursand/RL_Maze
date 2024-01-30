import logging
import numpy as np
from movement import Move
from mazeGenerator import *

target_update_frequency = 100 

class CuriosityAgent:
    def __init__(self, state_size, action_size, maze, gamma=0.99, learning_rate=0.01):
        self.state_size = state_size
        self.action_size = action_size
        self.q_table = np.zeros((state_size, action_size)) 
        self.gamma = gamma
        self.epsilon = 1.0  
        self.epsilon_decay = 0.995
        self.min_epsilon = 0.01
        self.learning_rate = learning_rate
        self.maze = Move(maze.grid_cells, maze.cols, maze.rows, maze.start_cell, maze.goal_cell)

        self.grid_width = maze.cols
        self.grid_height = maze.rows
        # Initialize a logger
        self.logger = logging.getLogger("CuriosityAgent")
        self.logger.setLevel(logging.INFO)
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        ch = logging.StreamHandler()
        ch.setFormatter(formatter)
        self.logger.addHandler(ch)

     
    """def act(self, state):
        #explore within the valid choices

        if np.random.rand() < self.epsilon:
            return np.random.choice(self.action_size)  
        else:
            return np.argmax(self.q_table[state, :])  
        """
    def state_to_coordinates(self, state):
        return state % self.maze.cols, state // self.maze.cols

    def act(self, state):
    # Calculate the valid actions from the current state
        valid_actions = self.get_valid_actions(state)

    # If there are no valid actions, return None or handle it as needed
        if not valid_actions:
            return None

    # Exploration vs exploitation
        if np.random.rand() < self.epsilon:
            # Choose a random action from the valid actions
            return np.random.choice(valid_actions)
        else:
            # Choose the best action based on Q-values, considering only valid actions
            q_values = {action: self.q_table[state, action] for action in valid_actions}
            return max(q_values, key=q_values.get)

    def get_valid_actions(self, state):
        x, y = self.state_to_coordinates(state)
        
        valid_actions = []
        # Check if the agent can move up, right, down, or left
        if self.is_valid_move(x, y - 1):  # Move up
            valid_actions.append(0)  # Append the action index for 'up'
        if self.is_valid_move(x + 1, y):  # Move right
            valid_actions.append(1)  # Append the action index for 'right'
        if self.is_valid_move(x, y + 1):  # Move down
            valid_actions.append(2)  # Append the action index for 'down'
        if self.is_valid_move(x - 1, y):  # Move left
            valid_actions.append(3)  # Append the action index for 'left'

        return valid_actions


    # Example implementation of is_valid_move
    def is_valid_move(self, x, y):
        # Check if the cell is within grid bounds
        if 0 <= x < self.grid_width and 0 <= y < self.grid_height:
            # Check if the cell is not surrounded by walls
            cell = self.maze.grid_cells[y * self.grid_width + x]  # Adjust indexing if necessary
            return not (cell.walls['top'] and cell.walls['right'] and cell.walls['bottom'] and cell.walls['left'])
        return False



    def update(self, state, action, reward, next_state, done):
        dx, dy = 0, 0
        if action == 0:  
            dy = -1
        elif action == 1:  
            dx = 1
        elif action == 2:  
            dy = 1
        elif action == 3:  
            dx = -1

        new_x, new_y = state % self.maze.cols + dx, state // self.maze.cols + dy

        if (new_x, new_y) == self.maze.goal_position:
            reward = 1
        elif (new_x, new_y) == (state % self.maze.cols, state // self.maze.cols):
            reward = -0.5  
        else:
            reward = 1

        q_value = self.q_table[state, action]
        next_q_values = self.q_table[next_state, :]
        target_q_value = reward + self.gamma * np.max(next_q_values) * (1 - done)
        td_error = target_q_value - q_value
        self.q_table[state, action] = q_value + self.learning_rate * td_error
        self.epsilon = max(self.min_epsilon, self.epsilon * self.epsilon_decay)


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


    
    def train(self, episodes):
        for episode in range(episodes):
            state = self.maze.reset()
            total_reward = 0
            done = False
            num_steps = 0
            print(f"Starting Episode {episode + 1}")

            while not done:
                print(f"  Inside loop, State: {state}")

                action = self.act(state)
                next_state, reward, done, _ = self.maze.step(action)
                print(f"  Action: {action}, Next State: {next_state}, Reward: {reward}, Done: {done}")

                self.update(state, action, reward, next_state, done)
                state = next_state
                total_reward += reward
                num_steps += 1
                done = True

            print(f"Episode {episode + 1}: Total Reward = {total_reward}, Steps = {num_steps}, Goal Reached = {done}")

            self.epsilon = max(self.min_epsilon, self.epsilon * self.epsilon_decay)

        print("Training complete.")

        

    def evaluate(self, episodes):
        total_rewards = []
        for _ in range(episodes):
            state = self.maze.reset()
            done = False
            total_reward = 0
            

            while not done:
                action = self.act(state)
                next_state, reward, done = self.maze.step(action)
                total_reward += reward
                state = next_state

            total_rewards.append(total_reward)

        average_reward = np.mean(total_rewards)
        print("Average reward over {episodes} evaluation episodes: {average_reward}")
        return average_reward