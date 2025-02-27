from PIL import Image
import deepdanbooru as dd
import numpy as np
import os
import sys

def main():
    print("Testing DeepDanbooru")
    model_path = "deepdanbooru_model"
    print(f"Using model path: {model_path}")
    print(f"Files in directory: {os.listdir(model_path)}")
    
    try:
        print("Loading model...")
        model = dd.project.load_model_from_project(model_path, compile_model=False)
        print("Model loaded successfully")
        
        tags = dd.project.load_tags_from_project(model_path)
        print(f"Loaded {len(tags)} tags")
        print("DeepDanbooru test passed\!")
        return 0
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()
        return 1

if __name__ == "__main__":
    sys.exit(main())
