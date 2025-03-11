import axios from 'axios';
import type { AxiosResponse } from 'axios';

interface GetDeviceResponse {
  message: { host: string, name: string }[];
  status: boolean;
}

export const getDevice = async (url: string): Promise<GetDeviceResponse> => {
  try {
    const response: AxiosResponse = await axios.get(url);
    return {
      message: response.data.message,
      status: response.data.status,
    };
  } catch (error) {
    console.log('error :', error);
    return {
      message: [],
      status: false,
    };
  }
}