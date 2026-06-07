import {api} from './apiClient';

export const sendCommand = async (deviceId: string, action: string) => {
  try {
    const response = await api.post('/command', {
      device_id: deviceId,
      action,
    });
    return response.data;
  } catch (error) {
    console.error('Command failed:', error);
    throw error;
  }
};