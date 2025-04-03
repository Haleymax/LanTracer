import axios from 'axios';
import type { AxiosResponse } from 'axios';

interface GetDeviceResponse {
  message: { host: string, name: string }[];
  status: boolean;
}

interface GetMemoryRequest {
  status: boolean;
  data: any[];
  message: string;
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


export const getDeviceMemory = async (url: string, host: string, days: string): Promise<GetMemoryRequest> => {
  try {
    const data = {
      host: host,
      days: days
    }
    const response: AxiosResponse = await axios.post(url, data);
    return {
      message: response.data.message,
      status: response.data.status,
      data: response.data.data,
    };
  } catch (error) {
    console.log('error :', error);
    return {
      message: '',
      status: false,
      data: [],
    };
  }
}