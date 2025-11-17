# FastAPI does not have built-in CSRF protection like Django.
# You typically use a library or implement custom middleware.
# Here's a conceptual example using a library like 'fastapi-csrf-token' (pip install fastapi-csrf-token)
from fastapi import Request, Depends
from starlette.middleware.sessions import SessionMiddleware # For session-based token storage
from starlette.responses import HTMLResponse
from starlette.routing import Route
from itsdangerous import URLSafeTimedSerializer # For token generation

SECRET_KEY = "your-super-secret-key" # CHANGE THIS IN PRODUCTION
serializer = URLSafeTimedSerializer(SECRET_KEY)

app = FastAPI()
app.add_middleware(SessionMiddleware, secret_key=SECRET_KEY) # Needed for session-based CSRF

def generate_csrf_token(request: Request):
    if "csrf_token" not in request.session:
        token = serializer.dumps(request.session.session_id) # Or a unique identifier
        request.session["csrf_token"] = token
    return request.session["csrf_token"]

def verify_csrf_token(request: Request):
    form_token = request.headers.get("X-CSRF-Token") # Common for API requests
    session_token = request.session.get("csrf_token")

    if not form_token or not session_token or form_token != session_token:
        # Try to load token from form data if not in headers (e.g., traditional forms)
        # This part would be more complex for actual form processing.
        try:
            # Attempt to deserialize to verify it's a valid token structure
            serializer.loads(form_token, max_age=3600) # Token valid for 1 hour
        except Exception:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Invalid CSRF token")
        
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="CSRF token mismatch")
    
    # If valid, return True or the token itself
    return True

@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request, csrf_token: str = Depends(generate_csrf_token)):
    return f"""
    <html>
        <head>
            <title>CSRF Demo</title>
            <script>
                function submitForm() {{
                    const form = document.getElementById('myform');
                    const formData = new FormData(form);
                    fetch('/change-password', {{
                        method: 'POST',
                        headers: {{
                            'X-CSRF-Token': document.getElementById('csrf_token').value,
                            'Content-Type': 'application/json' // Assuming JSON for API
                        }},
                        body: JSON.stringify({{ new_password: 'new_secret_password' }})
                    }})
                    .then(response => response.json())
                    .then(data => alert(JSON.stringify(data)))
                    .catch(error => console.error('Error:', error));
                }}
            </script>
        </head>
        <body>
            <h1>Change Password (CSRF Protected)</h1>
            <form id="myform">
                <input type="hidden" id="csrf_token" name="csrf_token" value="{csrf_token}">
                <label for="new_password">New Password:</label>
                <input type="password" id="new_password" name="new_password" value="secret123">
                <button type="button" onclick="submitForm()">Change Password</button>
            </form>
            <p>Check the console for CSRF token generation/verification logic.</p>
        </body>
    </html>
    """

class PasswordChange(BaseModel):
    new_password: str

@app.post("/change-password")
async def change_password(
    request: Request,
    password_change: PasswordChange,
    csrf_check: bool = Depends(verify_csrf_token) # Run CSRF check
):
    # If csrf_check didn't raise an exception, the token is valid
    # In a real app, update the user's password securely
    print(f"Password changed for session {request.session.get('session_id')} to {password_change.new_password}")
    return {"message": "Password changed successfully"}
