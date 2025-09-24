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
