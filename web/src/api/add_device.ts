import axios from "axios";
import type { AxiosResponse } from "axios";

interface AddDeviceResponse {
  message: string;
  status: boolean;
}

interface AddDeviceRequest {
    host: string;
    name: string;
}

export const addDevice = async (url: string, data: AddDeviceRequest): Promise<AddDeviceResponse> => {
    try {
        const response: AxiosResponse = await axios.post(url, data);
        return {
            message: response.data.message,
            status: response.data.status,
        };
    } catch (error) {
        console.log('error :', error);
        return {
            message: '',
            status: false,
        };
    }
}