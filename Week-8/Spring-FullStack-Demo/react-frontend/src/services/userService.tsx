import { getToken } from './authService';

const BASE_URL = 'http://localhost:8080/users';

export const getAllUsers = async (): Promise<any[]> => {
  const res = await fetch(BASE_URL, {
    headers: { Authorization: `Bearer ${getToken()}` }
  });
  if (!res.ok) throw new Error('Failed to fetch users');
  return res.json();
};