# anwendung erstellen 
<!-- Auf aktuellen stand bringen -->
npm uninstall -g @angular/cli
npm cache clean --force
npm install -g @angular/cli@latest
ng version
<!-- neues projekt anlegen -->
ng new angular
npm install bootstrap
ng add @angular/material
npm install @angular/animations
npm install keycloak-angular keycloak-js



<!-- environment.ts und environment.development.ts anlegen -->
<!-- environment.ts -->
```
export const environment = {
  production: false,
  keycloak: {
    url: 'https://auth.schatzbuch.io',
    realm: 'schatzbuch',
    clientId: 'schatzbuch-spa'
  },
  api: {
    serverUrl: 'http://localhost:6060'
  },
  postLogoutRedirect: 'http://localhost:4040/'
};
```
<!-- environment.development.ts -->
```
export const environment = {
  production: false,
  keycloak: {
    url: 'https://auth.schatzbuch.io',
    realm: 'schatzbuch',
    clientId: 'schatzbuch-spa'
  },
  api: {
    serverUrl: 'http://localhost:6060'
  },
  postLogoutRedirect: 'http://localhost:4040/'
};
```





# Python anlegen 
python -m venv venv
venv\Scripts\activate.bat  <!-- Windows -->
pip install fastapi uvicorn[standard] python-keycloak
