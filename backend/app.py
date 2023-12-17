from flask import Flask, jsonify
from flask_cors import CORS  
import numpy as np
from dynamicMaze import generate_dynamic_maze

app = Flask(__name__)
CORS(app)  # This will enable CORS for all routes

@app.route('/api/maze', methods=['GET'])
def get_maze():
    # Your maze generation logic here...
    # Convert numpy array to list for JSON serialization
    maze = generate_dynamic_maze()
    maze_data = maze.tolist()
    return jsonify({'maze': maze_data})

if __name__ == '__main__':
    app.run(debug=True)
