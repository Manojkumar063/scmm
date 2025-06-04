from jose import jwt, JWTError
from datetime import datetime, timedelta
from fastapi.responses import RedirectResponse
from fastapi import Cookie, HTTPException, status, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
import os
from dotenv import load_dotenv
from typing import Dict, Optional, Union
import logging

load_dotenv()

# Set up logger
logger = logging.getLogger(__name__)

JWT_SECRET = os.getenv("JWT_SECRET")
JWT_ALGORITHM = os.getenv("JWT_ALGORITHM", "HS256")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "100"))

# Validate JWT configuration
if not JWT_SECRET:
    logger.error("JWT_SECRET environment variable not set")
    raise ValueError("JWT_SECRET environment variable is required")

# HTTP Bearer for Swagger UI
security = HTTPBearer(auto_error=False)

def create_access_token(data: Dict[str, str], expires_delta: Optional[int] = None) -> str:
    """Create JWT access token with expiration."""
    to_encode = data.copy()
    expire_minutes = expires_delta or ACCESS_TOKEN_EXPIRE_MINUTES
    expire = datetime.utcnow() + timedelta(minutes=30)
    to_encode.update({'exp': expire, 'iat': datetime.utcnow()})
    
    logger.info(f"Creating token for {data.get('sub')} with {expire_minutes} minutes expiry")
    return jwt.encode(to_encode, JWT_SECRET, algorithm=JWT_ALGORITHM)

def verify_token(token: str) -> Dict[str, str]:
    """Verify and decode JWT token."""
    try:
        # Remove Bearer prefix if present
        token = token.replace("Bearer ", "") if token.startswith("Bearer ") else token
        logger.info(f"Processing token (first 20 chars): {token[:20]}...")
        
        payload = jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
        email = payload.get("sub")
        
        if email is None:
            logger.warning("Token payload missing 'sub' field")
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token payload"
            )
        
        # Check token expiration
        exp = payload.get("exp")
        if exp:
            if datetime.utcnow() > datetime.fromtimestamp(exp):
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

def get_current_user(
    access_token: Optional[str] = Cookie(None),
    credentials: Optional[HTTPAuthorizationCredentials] = Depends(security)
) -> Dict[str, str]:
    """Extract and validate current user from JWT token (Cookie or Authorization header)."""
    token = None
    
    # Try Authorization header first (for Swagger/API usage)
    if credentials:
        token = credentials.credentials
        logger.info("Token from Authorization header")
    # Fall back to cookie (for web UI)
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