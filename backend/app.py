from flask import Flask, jsonify
from flask_cors import CORS  
import numpy as np
from dynamicMaze import generate_dynamic_maze

app = Flask(__name__)
cors = CORS(app, resources={r"/api/*": {"origins": "http://localhost:3000"}})

@app.route('/api/maze', methods=['GET'])
def get_maze():
   try:
        maze, start, goal = generate_dynamic_maze()
        
        if isinstance(maze, np.ndarray):
            maze = maze.tolist()
            
        maze_data = {
            "maze": maze, 
            "start": start,
            "goal": goal
        }
        return jsonify(maze_data)
   except Exception as e:
            print(e)
            return jsonify({"error": "There was an error generating the maze"}), 500

if __name__ == '__main__':
    app.run(debug=True)
