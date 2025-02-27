#!/bin/bash
set -e

echo "Starting build process..."

# Create necessary directories
mkdir -p deepdanbooru_model
mkdir -p static

# Copy static files
echo "Setting up static files..."
cat > static/styles.css << 'EOL'
/* CSS Variables */
:root {
  --color-background: #f8f5f1;
  --color-background-secondary: #f9f6f0;
  --color-primary: #4a3524;
  --color-secondary: #665544;
  --color-accent: #b39b7d;
  --color-accent-hover: #a08c6e;
  --color-dashed-border: #ccc;
  --color-bullet: #997755;
  --color-border-secondary: #e0d5c7;
  --color-button-disabled: #ccc;
  --box-shadow-color: rgba(0, 0, 0, 0.1);
  --box-shadow-hover: rgba(0, 0, 0, 0.2);
  --space-xs: 4px;
  --space-sm: 10px;
  --space-md: 20px;
  --space-lg: 30px;
  --space-xl: 40px;
  --font-size-base: 16px;
  --font-size-sm: 14px;
  --font-size-lg: 18px;
  --font-size-xl: 24px;
}

/* Global Styles */
* {
  box-sizing: border-box;
}

body {
  font-family: Arial, sans-serif;
  margin: 0;
  padding: var(--space-md);
  background-color: var(--color-background);
  font-size: var(--font-size-base);
  line-height: 1.5;
  color: var(--color-secondary);
}

.container {
  max-width: 800px;
  margin: 0 auto;
  background-color: #fff;
  padding: var(--space-lg);
  border-radius: 8px;
  box-shadow: 0 2px 4px var(--box-shadow-color);
  position: relative;
}

/* Headers */
h1, h2 {
  color: var(--color-primary);
  margin-bottom: var(--space-md);
}

h1 {
  text-align: center;
  border-bottom: 1px solid var(--color-border-secondary);
  padding-bottom: var(--space-sm);
}

/* Upload Area */
.upload-area {
  border: 2px dashed var(--color-dashed-border);
  border-radius: 8px;
  padding: var(--space-xl);
  text-align: center;
  margin: var(--space-md) 0;
  cursor: pointer;
  background-color: var(--color-background-secondary);
  transition: background-color 0.3s ease;
}

.upload-area:hover {
  background-color: #f0ede6;
}

.upload-area.dragover {
  background-color: #eee;
}

/* Image Preview */
#preview {
  max-width: 400px;
  width: 100%;
  height: auto;
  margin: var(--space-md) auto;
  border-radius: 8px;
  display: none;
}

/* Style Toggle */
.style-selector {
  background-color: var(--color-background-secondary);
  padding: var(--space-md);
  border-radius: 6px;
  margin: var(--space-lg) 0;
}

.style-toggle {
  display: flex;
  background: #fff;
  padding: var(--space-xs);
  border-radius: 8px;
  position: relative;
  height: 60px;
  justify-content: space-between;
  align-items: center;
}

.style-toggle button {
  flex: 1;
  margin: 0;
  background: transparent;
  color: var(--color-secondary);
  position: relative;
  z-index: 1;
}

/* Buttons */
button {
  padding: 15px;
  background-color: var(--color-accent);
  color: #fff;
  border: none;
  border-radius: 6px;
  cursor: pointer;
  font-size: var(--font-size-base);
  margin: var(--space-md) 0;
  transition: background-color 0.3s ease;
}

button:hover:not(:disabled) {
  background-color: var(--color-accent-hover);
}

button:disabled {
  background-color: var(--color-button-disabled);
  cursor: not-allowed;
}

/* Response Area */
#response {
  background-color: var(--color-background-secondary);
  padding: var(--space-md);
  border-radius: 6px;
  margin: var(--space-md) 0;
  white-space: pre-wrap;
  min-height: 60px;
}

/* Mobile Responsiveness */
@media (max-width: 600px) {
  .container {
    padding: var(--space-md);
  }
  
  .upload-area {
    padding: var(--space-md);
  }
  
  button {
    font-size: var(--font-size-sm);
    padding: 12px;
  }
  
  #preview {
    max-width: 100%;
  }
}
EOL

# Download pre-trained model files
echo "Downloading model files..."
curl -L -o deepdanbooru_model/model-resnet_custom_v3.h5 https://github.com/KichangKim/DeepDanbooru/releases/download/v3-20211112-sgd-e28/model-resnet_custom_v3.h5
curl -L -o deepdanbooru_model/tags.txt https://github.com/KichangKim/DeepDanbooru/releases/download/v3-20211112-sgd-e28/tags.txt

echo "Build process complete!"