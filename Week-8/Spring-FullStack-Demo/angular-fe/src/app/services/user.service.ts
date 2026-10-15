import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { AuthService } from './auth.service';

@Injectable({ providedIn: 'root' })
export class UserService {

  private baseUrl = 'http://localhost:8080/users';

  constructor(private http: HttpClient, private authService: AuthService) {}

  getAllUsers() {
    return this.http.get<any[]>(this.baseUrl, { headers: this.authService.getAuthHeaders() });
  }
}