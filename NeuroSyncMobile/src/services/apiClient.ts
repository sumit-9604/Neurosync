import axios from 'axios';

export const api = axios.create({
  baseURL: 'http://YOUR_BACKEND_URL:8000',
  timeout: 10000,
});