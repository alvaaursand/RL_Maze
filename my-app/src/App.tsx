import React from 'react';
import './App.css';
import Maze from './components/mazeComponent';


function App() {
  const mazeData = [
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
}
export default App;







