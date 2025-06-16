from fastapi import APIRouter, Request
from fastapi.templating import Jinja2Templates
from .cookie_handler import delete_access_token_cookie

router = APIRouter()
templates = Jinja2Templates(directory='templates')

@router.get('/logout')
def logout(request: Request):
    """Handle user logout by clearing access token cookie and rendering login page."""
    response = templates.TemplateResponse(
        'landingpage.html',
        context={
            'request': request,
            'message': 'You have been logged out successfully.'
        }
    )
    delete_access_token_cookie(response)
    return response