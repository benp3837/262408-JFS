// dashboard/dashboard.component.ts
import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';

@Component({
  selector: 'app-dashboard',
  standalone: true,
  imports: [CommonModule],
  templateUrl: './dashboard.component.html',
  styleUrl: './dashboard.component.css'
})
export class DashboardComponent {

  //TODO: subscribe to the call to get all games in the service

  //just some AI dummy data for now

  users = [
    { id: 1, name: 'Alice Johnson', email: 'alice@example.com', role: 'Admin' },
    { id: 2, name: 'Bob Smith',     email: 'bob@example.com',   role: 'Editor' },
    { id: 3, name: 'Carol White',   email: 'carol@example.com', role: 'Viewer' }
  ];
}