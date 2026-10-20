import { Component } from '@angular/core';
import { FormsModule } from '@angular/forms';
import { RouterLink, Router } from '@angular/router';
import { UserService } from '../../services/user.service';

@Component({
  selector: 'app-login',
  standalone: true,
  imports: [FormsModule, RouterLink],
  templateUrl: './login.component.html',
  styleUrl: './login.component.css'
})
export class LoginComponent {
  username = '';
  password = '';

  constructor(private userService: UserService, private router: Router) {}

  onLogin() {
    this.userService.login(this.username, this.password).subscribe({
      next: (user) => {
        this.userService.username = user.username;
        this.router.navigate(['/dashboard']);
      },
      error: () => alert('Login failed.')
    });
  }
}