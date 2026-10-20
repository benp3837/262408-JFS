import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';

@Injectable({ providedIn: 'root' })
export class UserService {

  private baseUrl = 'http://localhost:8080/users';
  username: string = '';

  constructor(private http: HttpClient) {}

  login(username: string, password: string) {
    return this.http.post<any>(`${this.baseUrl}/login`, { username, password });
  }

  register(username: string, password: string) {
    return this.http.post(`${this.baseUrl}/register`, { username, password, role: 'user' });
  }

  getWelcome() {
    return this.http.get<any>(`${this.baseUrl}/welcome/${this.username}`);
  }
}