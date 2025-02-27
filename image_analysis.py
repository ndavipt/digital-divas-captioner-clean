from PIL import Image
import numpy as np
import os
import openai
from dotenv import load_dotenv
import traceback
import time

# Load environment variables from .env file
load_dotenv()

class ImageAnalyzer:
    def __init__(self):
        # Initialize xAI Grok Client
        api_key = os.getenv("XAI_API_KEY")
        if not api_key:
            raise ValueError("XAI_API_KEY is missing in environment variables.")
        self.client = openai.OpenAI(
            api_key=api_key,
            base_url="https://api.x.ai/v1"
        )
        print("ImageAnalyzer initialized with X.AI client only (no DeepDanbooru)")

    def analyze_image(self, image_input):
        """Analyze image and return basic tags (without DeepDanbooru)"""
        try:
            # For now, use basic predetermined tags
            basic_tags = ["woman", "photo", "portrait", "beautiful", "social media"]
            
            print(f"Using basic tags: {basic_tags}")
            caption = self._generate_caption(basic_tags)
            return basic_tags, caption
        except Exception as e:
            print(f"Error in analyze_image: {e}")
            traceback.print_exc()
            return ["photo"], "A wonderful photo."

    def _generate_caption(self, tags):
        """Generate caption using xAI Grok based on tags."""
        try:
            # Only send text tags to Grok, not the image
            prompt = f"Based on these image tags: {', '.join(tags)}, create a descriptive caption."
            response = self.client.chat.completions.create(
                model="grok-2-1212",
                messages=[{"role": "user", "content": prompt}],
                max_tokens=150
            )
            return response.choices[0].message.content.strip()
        except Exception as e:
            print(f"Error in _generate_caption: {e}")
            traceback.print_exc()
            return "A beautiful photo that captures a special moment."