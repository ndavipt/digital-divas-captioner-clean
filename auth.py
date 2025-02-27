from functools import wraps
from flask import redirect, session, url_for, request, jsonify
from os import environ as env
from authlib.integrations.flask_client import OAuth
from urllib.parse import urlencode, quote_plus

oauth = OAuth()

def setup_auth(app):
    # Auth0 configuration
    app.secret_key = env.get("APP_SECRET_KEY")
    oauth.init_app(app)
    
    domain = env.get("AUTH0_DOMAIN")
    oauth.register(
    "auth0",
    client_id=env.get("AUTH0_CLIENT_ID"),
    client_secret=env.get("AUTH0_CLIENT_SECRET"),
    api_base_url=f"https://{env.get('AUTH0_DOMAIN')}",
    access_token_url=f"https://{env.get('AUTH0_DOMAIN')}/oauth/token",
    authorize_url=f"https://{env.get('AUTH0_DOMAIN')}/authorize",
    client_kwargs={
        "scope": "openid profile email",
        "audience": f"https://{env.get('AUTH0_DOMAIN')}/api/v2/"  
    },
    jwks_uri=f"https://{env.get('AUTH0_DOMAIN')}/.well-known/jwks.json"  
)






def requires_auth(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if 'user' not in session:
            if request.is_json:
                return jsonify({"error": "Authentication required"}), 401
            return redirect('/login')
        return f(*args, **kwargs)
    return decorated

def get_user():
    return session.get('user')