import logging
import numpy as np
from maze import Maze

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
        
        self.maze = Maze(maze.grid_cells, maze.cols, maze.rows, maze.start_cell, maze.goal_cell)

        # Initialize a logger
        self.logger = logging.getLogger("CuriosityAgent")
        self.logger.setLevel(logging.INFO)
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        ch = logging.StreamHandler()
        ch.setFormatter(formatter)
        self.logger.addHandler(ch)

     
    def act(self, state):
        if np.random.rand() < self.epsilon:
            return np.random.choice(self.action_size)  
        else:
            return np.argmax(self.q_table[state, :])  
        

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

    episodes= 100
            
    def train(self, episodes):
        for _ in range(episodes):
            state = self.maze.reset()
            total_reward = 0
            done = False
            num_steps = 0
            state = self.maze.reset()


            while not done:
                action = self.act(state)
                next_state, reward, done, _ = self.maze.step(action)
                self.update(state, action, reward, next_state, done)

                state = next_state
                total_reward += reward
                num_steps += 1

            self.logger.info("Episode {episode + 1}: Total Reward = {total_reward}, Steps = {num_steps}, Goal Reached = {done}")

            self.epsilon = max(self.min_epsilon, self.epsilon * self.epsilon_decay)


        self.logger.info("Training complete.")

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
        self.logger.info("Average reward over {episodes} evaluation episodes: {average_reward}")
        return average_reward