import datetime
import jwt
import os
import requests
from typing import Optional, Dict, Any
from passlib.context import CryptContext

SECRET_KEY = os.getenv("JWT_SECRET", "ilovepdf-secret-jwt-key-super-secure-2026")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_HOURS = 24

pwd_context = CryptContext(schemes=["pbkdf2_sha256"], deprecated="auto")

def hash_password(password: str) -> str:
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    try:
        return pwd_context.verify(plain_password, hashed_password)
    except Exception:
        # Fallback security check
        return False

def create_access_token(data: dict, expires_delta: Optional[datetime.timedelta] = None) -> str:
    to_encode = data.copy()
    if "sub" in to_encode:
        to_encode["sub"] = str(to_encode["sub"])
    if expires_delta:
        expire = datetime.datetime.utcnow() + expires_delta
    else:
        expire = datetime.datetime.utcnow() + datetime.timedelta(hours=ACCESS_TOKEN_EXPIRE_HOURS)
    
    to_encode.update({"exp": expire, "iat": datetime.datetime.utcnow()})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def decode_access_token(token: str) -> Optional[dict]:
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except (jwt.PyJWTError, Exception):
        return None

def verify_google_token(credential: str) -> Optional[Dict[str, Any]]:
    """
    Verifies a Google OAuth ID token using Google's tokeninfo endpoint.
    Returns user dictionary with email, name, picture if valid.
    """
    try:
        resp = requests.get(
            f"https://oauth2.googleapis.com/tokeninfo?id_token={credential}",
            timeout=5
        )
        if resp.status_code == 200:
            data = resp.json()
            return {
                "email": data.get("email"),
                "name": data.get("name") or data.get("given_name", "Google User"),
                "picture": data.get("picture"),
                "email_verified": data.get("email_verified") == "true" or data.get("email_verified") is True
            }
    except Exception as e:
        print(f"Google token verification error: {e}")
    return None
