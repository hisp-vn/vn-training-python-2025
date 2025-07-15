from fastapi import Depends, FastAPI, HTTPException, Security, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

app = FastAPI(
    title="HTTP Bearer Auth Example",
    version="1.0.0",
    description="Example using HTTP Bearer token in Authorization header.",
)

# Define the bearer scheme (no auto_error so we can return custom messages)
bearer_scheme = HTTPBearer(auto_error=False)

# Dummy valid token (usually you'd check this against a database or JWT)
VALID_TOKENS = {"mysecrettoken", "another-valid-token"}


def verify_bearer_token(credentials: HTTPAuthorizationCredentials = Security(bearer_scheme)) -> str:
    if not credentials or credentials.scheme.lower() != "bearer":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Authorization token missing or wrong scheme",
        )

    token = credentials.credentials

    if token not in VALID_TOKENS:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Invalid token",
        )

    return token


@app.get("/", tags=["Public"])
async def root():
    return {"message": "Welcome! Try the /secure endpoint with Bearer token."}


@app.get("/secure", tags=["Protected"])
async def read_secure(token: str = Depends(verify_bearer_token)):
    return {"message": "Access granted with token", "token_used": token}
