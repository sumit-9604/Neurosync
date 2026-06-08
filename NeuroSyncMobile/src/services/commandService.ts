import {api} from './apiClient';

export const sendCommand = async (deviceId: string, action: string) => {
  const response = await api.post('/api/v1/command', {
    device_id: deviceId,
    action,
  });
  return response.data;
};