import { Component, OnInit, OnDestroy } from '@angular/core';
import { CommonModule } from '@angular/common';
import { UserService } from '../../services/user.service';

@Component({
  selector: 'app-dashboard',
  standalone: true,
  imports: [CommonModule],
  templateUrl: './dashboard.component.html',
  styleUrl: './dashboard.component.css'
})
export class DashboardComponent implements OnInit, OnDestroy {
  welcomeMessage = '';

  // Claude gave me a pretty good "DVD logo floating on the screen" effect

  // Bouncing DVD logo state vars
  x = 150;
  y = 150;
  dx = 2;
  dy = 2;
  imgWidth = 150;
  imgHeight = 150;
  imgSrc: string = '';
  private animationId: any;

  constructor(private userService: UserService) {}

ngOnInit() {
  //one lil GET request to greet the user with their name
  this.userService.getWelcome().subscribe({
    next: (msg) => this.welcomeMessage = msg,
    error: () => this.welcomeMessage = 'Welcome!'
  });

  const pokemon = ['groudon.png', 'kyogre.png', 'latias.png', 'mudkip.png', 'torchic.png', 'treecko.png'];
  this.imgSrc = '/' + pokemon[Math.floor(Math.random() * pokemon.length)];

  this.animate();
}


//FLoating animation which is called in the onOnit() right above this
  animate() {
    this.animationId = setInterval(() => {
      this.x += this.dx;
      this.y += this.dy;

      const maxX = window.innerWidth - this.imgWidth;
      const maxY = window.innerHeight - this.imgHeight - 80; // leave room for header

      if (this.x <= 0 || this.x >= maxX) this.dx *= -1;
      if (this.y <= 0 || this.y >= maxY) this.dy *= -1;

      this.x = Math.max(0, Math.min(this.x, maxX));
      this.y = Math.max(0, Math.min(this.y, maxY));
    }, 16); // ~60fps
  }

  ngOnDestroy() {
    clearInterval(this.animationId);
  }
}