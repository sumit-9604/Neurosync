import {api} from './apiClient';

export const loginUser = async (email: string, password: string) => {
  const response = await api.post('/api/v1/login', {email, password});
  return response.data;
};

export const registerUser = async (email: string, password: string) => {
  const response = await api.post('/api/v1/register', {email, password});
  return response.data;
};