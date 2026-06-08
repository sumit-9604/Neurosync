import {api} from './apiClient';

export const sendCommand = async (deviceId: string, action: string, args: object = {}) => {
  const response = await api.post(`/api/v1/devices/${deviceId}/command`, {
    action,
    ...args,
  });
  return response.data;
};