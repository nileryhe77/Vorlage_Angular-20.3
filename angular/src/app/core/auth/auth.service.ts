import { Injectable } from '@angular/core';
import { KeycloakService } from 'keycloak-angular';
import { BehaviorSubject } from 'rxjs';

@Injectable({ providedIn: 'root' })
export class AuthService {
  private loggedInSubject = new BehaviorSubject<boolean>(false);
  loggedIn$ = this.loggedInSubject.asObservable();

  constructor(private keycloak: KeycloakService) {
    this.updateLoginStatus();
  }

  /** Login-Status prüfen und streamen */
  async updateLoginStatus(): Promise<void> {
    const status = await this.keycloak.isLoggedIn();
    this.loggedInSubject.next(status);
  }

  /** Einzelne Abfrage möglich */
  async isLoggedIn(): Promise<boolean> {
    return this.keycloak.isLoggedIn();
  }

  login(): void {
    this.keycloak.login();
  }

  logout(): void {
    this.keycloak.logout(window.location.origin);
  }
}
