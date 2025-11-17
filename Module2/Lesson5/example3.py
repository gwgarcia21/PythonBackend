# This is a conceptual example, actual ORM integration is more involved (e.g., SQLAlchemy)
# This lesson does not cover full ORM setup, as Module 3 covers Database Management and Integration.

async def get_user_by_username(username: str):
    # Using a conceptual ORM-like interaction
    # The ORM handles parameterization, preventing injection
    # e.g., db.query(User).filter(User.username == username).first()
    print(f"Safely querying for user: {username}")
    # This is SAFE because the ORM uses parameters, not string concatenation.
    if username == "admin":
        return {"username": "admin", "role": "admin"}
    return {"username": username, "role": "user"}

@app.get("/users/search/")
async def search_users(username: str):
    user_data = await get_user_by_username(username)
    return user_data