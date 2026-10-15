import { Injectable } from '@angular/core';
import { HttpClient, HttpHeaders } from '@angular/common/http';

@Injectable({ providedIn: 'root' })
export class AuthService {

  private baseUrl = 'http://localhost:8080/auth';
  private token: string = '';
  private role: string = '';

  constructor(private http: HttpClient) {}

  login(username: string, password: string) {
    return this.http.post(`${this.baseUrl}`, { username, password }, { responseType: 'text' });
  }

  register(username: string, password: string, role: string) {
    return this.http.post(`${this.baseUrl}/register`, { username, password, role });
  }

  setToken(token: string) {
    this.token = token;
    const payload = JSON.parse(atob(token.split('.')[1]));
    this.role = payload.role;
    console.log('Token set. Role:', this.role);
  }

  getToken() { return this.token; }
  getRole() { return this.role; }
  isAdmin() { return this.role.toUpperCase() === 'ROLE_ADMIN'; }

  getAuthHeaders() {
    return new HttpHeaders({ Authorization: `Bearer ${this.token}` });
  }
}