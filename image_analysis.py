from PIL import Image
import deepdanbooru as dd
import numpy as np
import os
import openai
from dotenv import load_dotenv
import tensorflow as tf
import traceback

# Load environment variables from .env file
load_dotenv()

class ImageAnalyzer:
    def __init__(self):
        # Load DeepDanbooru Model & Tags
        self.model_path = "deepdanbooru_model"
        try:
            print(f"Loading model from path: {self.model_path}")
            print(f"Files in model directory: {os.listdir(self.model_path)}")
            self.model = dd.project.load_model_from_project(self.model_path, compile_model=False)
            print("Model loaded successfully")
            self.tags_list = dd.project.load_tags_from_project(self.model_path)
            print(f"Loaded {len(self.tags_list)} tags")
        except Exception as e:
            print(f"Error loading DeepDanbooru model: {e}")
            traceback.print_exc()
            raise

        # Initialize xAI Grok Client
        api_key = os.getenv("XAI_API_KEY")
        if not api_key:
            raise ValueError("XAI_API_KEY is missing in environment variables.")
        self.client = openai.OpenAI(
            api_key=api_key,
            base_url="https://api.x.ai/v1"
        )

    def analyze_image(self, image_input):
        """Analyze image and return both tags and caption"""
        try:
            print("Analyzing image with DeepDanbooru...")
            tags = self._describe_image(image_input)
            print(f"Found tags: {tags}")
            
            if tags:
                print("Generating caption from tags...")
                caption = self._generate_caption(tags)
                return tags, caption
            return [], None
        except Exception as e:
            print(f"Error in analyze_image: {e}")
            traceback.print_exc()
            raise

    def _describe_image(self, image_input):
        """Generate image tags using DeepDanbooru."""
        try:
            # Handle both file paths and BytesIO objects
            print("Opening image...")
            image = Image.open(image_input)
            print(f"Image format: {image.format}, size: {image.size}, mode: {image.mode}")
            image = image.convert("RGB").resize((512, 512))
            print("Converting to array...")
            image_array = np.array(image) / 255.0
            image_array = np.expand_dims(image_array, axis=0)
            print(f"Array shape: {image_array.shape}")

            print("Running model prediction...")
            predictions = self.model.predict(image_array)[0]
            print(f"Got {len(predictions)} predictions")
            threshold = 0.5
            return [self.tags_list[i] for i, score in enumerate(predictions) if score > threshold]
        except Exception as e:
            print(f"Error in _describe_image: {e}")
            traceback.print_exc()
            raise

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
            raise

# Test code
if __name__ == "__main__":
    analyzer = ImageAnalyzer()
    test_image_path = "path/to/test/image.jpg"
    tags, caption = analyzer.analyze_image(test_image_path)
    print(f"Tags: {tags}")
    print(f"Caption: {caption}") 