import axios from 'axios';
import {tokenKeyName} from "../constants/constants.ts";

const baseURL = import.meta.env.VITE_REST_API_URL || 'http://localhost:5000/api';
//const baseURL = "http://localhost:5000/api"; // FONTOS!
  


const axiosInstance = axios.create({
    baseURL,
    headers: {
        'Content-Type': 'application/json',
    },
});



axiosInstance.interceptors.request.use(
    config => {
        const token = localStorage.getItem(tokenKeyName);
        if (token) {
            config.headers['Authorization'] = `Bearer ${token}`;
        }
        return config;
    },
    error => {
        return Promise.reject(error);
    }
);

axiosInstance.interceptors.response.use(
    response => {
        return response;
    },
    error => {
        if (error.response.status === 401) {
            console.error('Unauthorized access - redirecting to login');
            localStorage.clear();
            window.location.href = '/';
        } else if(error.response.status == 400) {
            console.error('Bad request - use http instead of https:', error.response.data);
        } else {
            if (!error.response) {
                console.error('Network error - could not connect to API:', error.message);
            }
        }
        return Promise.reject(error);
    }
);

export default axiosInstance;