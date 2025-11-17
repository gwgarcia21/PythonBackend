""" 1. Implement a system where users can have multiple roles.
    2. Create a new permission, such as edit_profile, and add it to one of the roles.
    3. Create an endpoint that requires the edit_profile permission."""

from fastapi import FastAPI, Depends, HTTPException, status

app = FastAPI()

# Dummy role database
roles = {
    "administrator": ["create_post", "read_post", "update_post", "delete_post", "create_video"],
    "editor": ["create_post", "read_post", "update_post"],
    "author": ["create_post", "read_post"],
    "reader": ["read_post"],
    "video_editor": ["create_video"]
}

# Dummy user role assignments
user_roles = {
    "john": ["administrator"],
    "jane": ["editor", "video_editor"],
    "mike": ["author"],
    "susan": ["reader"],
}

# Dependency to get the current user's roles
async def get_user_roles(username: str): # In real application get username from token
    current_user_roles = user_roles.get(username)
    if not current_user_roles:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="User has no role assigned")
    return current_user_roles

# Dependency to check for a specific permission
def permission_check(permission: str):
    async def check_permission(current_user_roles: str = Depends(get_user_roles)):
        success = False
        for role in current_user_roles:
            permissions = roles.get(role)
            if not permissions or permission not in permissions:
                continue
            success = True
        if not success:
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

@app.post("/videos", dependencies=[Depends(permission_check("create_video"))])
async def create_video():
    return {"message": "Video created"}