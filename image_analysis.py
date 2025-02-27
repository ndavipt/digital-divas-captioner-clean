from PIL import Image
import numpy as np
import os
import openai
import base64
import io
from dotenv import load_dotenv
import traceback
import time

# Load environment variables from .env file
load_dotenv()

class ImageAnalyzer:
    def __init__(self):
        # Initialize OpenAI client for vision analysis
        openai_api_key = os.getenv("OPENAI_API_KEY")
        if not openai_api_key:
            raise ValueError("OPENAI_API_KEY is missing in environment variables.")
        self.openai_client = openai.OpenAI(api_key=openai_api_key)
        
        # Initialize X.AI client for caption generation
        xai_api_key = os.getenv("XAI_API_KEY")
        if not xai_api_key:
            raise ValueError("XAI_API_KEY is missing in environment variables.")
        self.xai_client = openai.OpenAI(
            api_key=xai_api_key,
            base_url="https://api.x.ai/v1"
        )
        print("ImageAnalyzer initialized with OpenAI vision and X.AI client")

    def _encode_image(self, image_file):
        """Convert image to base64 for OpenAI API"""
        image = Image.open(image_file)
        # Convert to RGB if needed
        if image.mode != "RGB":
            image = image.convert("RGB")
        buffered = io.BytesIO()
        image.save(buffered, format="JPEG")
        return base64.b64encode(buffered.getvalue()).decode('utf-8')

    def analyze_image(self, image_input):
        """Analyze image using OpenAI's Vision model"""
        try:
            print("Analyzing image with OpenAI Vision...")
            # Reset the file pointer if it's a BytesIO object
            if isinstance(image_input, io.BytesIO):
                image_input.seek(0)
            
            # Encode image to base64
            base64_image = self._encode_image(image_input)
            
            # Analyze with OpenAI Vision
            response = self.openai_client.chat.completions.create(
                model="gpt-4-vision-preview",
                messages=[
                    {
                        "role": "user",
                        "content": [
                            {"type": "text", "text": "Identify key elements and features in this image, focusing on visual descriptors, styles, colors, and subjects. Create at least 10 specific, accurate tags that someone could use to find this image. Format your response as a comma-separated list of tags only."},
                            {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{base64_image}"}}
                        ]
                    }
                ],
                max_tokens=300
            )
            
            # Get tags from response
            tags_text = response.choices[0].message.content
            tags = [tag.strip() for tag in tags_text.split(',')]
            print(f"Generated tags: {tags}")
            
            # Generate caption
            caption = self._generate_caption(tags)
            return tags, caption
        except Exception as e:
            print(f"Error in analyze_image: {e}")
            traceback.print_exc()
            return ["error analyzing image"], "Could not analyze image"

    def _generate_caption(self, tags):
        """Generate caption using X.AI Grok based on tags."""
        try:
            # Only send text tags to Grok with a more detailed prompt
            prompt = f"""Based on these image tags: {', '.join(tags)}, create a descriptive, factual caption.
            Focus on describing what is actually visible in the image.
            Be detailed about the scene, setting, and subjects.
            Keep it neutral - I'll add stylistic elements later."""
            
            response = self.xai_client.chat.completions.create(
                model="grok-2-1212",
                messages=[{"role": "user", "content": prompt}],
                max_tokens=150
            )
            return response.choices[0].message.content.strip()
        except Exception as e:
            print(f"Error in _generate_caption: {e}")
            traceback.print_exc()
            return "A beautiful photo that captures a special moment."