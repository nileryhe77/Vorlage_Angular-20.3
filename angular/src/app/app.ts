import { Component, signal } from '@angular/core';
import { RouterOutlet } from '@angular/router';
import { CommonModule } from '@angular/common';
import { Header } from './shared/components/header/header';
import { Sidebar } from './shared/components/sidebar/sidebar';
import { AuthService } from './core/auth/auth.service';

@Component({
  selector: 'app-root',
  imports: [CommonModule, RouterOutlet, Header, Sidebar], // 👈 wichtig
  templateUrl: './app.html',
  styleUrl: './app.css'
})
export class App {
  loggedIn = false;

  constructor(private auth: AuthService) { }

  ngOnInit() {
    this.auth.loggedIn$.subscribe(status => {
      this.loggedIn = status;
    });
  }

  login() {
    this.auth.login();
  }
}
