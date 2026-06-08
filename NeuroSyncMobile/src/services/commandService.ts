import {api} from './apiClient';

export const sendCommand = async (deviceId: string, action: string, args: object = {}) => {
  const response = await api.post('/api/v1/command', {
    device_id: deviceId,
    action,
    payload: args,
  });
  return response.data;
};