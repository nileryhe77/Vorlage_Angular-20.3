# -*- coding: utf-8 -*-

import httpx
import time
from jose import jwt, JWTError
from fastapi import Request, HTTPException, Depends
from application.config import settings


_jwks_cache = None           # hier speichern wir das zuletzt geholte JWKS
_jwks_last_fetch = 0         # wann zuletzt vom Server geholt (Unix-Zeitstempel)
_JWKS_TTL = 3600             # Gültigkeit: 3600 Sekunden = 1 Stunde

async def get_jwks():
    """Holt die JWKS von Keycloak – aber cached sie für 1 Stunde."""
    global _jwks_cache, _jwks_last_fetch
    now = time.time()

    # 1. Wenn wir schon ein JWKS im Cache haben und es noch gültig ist → Cache zurückgeben
    if _jwks_cache and (now - _jwks_last_fetch) < _JWKS_TTL:
        return _jwks_cache

    # 2. Sonst: Keycloak fragen und Ergebnis im Cache speichern
    jwks_url = f"{settings.keycloak_url}/realms/{settings.keycloak_realm}/protocol/openid-connect/certs"
    async with httpx.AsyncClient() as client:
        response = await client.get(jwks_url)
        response.raise_for_status()
        _jwks_cache = response.json()
        _jwks_last_fetch = now
        return _jwks_cache


# -------------------------------------------------------------------
# Token verifizieren
# -------------------------------------------------------------------
async def verify_token(request: Request):
    # 1. Token aus dem Header lesen
    auth = request.headers.get("authorization")
    if not auth or not auth.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Token fehlt oder ungültig")

    token = auth.split(" ")[1]

    # 2. Header auslesen → dort steht, welcher Key benutzt wurde
    unverified_header = jwt.get_unverified_header(token)

    # 3. JWKS holen (jetzt mit Cache)
    jwks = await get_jwks()

    # 4. Passenden Public Key im JWKS suchen
    key = next((k for k in jwks["keys"] if k["kid"] == unverified_header["kid"]), None)
    if not key:
        raise HTTPException(status_code=401, detail="Passender Key nicht gefunden")

    # 5. Token mit dem Public Key prüfen
    try:
        payload = jwt.decode(
            token,
            key,
            algorithms=["RS256"],
            audience=settings.keycloak_client_id,
            issuer=f"{settings.keycloak_url}/realms/{settings.keycloak_realm}"
        )
        # 6. Optional: einen "Usernamen" für Logs ermitteln
        user = payload.get("preferred_username") or payload.get("email") or payload.get("sub")
        # print(f"Zugriff durch: {user}")
        return payload
    except JWTError:
        raise HTTPException(status_code=401, detail="Token ungültig oder abgelaufen")


# -------------------------------------------------------------------
# Rollenprüfung (optional)
# -------------------------------------------------------------------
def require_role(role: str):
    async def role_checker(user=Depends(verify_token)):
        roles = user.get("realm_access", {}).get("roles", [])
        if role not in roles:
            raise HTTPException(status_code=403, detail=f"Zugriff verweigert – Rolle '{role}' fehlt")
        return user
    return role_checker
