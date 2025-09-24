# -*- coding: utf-8 -*-
from fastapi import APIRouter, Depends
from auth.jwt_auth import verify_token

router = APIRouter(prefix="/test", tags=["Test"])

@router.get("/")
async def test_root():
    return {"msg": "Test-Endpoint lueuft"}

@router.get("/secure")
async def test_secure(user=Depends(verify_token)):
    return {"msg": f"Hallo {user['preferred_username']}, du bist eingeloggt"}
