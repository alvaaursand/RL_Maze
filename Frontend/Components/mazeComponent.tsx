import React from "react";

type MazeProps = {
  width: number;
  height: number;
  mazeData: number[][]; // 2D array representing the maze, 1 for wall, 0 for path
};

const Maze: React.FC<MazeProps> = ({ width, height, mazeData }) => {
  const renderMaze = () => {
    return mazeData.map((row, rowIndex) => (
      <div key={rowIndex} className="flex">
        {row.map((cell, cellIndex) => (
          <div
            key={cellIndex}
            className={`w-5 h-5 border ${
              cell === 1 ? "bg-gray-800" : "bg-gray-200"
            }`}
          />
        ))}
      </div>
    ));
  };

  return (
    <div className="flex flex-col border-2 border-gray-800">{renderMaze()}</div>
  );
};

export default Maze;
