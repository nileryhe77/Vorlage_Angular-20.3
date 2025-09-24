import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';   // 👈 wichtig
import { MatToolbarModule } from '@angular/material/toolbar';
import { MatButtonModule } from '@angular/material/button';
import { MatIconModule } from '@angular/material/icon';
import { RouterModule } from '@angular/router';
import { AuthService } from '../../../core/auth/auth.service';

@Component({
  selector: 'app-header',
  standalone: true,
  imports: [
    CommonModule,          // 👈 hinzufügen
    MatToolbarModule,
    MatButtonModule,
    MatIconModule,
    RouterModule
  ],
  templateUrl: './header.html'
})
export class Header implements OnInit {
  loggedIn = false;

  constructor(private authService: AuthService) { }

  async ngOnInit() {
    this.loggedIn = await this.authService.isLoggedIn();
    this.authService.loggedIn$.subscribe(status => {
      this.loggedIn = status;
    });
  }

  login() { this.authService.login(); }
  logout() { this.authService.logout(); }
}
