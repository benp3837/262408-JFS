import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';

@Injectable({ providedIn: 'root' })
export class UserService {

  private baseUrl = 'http://localhost:8080/users';

  constructor(private http: HttpClient) {}

  getAllUsers() {
    return this.http.get<any[]>(this.baseUrl);
  }
}