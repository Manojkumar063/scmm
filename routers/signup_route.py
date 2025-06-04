from fastapi import APIRouter, Request, Form, HTTPException, status
from fastapi.templating import Jinja2Templates
from fastapi.responses import RedirectResponse
from passlib.context import CryptContext
import re
import logging
from typing import Optional

from database import users_data
from models import Users

logger = logging.getLogger(__name__)
router = APIRouter()
templates = Jinja2Templates(directory='templates')
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def validate_password(password: str) -> Optional[str]:
    """Validate password strength and return error message if invalid."""
    if len(password) < 8:
        return "Password should be at least 8 characters long"
    if not any(char.isdigit() for char in password):
        return "Password should contain at least one digit"
    if not any(char.isalpha() for char in password):
        return "Password should contain at least one alphabet"
    if not re.search(r'[!@#$%^&*(),.?\":{}|<>]', password):
        return "Password should contain at least one special character"
    return None

def validate_email(email: str) -> bool:
    """Basic email validation."""
    email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(email_pattern, email) is not None

@router.get("/register")
async def show_register(request: Request):
    """Display registration page."""
    return templates.TemplateResponse("register.html", {"request": request})

@router.get('/')
def register(request: Request):
    """Display registration page (root route)."""
    return templates.TemplateResponse("register.html", {"request": request})

@router.post("/register")
async def register_user(
    request: Request,
    username: str = Form(...),
    email: str = Form(...),
    password: str = Form(...),
    confirm_password: str = Form(...),
    role: str = Form(...),
):
    """Register new user with validation."""
    # Log the registration attempt
    logger.info(f"New registration attempt - Email: {email}, Username: {username}, Role: {role}")
    try:
        logger.info(f"Registration attempt for email: {email}")
        
        # Clean inputs
        email = email.lower().strip()
        username = username.strip()
        
        logger.info(f"Cleaned email: {email}, username: {username}")

        # Check database connection
        if users_data is None:
            logger.error("Database connection not available during registration")
            return templates.TemplateResponse("register.html", {
                "request": request,
                "message": "Database connection error. Please try again later."
            })

        # Email validation
        if not validate_email(email):
            logger.warning(f"Invalid email format: {email}")
            return templates.TemplateResponse("register.html", {
                "request": request,
                "message": "Please enter a valid email address."
            })

        # Password match
        if password != confirm_password:
            logger.warning(f"Password mismatch for {email}")
            return templates.TemplateResponse("register.html", {
                "request": request,
                "message": "Passwords do not match."
            })

        # Password strength
        password_error = validate_password(password)
        if password_error:
            logger.warning(f"Password validation failed for {email}: {password_error}")
            return templates.TemplateResponse("register.html", {
                "request": request,
                "message": password_error
            })

        # Check for existing email
        existing_user = users_data.find_one({"email": email})
        if existing_user:
            logger.warning(f"Email already exists: {email}")
            return templates.TemplateResponse("register.html", {
                "request": request,
                "message": "Email already registered."
            })

        # Hash password
        hashed_password = pwd_context.hash(password)
        logger.info(f"Password hashed successfully for {email}")

        # Create user document
        user_doc = Users(
            username=username,
            email=email,
            password=hashed_password,
            role=role
        )
        
        # Convert to dict and log the document
        user_dict = user_doc.dict()
        logger.info(f"User document created for: {email}")

        # Insert user into database
        try:
            result = users_data.insert_one(user_dict)
            logger.info(f"Insert result: {result}")
            logger.info(f"Inserted ID: {result.inserted_id}")
            
            if not result.inserted_id:
                raise Exception("Failed to insert user - no ID returned")
                
            # Verify the insertion by querying back
            inserted_user = users_data.find_one({"_id": result.inserted_id})
            if inserted_user:
                logger.info(f"User successfully verified in database: {inserted_user['email']}")
                
                # Also check total count
                total_users = users_data.count_documents({})
                logger.info(f"Total users in database: {total_users}")
            else:
                logger.error(f"User not found after insertion: {result.inserted_id}")
                raise Exception("User insertion verification failed")
                
        except Exception as db_error:
            logger.error(f"Database insertion error for {email}: {str(db_error)}")
            logger.error(f"Database error type: {type(db_error)}")
            raise db_error

        logger.info(f"User registered successfully: {email}")
        return RedirectResponse(url="/login", status_code=status.HTTP_303_SEE_OTHER)

    except Exception as e:
        logger.error(f"Registration error for {email}: {str(e)}")
        logger.error(f"Error type: {type(e)}")
        import traceback
        logger.error(f"Full traceback: {traceback.format_exc()}")
        
        return templates.TemplateResponse("register.html", {
            "request": request,
            "message": "Something went wrong. Please try again."
        })

def debug_database_connection():
    """Test database connection and operations."""
    try:
        if users_data is None:
            logger.error("users_data is None - database connection failed")
            return False
            
        # Test connection
        db_stats = users_data.database.command("dbstats")
        logger.info(f"Database stats: {db_stats}")
        
        # Test collection access
        collection_stats = users_data.database.command("collStats", users_data.name)
        logger.info(f"Collection stats: {collection_stats}")
        
        # Count documents
        count = users_data.count_documents({})
        logger.info(f"Current user count: {count}")
        
        return True
    except Exception as e:
        logger.error(f"Database connection test failed: {str(e)}")
        return False