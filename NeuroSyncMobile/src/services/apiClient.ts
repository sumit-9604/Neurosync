import axios from 'axios';

export const api = axios.create({
  baseURL: 'http://YOUR_PC_IP:8000',
  timeout: 10000,
});