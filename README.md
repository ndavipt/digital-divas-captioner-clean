# Digital Divas Image Captioner

A powerful, mobile-friendly web application that generates AI-powered social media captions for your images. Built with Flask and powered by X.AI, this application analyzes your images and creates engaging captions tailored to your chosen style.

## 🌟 Features

- Mobile-responsive design for seamless use on any device
- Drag-and-drop image upload functionality
- Three caption styles:
  - 🛡️ Safe: Professional and family-friendly
  - 💝 Spicy: Flirty and playful
  - 🔥 Hot: Bold and seductive
- AI-powered image analysis using DeepDanbooru
- Advanced caption generation with X.AI
- Secure authentication with Auth0
- Real-time preview and processing
- Rate limiting for API protection
- File size and format validation

## 🚀 Getting Started

### Prerequisites

- Python 3.10 or higher
- X.AI API key
- Auth0 account
- Git (for cloning the repository)

### Installation

1. Clone the repository:
```bash
git clone https://github.com/your-username/digital-divas-captioner.git
cd digital-divas-captioner
```

2. Create and activate a virtual environment:
```bash
# On Windows
python -m venv venv
venv\Scripts\activate

# On macOS/Linux
python -m venv venv
source venv/bin/activate
```

3. Install required packages:
```bash
pip install -r requirements.txt
```

4. Create a .env file in the root directory with all required credentials:
```env
AUTH0_DOMAIN=your-auth0-domain
AUTH0_CLIENT_ID=your-auth0-client-id
AUTH0_CLIENT_SECRET=your-auth0-client-secret
APP_SECRET_KEY=your-app-secret-key
AUTH0_AUDIENCE=your-auth0-audience
OPENAI_API_KEY=your-openai-api-key
XAI_API_KEY=your_xai_api_key_here
```

5. Run the application:
```bash
python app.py
```

The application will be available at `http://localhost:5000`

### Docker Deployment

Build and run with Docker:

```bash
docker build -t digital-divas-captioner .
docker run -p 5000:10000 -e PORT=10000 digital-divas-captioner
```

### Deploying to Render

1. Fork/push this repository to your GitHub account
2. Create a new Web Service on Render
3. Connect to your GitHub repository
4. Select "Docker" as the Environment
5. Add all environment variables in the Render dashboard
6. Deploy the service

The deployment is configured via the render.yaml file.

## 💻 Usage

1. Open your web browser and navigate to `http://localhost:5000`
2. Log in using Auth0 authentication
3. Upload an image by either:
   - Dragging and dropping it into the upload area
   - Clicking the upload area to select a file
4. Select your desired caption style (Safe, Spicy, or Hot)
5. Click "Generate Captions"
6. Copy your generated captions and use them for your social media posts

## 📱 Mobile Features

- Responsive design that adapts to any screen size
- Touch-optimized interface
- Efficient image upload on mobile devices
- Smooth transitions and animations
- Mobile-friendly button sizes and spacing

## 🔒 Auth0 Configuration

1. Create an Auth0 application (Regular Web Application)
2. Configure the following URLs in Auth0:
   - Allowed Callback URLs: `https://your-render-app.onrender.com/callback, http://localhost:5000/callback`
   - Allowed Logout URLs: `https://your-render-app.onrender.com, http://localhost:5000`
   - Allowed Web Origins: `https://your-render-app.onrender.com, http://localhost:5000`
3. Note your Auth0 Domain, Client ID, Client Secret, and Audience for your .env file

## 🛠️ Technical Stack

- **Backend**: Flask (Python)
- **Image Analysis**: DeepDanbooru
- **Caption Generation**: X.AI API
- **Frontend**: HTML5, CSS3, JavaScript
- **Authentication**: Auth0
- **Deployment**: Docker, Render
- **Mobile Optimization**: Responsive CSS, Touch Events

## 📋 Requirements

See `requirements.txt` for a complete list of Python dependencies.

## ⚙️ Configuration

The application can be configured through environment variables:
- `AUTH0_DOMAIN`: Your Auth0 domain
- `AUTH0_CLIENT_ID`: Your Auth0 client ID
- `AUTH0_CLIENT_SECRET`: Your Auth0 client secret
- `APP_SECRET_KEY`: Secret key for Flask session encryption
- `AUTH0_AUDIENCE`: Your Auth0 audience
- `OPENAI_API_KEY`: Your OpenAI API key
- `XAI_API_KEY`: Your X.AI API key
- `PORT`: Custom port number (default: 5000)

## 🤝 Contributing

Contributions are welcome! To contribute:

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 👏 Acknowledgments

- X.AI for providing the caption generation API
- DeepDanbooru for image analysis capabilities
- Auth0 for authentication services
- Flask team for the amazing web framework
- All contributors and users of this project

## 📞 Support

For support, please:
- Open an issue in the GitHub repository
- Check existing issues for similar problems
- Provide detailed information about your setup and the issue

---

Made with ❤️ by Digital Divas