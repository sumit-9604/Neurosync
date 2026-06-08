import axios from 'axios';

export const api = axios.create({
  baseURL: 'https://neurosync-production-0f2b.up.railway.app',
  timeout: 10000,
});