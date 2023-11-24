import React from "react";
import "./App.css";
import Maze from "./components/Maze";

const App: React.FC = () => {
  // Example maze data: 1 for wall, 0 for path
  const mazeData: number[][] = [
    [1, 1, 1, 1, 1],
    [1, 0, 0, 0, 1],
    [1, 0, 1, 0, 1],
    [1, 0, 1, 0, 0],
    [1, 1, 1, 1, 1],
  ];

  return (
    <div className="App">
      <header className="App-header">
        <Maze width={5} height={5} mazeData={mazeData} />
      </header>
    </div>
  );
};

export default App;
