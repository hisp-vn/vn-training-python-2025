import os
import webbrowser
import http.server
import urllib.parse
import secrets
import hashlib
import base64
import requests
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Retrieve config from .env
SERVER_BASE_URL = os.getenv("SERVER_BASE_URL")
CLIENT_ID = os.getenv("CLIENT_ID")
CLIENT_SECRET = os.getenv("CLIENT_SECRET")
SCOPE = os.getenv("SCOPE")
REDIRECT_URI = os.getenv("REDIRECT_URI")
API_ENDPOINT = os.getenv("API_ENDPOINT")

# Construct full endpoints
AUTH_URL = f"{SERVER_BASE_URL}/oauth2/authorize"
TOKEN_URL = f"{SERVER_BASE_URL}/oauth2/token"
FULL_API_URL = f"{SERVER_BASE_URL}{API_ENDPOINT}"

# Generate PKCE values
code_verifier = secrets.token_urlsafe(96)
code_challenge = (
    base64.urlsafe_b64encode(hashlib.sha256(code_verifier.encode("ascii")).digest())
    .decode("ascii")
    .rstrip("=")
)

# Generate state for security
state = secrets.token_urlsafe(16)

# Build authorization URL
auth_params = {
    "client_id": CLIENT_ID,
    "response_type": "code",
    "redirect_uri": REDIRECT_URI,
    "scope": SCOPE,
    "state": state,
    "code_challenge": code_challenge,
    "code_challenge_method": "S256",
}
auth_url = f"{AUTH_URL}?{urllib.parse.urlencode(auth_params)}"

print("Unencoded auth params:", auth_params)
print("Full encoded auth URL:", auth_url)
print("Opening browser for authentication...")
#webbrowser.open(auth_url)


# Local server to capture redirect
class RedirectHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        query = urllib.parse.urlparse(self.path).query
        params = urllib.parse.parse_qs(query)
        self.server.auth_code = params.get("code", [None])[0]
        self.server.received_state = params.get("state", [None])[0]
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()
        self.wfile.write(b"Authentication successful! You can close this window.")
        print("Auth code received. Closing server...")


# Start local server
server_address = (
    urllib.parse.urlparse(REDIRECT_URI).hostname,
    urllib.parse.urlparse(REDIRECT_URI).port,
)
httpd = http.server.HTTPServer(server_address, RedirectHandler)
httpd.auth_code = None
httpd.received_state = None
print(f"Starting local server at {REDIRECT_URI} to capture redirect...")
httpd.handle_request()  # Handle one request (the redirect)

# Verify state
if httpd.received_state != state:
    raise ValueError("State mismatch! Possible CSRF attack.")

auth_code = httpd.auth_code
if not auth_code:
    raise ValueError("No authorization code received.")

# Exchange code for tokens
token_data = {
    "grant_type": "authorization_code",
    "code": auth_code,
    "redirect_uri": REDIRECT_URI,
    "client_id": CLIENT_ID,
    "client_secret": CLIENT_SECRET,
    "code_verifier": code_verifier,
}
token_response = requests.post(TOKEN_URL, data=token_data)
token_response.raise_for_status()
tokens = token_response.json()

access_token = tokens.get("access_token")
refresh_token = tokens.get("refresh_token")

print("\nAccess Token:", access_token)
print("Refresh Token:", refresh_token)

# Make a sample API request
headers = {"Authorization": f"Bearer {access_token}"}
api_response = requests.get(FULL_API_URL, headers=headers)
print("\nAPI Response Status:", api_response.status_code)
print("API Response Headers:", api_response.headers)
try:
    print("API Response Body:", api_response.json())
except requests.exceptions.JSONDecodeError:
    print("API Response Body (non-JSON):", api_response.text)
if not api_response.ok:
    print("Warning: API request failed, but continuing for demo purposes.")
