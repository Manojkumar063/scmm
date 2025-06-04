from fastapi.responses import Response
from typing import Optional

def set_access_token_cookie(response: Response, access_token: str) -> None:
    """Set HTTP-only access token cookie with secure configuration."""
    response.set_cookie(
        key="access_token",
        value=f"Bearer {access_token}",
        httponly=True,
        secure=False,  # Set to True in production with HTTPS
        max_age=120 * 100,  # 200 minutes
        samesite="lax"
    )

def delete_access_token_cookie(response: Response) -> None:
    """Delete access token cookie."""
    response.delete_cookie(
        key="access_token",
        httponly=True,
        secure=False,  # Set to True in production with HTTPS
        samesite="lax"
    )