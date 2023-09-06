import axios, { AxiosResponse } from 'axios';

const api = axios.create({
  baseURL: 'http://localhost:5000', // Replace with your Flask API URL
});

// Example function to fetch data from your Flask API
export const fetchData = async (): Promise<AxiosResponse> => {
  try {
    const response = await api.get('/your-api-endpoint');
    return response;
  } catch (error) {
    console.error('Error fetching data:', error);
    throw error;
  }
};