import axios from 'axios';
import type { Blockchain, Report, User } from '../types';

const API_BASE_URL = 'http://localhost:8000';

// Create axios instance
export const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// API endpoints
export const blockchainAPI = {
  getBlockchain: async (): Promise<Blockchain> => {
    const response = await api.get('/blockchain');
    return response.data;
  },
};

export const reportsAPI = {
  submitReport: async (reportData: Partial<Report>): Promise<Report> => {
    const response = await api.post('/reports', reportData);
    return response.data;
  },
  
  getAllReports: async (): Promise<Report[]> => {
    const response = await api.get('/reports');
    return response.data;
  },
};

export const authAPI = {
  login: async (office_name: string, password: string): Promise<User> => {
    const response = await api.post('/login', { office_name, password });
    return response.data;
  },
  
  register: async (office_name: string, password: string): Promise<User> => {
    const response = await api.post('/register', { office_name, password });
    return response.data;
  },
};

export default api;
