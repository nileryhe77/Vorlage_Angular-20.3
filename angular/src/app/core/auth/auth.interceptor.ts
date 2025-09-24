import { inject } from '@angular/core';
import { HttpInterceptorFn } from '@angular/common/http';
import { from } from 'rxjs';
import { mergeMap } from 'rxjs/operators';
import { KeycloakService } from 'keycloak-angular';
import { environment } from '../../../environments/environment'; // korrekten Pfad prüfen

const allowedList: string[] = [
  `${environment.api.serverUrl}/appusers/sync`,
 
];



export const authInterceptor: HttpInterceptorFn = (req, next) => {
  const keycloak = inject(KeycloakService);

  const isAllowed = allowedList.some(url => req.url.startsWith(url));
  if (!isAllowed) {
    return next(req); // kein Token anhängen
  }

  return from(keycloak.updateToken(30)).pipe(
    mergeMap(() => keycloak.getToken()),
    mergeMap(token => {
      if (token) {
        const authReq = req.clone({
          setHeaders: { Authorization: `Bearer ${token}` }
        });
        return next(authReq);
      }
      return next(req);
    })
  );

};
