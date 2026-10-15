import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { UserService } from '../../services/user.service';
import { AuthService } from '../../services/auth.service';

@Component({
  selector: 'app-dashboard',
  standalone: true,
  imports: [CommonModule],
  templateUrl: './dashboard.component.html',
  styleUrl: './dashboard.component.css'
})
export class DashboardComponent implements OnInit {
  users: any[] = [];

  constructor(private userService: UserService, private authService: AuthService) {}

  // Getter so it's always evaluated fresh rather than set once on init
  get isAdmin(): boolean {
    return this.authService.isAdmin();
  }

  ngOnInit() {
    if (this.isAdmin) {
      this.userService.getAllUsers().subscribe({
        next: (data:any) => this.users = data,
        error: () => alert('Failed to load users.')
      });
    }
  }
}