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
          className={`w-10 h-10 border ${
            cell === 1 ? "bg-red-300" : "bg-green-700"
          }`}
          ></div>
          ))}
      </div>
    ));
  };
  console.log("mazeData", mazeData);  

  return (
    <div className="flex flex-col border-8 border-green-900">
      {renderMaze()}
    </div>
  );
};

export default Maze;
