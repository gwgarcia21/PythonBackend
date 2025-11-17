from fastapi.responses import HTMLResponse
import html # Python's built-in HTML escaping module

@app.get("/greet/{name}", response_class=HTMLResponse)
async def greet(name: str):
    # If 'name' could contain malicious scripts, manually escape it
    escaped_name = html.escape(name)
    return f"""
    <html>
        <head>
            <title>Greeting</title>
        </head>
        <body>
            <h1>Hello, {escaped_name}!</h1>
        </body>
    </html>
    """

@app.get("/display_comment/", response_class=HTMLResponse)
async def display_comment(user_comment: str = "No comment"):
    # Imagine user_comment came from a database where it was stored (and hopefully sanitized)
    # Always re-escape for output, especially if you're unsure about storage sanitization
    encoded_comment = html.escape(user_comment)
    return f"""
    <html>
        <head>
            <title>Comment Display</title>
        </head>
        <body>
            <p>User says: {encoded_comment}</p>
        </body>
    </html>
    """