from fastapi import Request, Form, APIRouter, status, HTTPException
from fastapi.templating import Jinja2Templates
from fastapi.responses import RedirectResponse, HTMLResponse
from passlib.context import CryptContext
from typing import Optional
from fastapi import Request, Form
import logging

from database import users_data
from .cookie_handler import set_access_token_cookie
from .jwt_handler import create_access_token

logger = logging.getLogger(__name__)
router = APIRouter()
templates = Jinja2Templates(directory='templates')
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify plain password against hashed password."""
    return pwd_context.verify(plain_password, hashed_password)

@router.get("/login", response_class=HTMLResponse)
async def login(request: Request):
    """Display login page."""
    return templates.TemplateResponse("login.html", {"request": request})

@router.post("/login")
async def login_post(
    request: Request,
    email: Optional[str] = Form(None, description="User email address"),
    password: Optional[str] = Form(None, description="User password")
):
    """Authenticate user and set access token cookie."""
    try:
        email = email.lower().strip() if email else ""
        password = password.strip() if password else ""

        logger.info(f"=== Login attempt for email: {email or 'Empty'} ===")

        # Manual validation to avoid FastAPI 422 errors
        if not email:
            return templates.TemplateResponse("login.html", {
                "request": request,
                "message": "Email is required.",
                "email": ""  # Keeps it blank intentionally
            })

        if not password:
            return templates.TemplateResponse("login.html", {
                "request": request,
                "message": "Password is required.",
                "email": email  # Retain email
            })

        if users_data is None:
            logger.error("Database connection not available during login")
            return templates.TemplateResponse("login.html", {
                "request": request,
                "message": "Database connection error. Please try again later.",
                "email": email
            })

        logger.info(f"Searching for user with email: {email}")
        user = users_data.find_one({"email": email})

        if not user:
            logger.warning(f"Login attempt with non-existent email: {email}")
            return templates.TemplateResponse("login.html", {
                "request": request,
                "message": "Invalid email or password.",
                "email": email
            })

        if not verify_password(password, user["password"]):
            logger.warning(f"Invalid password for: {email}")
            return templates.TemplateResponse("login.html", {
                "request": request,
                "message": "Invalid email or password.",
                "email": email
            })

        access_token = create_access_token(
            data={"sub": user["email"]},
            expires_delta=100
        )

        response = RedirectResponse(
            url="/dashboard",
            status_code=status.HTTP_303_SEE_OTHER
        )
        set_access_token_cookie(response, access_token)

        logger.info(f"User {email} logged in successfully")
        return response

    except Exception as e:
        logger.error(f"Login error: {str(e)}")
        import traceback
        logger.error(traceback.format_exc())

        return templates.TemplateResponse("login.html", {
            "request": request,
            "message": "An unexpected error occurred. Please try again later.",
            "email": email if 'email' in locals() else ""
        })
