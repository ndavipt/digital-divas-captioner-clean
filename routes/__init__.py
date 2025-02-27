# Import routes modules here
from routes.upload import upload_bp

# Function to register all blueprints to Flask app
def register_routes(app):
    app.register_blueprint(upload_bp)