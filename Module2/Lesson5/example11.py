import os
import secrets
from fastapi import FastAPI, Request, HTTPException, status, Depends
from fastapi.responses import HTMLResponse
from starlette.middleware.sessions import SessionMiddleware
from starlette.middleware.cors import CORSMiddleware
from starlette.middleware.base import BaseHTTPMiddleware
from pydantic import BaseModel, Field, EmailStr
from typing import Optional
from passlib.context import CryptContext
from itsdangerous import URLSafeTimedSerializer
import html
import bleach

# --- Configuration ---
# Use a strong, random secret key for production environments
# For demonstration, we'll use a simple one, but NEVER do this in production.
SECRET_KEY = os.getenv("SECRET_KEY", secrets.token_urlsafe(32))
CSRF_TOKEN_SECRET = os.getenv("CSRF_TOKEN_SECRET", secrets.token_urlsafe(32)) # Separate secret for CSRF
serializer = URLSafeTimedSerializer(CSRF_TOKEN_SECRET)

# Password hashing context
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

app = FastAPI(
    title="Secure FastAPI Demo",
    description="Demonstrating common backend vulnerabilities and FastAPI mitigations."
)

# --- Middleware ---

# 1. CORS Middleware (related to security, allowing specific origins)
# You should configure allowed_origins strictly for your frontend applications.
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:8000", "http://localhost:3000"],  # Replace with your frontend origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 2. Session Middleware (for CSRF token storage in this example)
app.add_middleware(SessionMiddleware, secret_key=SECRET_KEY)

# 3. Security Headers Middleware
class SecurityHeadersMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request, call_next):
        response = await call_next(request)
        response.headers["X-Content-Type-Options"] = "nosniff"
        response.headers["X-Frame-Options"] = "DENY"
        response.headers["Referrer-Policy"] = "strict-origin-when-cross-origin"
        # Content-Security-Policy is set on specific routes or responses if needed
        return response
app.add_middleware(SecurityHeadersMiddleware)


# --- Security Utilities and Dependencies ---

# Password Hashing
def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)

def verify_password_hash(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

# CSRF Token Generation and Verification
def generate_csrf_token(request: Request):
    if "csrf_token" not in request.session:
        # Generate a unique token, linked to the session
        token = serializer.dumps(request.session.session_id + str(secrets.token_hex(8)))
        request.session["csrf_token"] = token
    return request.session["csrf_token"]

def verify_csrf_token_dependency(request: Request):
    form_token = request.headers.get("X-CSRF-Token") or request.query_params.get("csrf_token")
    session_token = request.session.get("csrf_token")

    if not form_token or not session_token:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="CSRF token missing")

    try:
        # Validate the token's signature and freshness
        serializer.loads(form_token, max_age=3600) # Token valid for 1 hour
    except Exception:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Invalid or expired CSRF token")

    if form_token != session_token:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="CSRF token mismatch")
    
    return True # Token is valid


# --- Pydantic Models ---
class UserCreate(BaseModel):
    username: str = Field(..., min_length=3, max_length=20, pattern="^[a-zA-Z0-9_]+$")
    email: EmailStr
    password: str = Field(..., min_length=8)

class UserLogin(BaseModel):
    username: str
    password: str

class Comment(BaseModel):
    text: str = Field(..., max_length=500)

class PasswordChange(BaseModel):
    old_password: str
    new_password: str = Field(..., min_length=8)

# --- Endpoint Definitions ---

# Mock database (for demonstration purposes only)
fake_db = {
    "admin": {
        "email": "admin@example.com",
        "hashed_password": get_password_hash("adminsecurepassword123"),
        "role": "admin"
    }
}

@app.post("/register", status_code=status.HTTP_201_CREATED)
async def register_user(user: UserCreate):
    # Input validation handled by Pydantic automatically.
    if user.username in fake_db:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Username already exists")
    
    fake_db[user.username] = {
        "email": user.email,
        "hashed_password": get_password_hash(user.password),
        "role": "user"
    }
    return {"message": "User registered successfully", "username": user.username}

@app.post("/login")
async def login_user(request: Request, user: UserLogin):
    user_in_db = fake_db.get(user.username)
    if not user_in_db or not verify_password_hash(user.password, user_in_db["hashed_password"]):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
    
    # Simulate a successful login by setting a session variable
    # In a real app, this would be a JWT token or similar.
    request.session["username"] = user.username
    request.session["user_role"] = user_in_db["role"]
    return {"message": "Login successful", "username": user.username}

@app.get("/profile")
async def get_profile(request: Request):
    username = request.session.get("username")
    if not username:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Not authenticated")
    
    user_data = fake_db.get(username)
    if not user_data: # Should not happen if session is valid
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    
    # Sensitive data exposure mitigation: DO NOT return hashed password.
    return {"username": username, "email": user_data["email"], "role": user_data["role"]}


@app.post("/submit_comment", dependencies=[Depends(verify_csrf_token_dependency)])
async def submit_comment(request: Request, comment: Comment):
    # Input validation (max_length) handled by Pydantic.
    # Manual sanitization for rich text content to prevent XSS.
    # We strip all tags in this example for maximum security, but you might allow a few.
    cleaned_text = bleach.clean(comment.text, tags=[], strip=True) 

    # In a real app, save cleaned_text to database, associated with the user
    print(f"Comment from {request.session.get('username', 'anonymous')}: {cleaned_text}")
    return {"message": "Comment submitted and sanitized", "original_text": comment.text, "cleaned_text": cleaned_text}

@app.get("/view_comments", response_class=HTMLResponse)
async def view_comments(request: Request):
    # This is a highly simplified example. In a real application, comments would come from a database.
    # Assume a stored comment list for demonstration:
    stored_comments = [
        {"user": "Alice", "text": "Hello, everyone!"},
        {"user": "Bob", "text": "This is a <script>alert('malicious')</script> comment."}
    ]

    comment_html = ""
    for c in stored_comments:
        # Output encoding is crucial here to prevent stored XSS.
        escaped_text = html.escape(c["text"])
        escaped_user = html.escape(c["user"])
        comment_html += f"<p><b>{escaped_user}:</b> {escaped_text}</p>"

    # Example of CSP header on an HTML response
    response = HTMLResponse(f"""
        <html>
            <head>
                <title>Comments</title>
                <style>body {{ font-family: sans-serif; }}</style>
            </head>
            <body>
                <h1>User Comments</h1>
                {comment_html}
            </body>
        </html>
    """)
    response.headers["Content-Security-Policy"] = "default-src 'self'; script-src 'self';" # Restrict scripts to same origin
    return response

@app.post("/change-password", dependencies=[Depends(verify_csrf_token_dependency)])
async def change_password(request: Request, password_change: PasswordChange):
    username = request.session.get("username")
    if not username:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Not authenticated")
    
    user_in_db = fake_db.get(username)
    if not user_in_db or not verify_password_hash(password_change.old_password, user_in_db["hashed_password"]):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid old password")

    # Update password
    user_in_db["hashed_password"] = get_password_hash(password_change.new_password)
    fake_db[username] = user_in_db # Update the mock DB
    return {"message": "Password changed successfully"}

@app.get("/", response_class=HTMLResponse)
async def home(request: Request, csrf_token: str = Depends(generate_csrf_token)):
    username = request.session.get("username", "Guest")
    
    # HTML form with CSRF token for password change example
    return f"""
    <html>
        <head>
            <title>FastAPI Security Demo</title>
            <script>
                // Function to handle form submission via Fetch API
                async function submitComment() {{
                    const commentText = document.getElementById('comment_text').value;
                    const csrfToken = document.getElementById('csrf_token').value;
                    
                    const response = await fetch('/submit_comment', {{
                        method: 'POST',
                        headers: {{
                            'Content-Type': 'application/json',
                            'X-CSRF-Token': csrfToken // Send CSRF token in header
                        }},
                        body: JSON.stringify({{ text: commentText }})
                    }});
                    const data = await response.json();
                    alert(JSON.stringify(data));
                }}

                async function changePassword() {{
                    const oldPassword = document.getElementById('old_password').value;
                    const newPassword = document.getElementById('new_password').value;
                    const csrfToken = document.getElementById('csrf_token').value;

                    const response = await fetch('/change-password', {{
                        method: 'POST',
                        headers: {{
                            'Content-Type': 'application/json',
                            'X-CSRF-Token': csrfToken
                        }},
                        body: JSON.stringify({{ old_password: oldPassword, new_password: newPassword }})
                    }});
                    const data = await response.json();
                    alert(JSON.stringify(data));
                }}
            </script>
            <style>
                body {{ font-family: sans-serif; max-width: 800px; margin: auto; padding: 20px; }}
                h1 {{ color: #333; }}
                form {{ background: #f9f9f9; padding: 15px; border-radius: 8px; margin-bottom: 20px; }}
                label {{ display: block; margin-bottom: 5px; font-weight: bold; }}
                input[type="text"], input[type="password"], textarea {{
                    width: calc(100% - 22px); padding: 10px; margin-bottom: 10px; border: 1px solid #ddd; border-radius: 4px;
                }}
                button {{ background-color: #007bff; color: white; padding: 10px 15px; border: none; border-radius: 4px; cursor: pointer; }}
                button:hover {{ background-color: #0056b3; }}
                .section {{ margin-top: 30px; border-top: 1px solid #eee; padding-top: 20px; }}
            </style>
        </head>
        <body>
            <h1>Welcome, {username}!</h1>
            <p>This page demonstrates various security features in FastAPI.</p>

            <div class="section">
                <h2>Submit a Comment (CSRF Protected & XSS Sanitized)</h2>
                <form onsubmit="event.preventDefault(); submitComment();">
                    <input type="hidden" id="csrf_token" name="csrf_token" value="{csrf_token}">
                    <label for="comment_text">Your Comment (try injecting &lt;script&gt;alert('XSS')&lt;/script&gt;):</label>
                    <textarea id="comment_text" name="comment_text" rows="4">Hello, world! This is my comment.</textarea>
                    <button type="submit">Post Comment</button>
                </form>
                <p>Visit <a href="/view_comments" target="_blank">/view_comments</a> to see how comments are displayed (output encoded).</p>
            </div>

            <div class="section">
                <h2>Change Password (CSRF Protected)</h2>
                <p>Log in with 'admin' / 'adminsecurepassword123' first.</p>
                <form onsubmit="event.preventDefault(); changePassword();">
                    <input type="hidden" name="csrf_token" value="{csrf_token}">
                    <label for="old_password">Old Password:</label>
                    <input type="password" id="old_password" name="old_password">
                    <label for="new_password">New Password:</label>
                    <input type="password" id="new_password" name="new_password">
                    <button type="submit">Change Password</button>
                </form>
            </div>

            <div class="section">
                <h2>User Registration</h2>
                <p>Test Pydantic validation: try invalid email, short password/username, or existing username at <a href="/docs" target="_blank">/docs</a>.</p>
            </div>
            <div class="section">
                <h2>Current Profile</h2>
                <p>View your profile: <a href="/profile" target="_blank">/profile</a> (requires login).</p>
            </div>
        </body>
    </html>
    """