from flask import Blueprint, request, jsonify
from image_analysis import ImageAnalyzer
from io import BytesIO

upload_bp = Blueprint('upload', __name__)
analyzer = ImageAnalyzer()

@upload_bp.route("/upload", methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({"error": "No file part"}), 400
        
    file = request.files['file']
    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400
    
    # Read file into memory
    contents = file.read()
    image_stream = BytesIO(contents)
    
    # Analyze the image directly from memory
    tags, caption = analyzer.analyze_image(image_stream)
    
    return jsonify({
        "filename": file.filename,
        "tags": tags,
        "caption": caption
    })