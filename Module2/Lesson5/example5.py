from fastapi.responses import Response

@app.get("/secure_page")
async def secure_page():
    content = """
    <html>
        <head>
            <title>Secure Page</title>
        </head>
        <body>
            <h1>This page has a CSP!</h1>
            <script>
                // This script will be allowed if 'self' is in script-src
                console.log("Internal script executed.");
            </script>
            <!-- <script src="http://malicious.com/evil.js"></script> This would be blocked by CSP -->
        </body>
    </html>
    """
    response = HTMLResponse(content)
    # Example CSP: Allows scripts only from the same origin ('self') and google-analytics.com
    # This prevents external, untrusted scripts from running.
    response.headers["Content-Security-Policy"] = "default-src 'self'; script-src 'self' https://www.google-analytics.com; style-src 'self';"
    return response