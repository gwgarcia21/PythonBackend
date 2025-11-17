from fastapi import FastAPI, Depends, HTTPException, status

app = FastAPI()

# Dummy role database
roles = {
    "administrator": ["create_post", "read_post", "update_post", "delete_post"],
    "editor": ["create_post", "read_post", "update_post"],
    "author": ["create_post", "read_post"],
    "reader": ["read_post"],
}

# Dummy user role assignments
user_roles = {
    "john": "administrator",
    "jane": "editor",
    "mike": "author",
    "susan": "reader",
}

# Dependency to get the current user's role
async def get_user_role(username: str): # In real application get username from token
    role = user_roles.get(username)
    if not role:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="User has no role assigned")
    return role

# Dependency to check for a specific permission
def permission_check(permission: str):
    async def check_permission(role: str = Depends(get_user_role)):
        permissions = roles.get(role)
        if not permissions or permission not in permissions:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN, detail="Insufficient permissions"
            )
    return check_permission

# Example endpoints
@app.post("/posts", dependencies=[Depends(permission_check("create_post"))])
async def create_post():
    return {"message": "Post created"}

@app.get("/posts/{post_id}", dependencies=[Depends(permission_check("read_post"))])
async def read_post(post_id: int):
    return {"message": f"Post {post_id} read"}

@app.put("/posts/{post_id}", dependencies=[Depends(permission_check("update_post"))])
async def update_post(post_id: int):
    return {"message": f"Post {post_id} updated"}

@app.delete("/posts/{post_id}", dependencies=[Depends(permission_check("delete_post"))])
async def delete_post(post_id: int):
    return {"message": f"Post {post_id} deleted"}
