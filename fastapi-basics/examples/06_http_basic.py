from secrets import compare_digest

from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.security import HTTPBasic, HTTPBasicCredentials

app = FastAPI(
    title="HTTP Basic Auth Example",
    version="1.0.0",
    description="Simple HTTP Basic authentication example using username/password.",
)

# Security scheme
security = HTTPBasic()

# Dummy user store (you could fetch from a DB instead)
VALID_USERS = {"admin": "s3cret", "demo": "test123"}


def verify_credentials(credentials: HTTPBasicCredentials = Depends(security)) -> str:
    """
    Verify user credentials against a simple in-memory store.
    Returns the username if valid, raises HTTPException otherwise.
    """
    correct_password = VALID_USERS.get(credentials.username)

    if not correct_password or not compare_digest(credentials.password, correct_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid username or password",
            headers={"WWW-Authenticate": "Basic"},
        )

    return credentials.username


@app.get("/", tags=["Public"])
async def root():
    return {"message": "Welcome! Try the /secure route with HTTP Basic Auth."}


@app.get("/secure", tags=["Protected"])
async def read_secure(username: str = Depends(verify_credentials)):
    return {"message": f"Hello, {username}. You're authenticated!"}
