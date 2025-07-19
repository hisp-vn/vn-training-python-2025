# OAuth 2.1 CLI Demo for DHIS2

This is a simple Python script demonstrating the OAuth 2.1 authorization code flow with PKCE using a CLI script. It ties into the DHIS2 OAuth features configured in `AuthorizationServerConfig.java` (using Spring Authorization Server).

## Setup

1. Ensure you have UV installed (Python dependency manager).
2. Copy `.env.example` to `.env` and fill in the values:
   - `SERVER_BASE_URL`: Your DHIS2 server URL (e.g., http://localhost:8080).
   - `CLIENT_ID` and `CLIENT_SECRET`: From a registered OAuth client in DHIS2.
   - `SCOPE`: Scopes like 'openid email'.
   - `REDIRECT_URI`: Local URI (e.g., http://localhost:8000) registered in the client.
   - `API_ENDPOINT`: A protected endpoint (e.g., /api/users/me).
3. Install dependencies: Run `uv sync` in this directory.

## Running the Demo

1. Run the script: `uv run oauth_demo.py`.
2. It will open your browser to the login page. Authenticate with your DHIS2 credentials.
3. After redirect, the script captures the code, exchanges it for tokens, displays them, and makes a sample API request.

## Assumptions
- You have a DHIS2 instance with OAuth 2.1 enabled (as per `AuthorizationServerConfig.java`).
- A confidential client is registered with the redirect URI.
- PKCE is supported (optional but added for security).
- The API endpoint requires Bearer token auth and returns JSON.

## Notes
- This is for demo purposes; in production, handle tokens securely.
- If issues, ensure the redirect URI is allowed and ports are free.
