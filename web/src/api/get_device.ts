import axios from 'axios';
import type { AxiosResponse } from 'axios';

interface GetDeviceResponse {
  device: unknown;
  status: boolean;
}

export const getDevice = async (url: string): Promise<GetDeviceResponse> => {
  try {
    const response: AxiosResponse = await axios.get(url);
    console.log('data :', response.data);
    return {
      device: response.data,
      status: true,
    };
  } catch (error) {
    console.log('error :', error);
    return {
      device: null,
      status: false,
    };
  }
}
