// register/register.component.ts
import { Component } from '@angular/core';
import { FormsModule } from '@angular/forms';
import { AuthService } from '../../services/auth.service';
import { Router } from '@angular/router';

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

  //Hardcoding role to be "user!!" (can still make ppl admins from postman)
  role = 'user'; //maybe existing can promote then

  constructor(private router:Router, private authService: AuthService) {}

  onRegister() {
    this.authService.register(this.username, this.password, this.role).subscribe({
      next: () => {
        alert('Registration successful! You can now log in.')
        this.router.navigate(['/login'])
      },
      error: () => alert('Registration failed. Please try again.')
    });
  }
}