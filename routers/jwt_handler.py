# __________________________
# Imports
# __________________________

from datetime import datetime, timedelta
from typing import Dict, Optional

from jose import jwt, JWTError
from fastapi import Cookie, HTTPException, status, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from fastapi.responses import RedirectResponse

import os
import logging
from dotenv import load_dotenv


# __________________________
# Environment Setup & Config
# __________________________

load_dotenv()

logger = logging.getLogger(__name__)

JWT_SECRET = os.getenv("JWT_SECRET")
JWT_ALGORITHM = os.getenv("JWT_ALGORITHM", "HS256")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "100"))

if not JWT_SECRET:
    logger.error("JWT_SECRET environment variable not set")
    raise ValueError("JWT_SECRET environment variable is required")

security = HTTPBearer(auto_error=False)


# __________________________
# JWT Token Creation
# __________________________

def create_access_token(data: Dict[str, str], expires_delta: Optional[int] = None) -> str:
    """Create JWT access token with expiration."""
    to_encode = data.copy()
    expire_minutes = expires_delta or ACCESS_TOKEN_EXPIRE_MINUTES
    expire = datetime.utcnow() + timedelta(minutes=30)

    to_encode.update({
        'exp': expire,
        'iat': datetime.utcnow()
    })

    logger.info(f"Creating token for {data.get('sub')} with {expire_minutes} minutes expiry")
    return jwt.encode(to_encode, JWT_SECRET, algorithm=JWT_ALGORITHM)


# __________________________
# JWT Token Verification
# __________________________

def verify_token(token: str) -> Dict[str, str]:
    """Verify and decode JWT token."""
    try:
        # Remove Bearer prefix if present
        token = token.replace("Bearer ", "") if token.startswith("Bearer ") else token
        logger.info(f"Processing token (first 20 chars): {token[:20]}...")

        payload = jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
        email = payload.get("sub")

        if not email:
            logger.warning("Token payload missing 'sub' field")
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token payload"
            )

        # Check token expiration
        exp = payload.get("exp")
        if exp and datetime.utcnow() > datetime.fromtimestamp(exp):
            logger.warning(f"Token expired for user: {email}")
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Token has expired"
            )

        logger.info(f"Token validated successfully for user: {email}")
        return {"email": email}

    except JWTError as e:
        logger.error(f"JWT validation error: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token"
        )


# __________________________
# Dependency: Get Current User
# __________________________

def get_current_user(
    access_token: Optional[str] = Cookie(None),
    credentials: Optional[HTTPAuthorizationCredentials] = Depends(security)
) -> Dict[str, str]:
    """
    Extract and validate current user from JWT token.
    - Tries Authorization header first (for Swagger/API usage)
    - Falls back to access_token cookie (for web UI)
    """
    token = None

    if credentials:
        token = credentials.credentials
        logger.info("Token from Authorization header")
    elif access_token:
        token = access_token
        logger.info("Token from cookie")

    if not token:
        logger.warning("No access token provided")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Authentication required"
        )

    return verify_token(token)
