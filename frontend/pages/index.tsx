import { useEffect, useState } from 'react';
import { fetchData } from '../api';

const Home = () => {
  const [data, setData] = useState<any>(null);

  useEffect(() => {
    fetchData()
      .then((response) => setData(response.data))
      .catch((error) => console.error('Error:', error));
  }, []);

  return (
    <div>
      <h1>Data from Flask API:</h1>
      <pre>{JSON.stringify(data, null, 2)}</pre>
    </div>
  );
};

export default Home;