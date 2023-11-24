import React, { useState, useEffect } from 'react';
import './Maze.css';  // Import your CSS styles

type MazeProps = {
    width: number;
    height: number;
    mazeData: number[][]; // 2D array representing the maze, 1 for wall, 0 for path
};

const Maze: React.FC<MazeProps> = ({ width, height, mazeData }) => {
    const renderMaze = () => {
        return mazeData.map((row, rowIndex) => (
            <div key={rowIndex} className="maze-row">
                {row.map((cell, cellIndex) => (
                    <div
                        key={cellIndex}
                        className={`maze-cell ${cell === 1 ? 'wall' : 'path'}`}
                    />
                ))}
            </div>
        ));
    };

    return <div className="maze-container">{renderMaze()}</div>;
};

export default Maze;
