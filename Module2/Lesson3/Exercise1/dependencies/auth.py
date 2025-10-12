from fastapi import HTTPException, status


async def verify_token(x_token: str):
    """
    Verifies the validity of a token passed in the request headers.
    Raises an HTTP exception if the token is invalid.
    """
    if x_token != "valid_token":
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid X-Token header"
        )
