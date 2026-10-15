const BASE_URL = 'http://localhost:8080/auth';

export const login = async (username: string, password: string): Promise<string> => {
  const res = await fetch(`${BASE_URL}`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ username, password })
  });
  console.log('Status:', res.status);
  const body = await res.text();
  console.log('Body:', body);
  if (!res.ok) throw new Error('Invalid credentials');
  return body;
};

export const register = async (username: string, password: string, role: string): Promise<any> => {
  const res = await fetch(`${BASE_URL}/register`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ username, password, role })
  });
  if (!res.ok) throw new Error('Registration failed');
  return res.json();
};

let token: string = '';
let role: string = '';

export const setToken = (t: string) => {
  token = t;
  const payload = JSON.parse(atob(t.split('.')[1]));
  role = payload.role;
};

export const getToken = () => token;
export const getRole = () => role;
export const isAdmin = () => role === 'ADMIN';