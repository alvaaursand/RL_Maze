import './App.css';
import Maze from './components/mazeComponent';
import React, { useEffect, useState } from 'react';


type Position = [number, number];
type MazeData = {
  maze: number[][];
  start: Position;
  goal: Position;
};

const App: React.FC = () => {
  const [mazeData, setMazeData] = useState<MazeData | null>(null);
  const [isLoading, setIsLoading] = useState(true); // state to track loading status
  const [error, setError] = useState<string | null>(null); // state to track any fetching errors

  useEffect(() => {
    const fetchMazeData = async () => {
      setIsLoading(true); 
      setError(null); 
      try {
        const response = await fetch('http://127.0.0.1:5000/api/maze');
        if (!response.ok) {
          throw new Error(`HTTP error! status: ${response.status}`);
        }
        const data = await response.json();
        setMazeData({
          maze: data.maze,
          start: data.start, 
          goal: data.goal, 
        });
      } catch (error) {
        setError('Failed to fetch maze data'); 
        console.error('Failed to fetch maze data:', error);
      } finally {
        setIsLoading(false); 
      }
    };
    let debounceTimer: NodeJS.Timeout;


    const debouncedFetchMazeData = () => {
      clearTimeout(debounceTimer);
      debounceTimer = setTimeout(() => {
        fetchMazeData();
      }, 5000);
    };

    fetchMazeData();

    const intervalId = setInterval(debouncedFetchMazeData, 5000);

    return () => {
      clearInterval(intervalId);
      if (debounceTimer) clearTimeout(debounceTimer);
    };
  }, []);

  if (error) {
    return <div>Error: {error}</div>;
  }

  if (isLoading) {
    return <div>Loading maze...</div>;
  }

  if (mazeData) {
    return (
      <div className="App">
          <h1 className="App-header">The dynamic maze</h1>
        <div className="flex justify-center m-8 p-4 ">
          <Maze
            width={10}
            height={20}
            mazeData={mazeData.maze}
            start={mazeData.start}
            goal={mazeData.goal}
          />
        </div>
      </div>
    );
  }

  return <div>Failed to load the maze.</div>;
};

export default App;
