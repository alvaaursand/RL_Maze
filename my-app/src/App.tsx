import './App.css';
import Maze from './components/mazeComponent';
import React, { useEffect, useState } from 'react';


const App: React.FC = () => {
  const [mazeData, setMazeData] = useState<number[][] | null>(null);
  
  useEffect(() => {
    const fetchMazeData = async () => {
      try {
        const response = await fetch('http://127.0.0.1:5000/api/maze');
        const data = await response.json();
        setMazeData(data.maze);
      } catch (error) {
        console.error('Failed to fetch maze data:', error);
      }
    };
    const intervalId = setInterval(() => {
      fetchMazeData();
    }, 5000); // fetch new maze every 5 seconds
  
    return () => clearInterval(intervalId); // clear interval on component unmount

    
  }, []);

  // Render a loading state until the data is fetched
  if (!mazeData) {
    return <div>Loading maze...</div>;
  }

  return (
    <div className="App">
      <header className="App-header">
        <h1>The dynamic maze</h1>
        <Maze width={10} height={10} mazeData={mazeData} />
      </header>
    </div>
  );
};

export default App;








