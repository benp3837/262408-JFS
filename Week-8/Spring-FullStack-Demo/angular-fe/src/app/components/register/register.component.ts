// register/register.component.ts
import { Component } from '@angular/core';
import { FormsModule } from '@angular/forms';
import { AuthService } from '../../services/auth.service';

@Component({
  selector: 'app-register',
  standalone: true,
  imports: [FormsModule],
  templateUrl: './register.component.html',
  styleUrl: './register.component.css'
})
export class RegisterComponent {
  username = '';
  password = '';
  confirmPassword = '';

  constructor(private authService: AuthService) {}

  onRegister() {
    this.authService.register(this.username, this.password).subscribe({
      next: () => alert('Registration successful! You can now log in.'),
      error: () => alert('Registration failed. Please try again.')
    });
  }
}