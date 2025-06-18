# import os
# from dotenv import load_dotenv

# load_dotenv()

# # Email configuration from environment variables
# EMAIL_HOST = os.getenv("EMAIL_HOST")
# EMAIL_PORT = int(os.getenv("EMAIL_PORT", 587))
# EMAIL_USERNAME = os.getenv("EMAIL_USERNAME")
# EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD")
# EMAIL_USE_TLS = os.getenv("EMAIL_USE_TLS", "true").lower() == "true"
# BASE_URL = os.getenv("BASE_URL", "http://localhost:8000")

# # Validate required email configuration
# if not all([EMAIL_HOST, EMAIL_USERNAME, EMAIL_PASSWORD]):
#     raise ValueError("Email configuration is incomplete. Check EMAIL_HOST, EMAIL_USERNAME, and EMAIL_PASSWORD environment variables.")

# def send_reset_email(email: str, reset_token: str, base_url: str = None):
#     """Send password reset email"""
#     if base_url is None:
#         base_url = BASE_URL
        
#     try:
#         # Create message
#         msg = MIMEMultipart()
#         msg['From'] = EMAIL_USERNAME
#         msg['To'] = email
#         msg['Subject'] = "Password Reset Request - SCM System"
        
#         # Email body (same as before)
#         reset_link = f"{base_url}/reset-password?token={reset_token}"
#         # ... rest of your email body code ...
        
#         # Send email with improved error handling
#         with smtplib.SMTP(EMAIL_HOST, EMAIL_PORT) as server:
#             if EMAIL_USE_TLS:
#                 server.starttls()
#             server.login(EMAIL_USERNAME, EMAIL_PASSWORD)
#             text = msg.as_string()
#             server.sendmail(EMAIL_USERNAME, email, text)
        
#         return True
#     except Exception as e:
#         print(f"Failed to send email: {str(e)}")
#         return False