import bleach # pip install bleach

# ... (previous FastAPI app and models) ...

class Comment(BaseModel):
    text: str

@app.post("/comments/")
async def post_comment(comment: Comment):
    # Sanitize HTML from the comment text to prevent XSS
    # allowed_tags can be customized based on your requirements
    clean_text = bleach.clean(comment.text, tags=[], strip=True)
    # In a real app, store clean_text in the database
    return {"message": "Comment posted", "clean_text": clean_text}