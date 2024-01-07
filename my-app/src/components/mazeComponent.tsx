import React from "react";

type Position = [number, number];

type MazeProps = {
  width: number;
  height: number;
  mazeData: number[][]; 
  start: Position; 
  goal: Position; 
};

const Maze: React.FC<MazeProps> = ({ width, height, mazeData, start, goal }) => {
  console.log(mazeData);
  const renderMaze = () => {
    return mazeData.map((row, rowIndex) => (
      <div key={rowIndex} className="flex">
        {row.map((cell, cellIndex) => {
          const isStart = rowIndex === start[0] && cellIndex === start[1];
          const isGoal = rowIndex === goal[0] && cellIndex === goal[1];
          const cellClass = `w-10 h-10 border ${isStart ? "bg-emerald" : isGoal ? "bg-yellow" : cell === 1 ? "bg-cyan" : "bg-green "}
          border border-gray-700 shadow-inner`;
          return (
            <div
              key={cellIndex}
              className={cellClass}
              style={{ width: 'calc(100% / width)', height: 'calc(100% / height)' }}
              role="gridcell"
              aria-label={isStart ? 'Start' : isGoal ? 'Goal' : 'Cell'}
            ></div>
          );
        })}
      </div>
    ));
  };

  return (
    <div className="flex flex-col border-8 border-green-900 justify-center items-center"
    >
      {renderMaze()}
    </div>
  );
};

export default Maze;
