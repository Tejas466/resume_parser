from flask import Flask, redirect, url_for, session
from authlib.integrations.flask_client import OAuth
import os

app = Flask(__name__)
app.secret_key = os.urandom(24)  # Use a secure random key in production

# AWS Cognito Configuration
COGNITO_REGION = "eu-north-1" 
COGNITO_USERPOOL_ID = "eu-north-1_ZqANJU6FG"
COGNITO_CLIENT_ID = "7balkab8b8mjpr0kh8a6gsfo"
COGNITO_CLIENT_SECRET = "1v2u0p54a8v96hmlqggtgvcetom7din6aqa2lckrcubv6mumaio3"

oauth = OAuth(app)

oauth.register(
    name="oidc",
    authority=f"https://cognito-idp.{COGNITO_REGION}.amazonaws.com/{COGNITO_USERPOOL_ID}",
    client_id=COGNITO_CLIENT_ID,
    client_secret=COGNITO_CLIENT_SECRET,
    server_metadata_url=f"https://cognito-idp.{COGNITO_REGION}.amazonaws.com/{COGNITO_USERPOOL_ID}/.well-known/openid-configuration",
    client_kwargs={"scope": "openid email profile"}
)

@app.route("/")
def index():
    user = session.get("user")
    if user:
        return f"Hello, {user['email']}. <a href='/logout'>Logout</a>"
    else:
        return "Welcome! Please <a href='/login'>Login</a>."

@app.route("/login")
def login():
    return oauth.oidc.authorize_redirect(url_for("authorize", _external=True))

@app.route("/authorize")
def authorize():
    token = oauth.oidc.authorize_access_token()
    user = token.get("userinfo")
    session["user"] = user  # Store user session after authentication
    return redirect(url_for("index"))

@app.route("/logout")
def logout():
    session.pop("user", None)
    return redirect(url_for("index"))

if __name__ == "__main__":
    app.run(debug=True)
