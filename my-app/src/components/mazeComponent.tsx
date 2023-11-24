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
        <p>"hei"</p>
        {row.map((cell, cellIndex) => (
          <div
            
            key={cellIndex}
            className={`w-5 h-5 border ${
              cell === 1 ? "bg-red-200" : "bg-gray-800"
            }`}
          >
             <p>"hallo"</p>
            </div>
        ))}
      </div>
      
    ));
  };

  return (
    <div className="flex flex-col border-2 border-green-500">{renderMaze()}</div>
  );
};

export default Maze;
