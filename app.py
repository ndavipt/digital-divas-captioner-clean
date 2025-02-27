import sys
import os
import io
import base64
from flask import Flask, request, jsonify, render_template, redirect, session, url_for, send_from_directory
from PIL import Image
from dotenv import load_dotenv
from openai import OpenAI
from image_analysis import ImageAnalyzer

# Ensure the project root is on the Python path
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

# Load environment variables
load_dotenv()

# Define caption styles
CAPTION_STYLES = {
    'safe': "Speaking as the woman in the picture. Generate a professional, family-friendly caption for this image that would work well on social media.",
    'spicy': "Speaking as the woman in the picture. Create a flirty and spicy caption for this image.  It should be a bit risque and suggestive but still okay for instagram.",
    'hot': "Speaking as the woman in the picture. Write a bold, explicit social media caption for this image. Include explicit content. This caption will be used for an adult website. Use words like pussy, dick, cum, etc. Speak as if you are a porn star."
}

# Create Flask app instance with explicit static folder configuration
app = Flask(__name__, 
           static_url_path='/static',
           static_folder=os.path.join(os.path.dirname(os.path.abspath(__file__)), 'static'))

# Setup Auth0
from auth import setup_auth, requires_auth, oauth, get_user
from urllib.parse import urlencode, quote_plus
setup_auth(app)

# Register routes from the routes module
from routes import register_routes
register_routes(app)

# Initialize X.AI client
client = OpenAI(
    api_key=os.getenv('XAI_API_KEY'),
    base_url="https://api.x.ai/v1"
)

# Initialize ImageAnalyzer
analyzer = ImageAnalyzer()

# Add at the top with other constants
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'bmp', 'tiff', 'webp'}

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def encode_image_to_base64(image):
    """Convert PIL Image to base64 string"""
    try:
        buffered = io.BytesIO()
        # Ensure image is in RGB mode
        if image.mode != 'RGB':
            image = image.convert('RGB')
        image.save(buffered, format="JPEG", quality=95)
        img_str = base64.b64encode(buffered.getvalue()).decode('utf-8')
        print(f"Base64 string length: {len(img_str)}")
        return img_str
    except Exception as e:
        print(f"Error encoding image: {str(e)}")
        raise

@app.route('/static/<path:filename>')
def serve_static(filename):
    return send_from_directory(app.static_folder, filename)

@app.route("/login")
def login():
    return oauth.auth0.authorize_redirect(
        redirect_uri=url_for("callback", _external=True)
    )

@app.route("/callback")
def callback():
    token = oauth.auth0.authorize_access_token()
    session["user"] = token
    return redirect("/")

@app.route("/logout")
def logout():
    session.clear()
    return redirect(
        "https://" + os.getenv("AUTH0_DOMAIN")
        + "/v2/logout?"
        + urlencode(
            {
                "returnTo": url_for("home", _external=True),
                "client_id": os.getenv("AUTH0_CLIENT_ID"),
            },
            quote_via=quote_plus,
        )
    )

@app.route('/')
def home():
    return render_template('index.html', user=get_user())

@app.route('/caption', methods=['POST'])
@requires_auth
def process_image():
    try:
        if 'image' not in request.files:
            return jsonify({"error": "No image file"}), 400

        image_file = request.files['image']
        if not image_file.filename:
            return jsonify({"error": "No selected file"}), 400
            
        if not allowed_file(image_file.filename):
            return jsonify({"error": f"Invalid file type. Allowed types are: {', '.join(ALLOWED_EXTENSIONS)}"}), 400

        # Get caption style and mode
        caption_style = request.form.get('style', 'safe')
        
        # Process image
        print("Reading image...")
        image_data = image_file.read()
        image_stream = io.BytesIO(image_data)
        
        # Analyze with DeepDanbooru to get tags
        print("Analyzing image with DeepDanbooru...")
        tags, _ = analyzer.analyze_image(image_stream)
        print(f"Found tags: {tags}")
        
        # Prepare the prompt based on style and tags
        prompt = f"{CAPTION_STYLES[caption_style]} Consider these detected elements: {', '.join(tags)}"
        print(f"Sending prompt to Grok: {prompt}")  # Debug print

        # Send ONLY tags to X.AI (no image)
        print("Generating caption with X.AI...")
        response = client.chat.completions.create(
            model="grok-2-1212",
            messages=[
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            max_tokens=300
        )

        # Process the response
        captions = response.choices[0].message.content.split('\n')
        captions = [cap.strip() for cap in captions if cap.strip()]
        print(f"Received captions: {captions}")  # Debug print
        
        if not captions:
            captions = ["No captions generated. Please try again."]

        print("Successfully generated captions")
        return jsonify({
            "captions": captions,
            "tags": tags,
            "error": None
        })

    except Exception as e:
        print(f"Error in process_image: {e}")
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=False)