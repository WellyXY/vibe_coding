# Vibe Coding - AI-Powered Dating Discovery App

An intelligent dating recommendation system powered by Gemini AI, featuring an interactive agent and swipeable card interface.

![Python](https://img.shields.io/badge/Python-3.9+-blue.svg)
![Flask](https://img.shields.io/badge/Flask-2.3+-green.svg)
![License](https://img.shields.io/badge/license-MIT-blue.svg)

**🌐 Live Demo**: [https://vibe-coding-one-pink.vercel.app](https://vibe-coding-one-pink.vercel.app)

## 📋 Table of Contents

- [Features](#-features)
- [Architecture](#-architecture)
- [Quick Start](#-quick-start)
- [Project Structure](#-project-structure)
- [Deployment](#-deployment)
- [API Documentation](#-api-documentation)
- [Development](#-development)
- [Troubleshooting](#-troubleshooting)

## 🌟 Features

- **AI-Powered Recommendations**: Uses Google Gemini AI to intelligently rank and recommend users
- **Interactive Agent**: Conversational UI that asks personalized questions
- **Swipeable Cards**: Tinder-like card interface with smooth animations
- **Dynamic Questions**: AI-generated questions based on user preferences
- **Beautiful Avatars**: Mix of real photos and anime-style character avatars
- **RESTful API**: Clean API for easy integration
- **Production Ready**: Deployed on Vercel (frontend) + Railway (backend)

## 🏗️ Architecture

This is a **full-stack application** with separated frontend and backend:

```
┌─────────────────┐         ┌─────────────────┐
│   Vercel        │         │    Railway      │
│   (Frontend)    │ ─API──> │   (Backend)     │
│                 │         │                 │
│  - index.html   │         │  - Flask API    │
│  - app.js       │         │  - Gemini AI    │
│  - config.js    │         │  - Python Logic │
└─────────────────┘         └─────────────────┘
```

**Frontend (Vercel)**:
- Static files: HTML, CSS, JavaScript
- Dynamic API configuration
- URL: https://vibe-coding-one-pink.vercel.app

**Backend (Railway)**:
- Flask API server
- Gemini AI integration
- User database
- URL: https://vibe-coding-production-cdb4.up.railway.app

## 🚀 Quick Start

### Option 1: Use the Live Demo

Simply visit: **[https://vibe-coding-one-pink.vercel.app](https://vibe-coding-one-pink.vercel.app)**

### Option 2: Run Locally

#### Prerequisites

- Python 3.9 or higher
- pip (Python package manager)
- A Gemini API key ([Get one here](https://makersuite.google.com/app/apikey))

#### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/WellyXY/vibe_coding.git
   cd vibe_coding
   ```

2. **Install Python dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Configure environment variables**
   ```bash
   cp .env.example .env
   # Edit .env and add your Gemini API key:
   # GEMINI_API_KEY=your_api_key_here
   ```

4. **Start the backend server**
   ```bash
   python app.py
   ```
   Server will run on `http://localhost:5000`

5. **Open the frontend**
   - Simply open `index.html` in your browser
   - Or use a local server:
     ```bash
     python -m http.server 8000
     ```
   - Visit: `http://localhost:8000`

## 📁 Project Structure

```
vibe_coding/
├── 📄 Core Application Files
│   ├── index.html                  # Main web interface
│   ├── discover.html               # Alternative discovery page
│   ├── app.js                      # Frontend card stack logic
│   ├── styles.css                  # Styling
│   ├── config.js                   # API configuration (dev/prod)
│   └── vercel.json                 # Vercel deployment config
│
├── 🐍 Backend (Python)
│   ├── app.py                      # Flask API server
│   ├── recommendation_system.py    # AI recommendation engine
│   ├── gemini_client.py           # Gemini API client
│   ├── users_database.json        # User data (100 users)
│   ├── requirements.txt           # Python dependencies
│   └── Procfile                   # Railway deployment config
│
├── 🖼️ Assets
│   ├── avatars/                   # User avatar images (100)
│   │   ├── avatar_001-070.jpg    # Real photos
│   │   └── avatar_071-100.png    # Anime characters
│   └── assets/                    # UI icons and images
│
├── 🛠️ Development Scripts
│   └── scripts/
│       ├── generate_users.py          # Generate user database
│       ├── download_avatars.py        # Download avatar images
│       ├── interactive_recommend.py   # CLI recommendation tool
│       └── test_api.py               # API testing
│
├── 📚 Documentation
│   └── docs/
│       ├── DEPLOYMENT_GUIDE.md        # Complete deployment guide
│       ├── RAILWAY_DEPLOYMENT.md      # Railway-specific setup
│       ├── GEMINI_README.md          # Gemini AI integration
│       ├── RECOMMENDATION_README.md   # Recommendation system docs
│       └── test-connection.html       # API connection tester
│
└── 📝 Configuration
    ├── .env.example               # Environment variables template
    ├── .gitignore                # Git ignore rules
    └── README.md                 # This file
```

## 🌐 Deployment

The app is deployed on two platforms:

### Frontend: Vercel

- **URL**: https://vibe-coding-one-pink.vercel.app
- **Deployment**: Automatic on git push
- **Files**: HTML, CSS, JS, static assets

### Backend: Railway

- **URL**: https://vibe-coding-production-cdb4.up.railway.app
- **Deployment**: Automatic on git push
- **Environment Variables Required**:
  ```
  GEMINI_API_KEY=your_api_key
  FLASK_ENV=production
  PORT=8080
  ```

### Deploy Your Own

See detailed guides in:
- `docs/DEPLOYMENT_GUIDE.md` - Complete deployment walkthrough
- `docs/RAILWAY_DEPLOYMENT.md` - Railway-specific configuration

Quick deploy buttons:
- [![Deploy to Vercel](https://vercel.com/button)](https://vercel.com/import/project?template=https://github.com/WellyXY/vibe_coding)
- [![Deploy on Railway](https://railway.app/button.svg)](https://railway.app/new/template?template=https://github.com/WellyXY/vibe_coding)

## 📡 API Documentation

### Base URLs

- **Production**: `https://vibe-coding-production-cdb4.up.railway.app`
- **Local**: `http://localhost:5000`

### Endpoints

#### 1. Health Check
```http
GET /api/health
```

**Response**:
```json
{
  "status": "ok",
  "version": "1.0.0"
}
```

#### 2. Get Available Options
```http
GET /api/options
```

**Response**:
```json
{
  "locations": ["New York", "Tokyo", "Paris", ...],
  "occupations": ["Engineer", "Designer", ...],
  "hobbies": ["Photography", "Travel", ...]
}
```

#### 3. Get Recommendations
```http
POST /api/recommend
Content-Type: application/json

{
  "criteria": {
    "location": "New York",
    "hobby": "Photography",
    "occupation": "Engineer",
    "age_min": 25,
    "age_max": 35,
    "gender": "Female"
  },
  "top_k": 50
}
```

**Response**:
```json
{
  "success": true,
  "count": 50,
  "recommendations": [
    {
      "id": 42,
      "name": "Sarah",
      "age": 28,
      "occupation": "Designer",
      "location": "New York, NY",
      "hobby": ["Photography", "Travel"],
      "gender": "Female",
      "image": "avatars/avatar_042.jpg",
      "match_score": 0.95
    },
    ...
  ]
}
```

#### 4. Generate Dynamic Question
```http
POST /api/generate-question
Content-Type: application/json

{
  "previous_answers": ["New York", "Outdoor adventures"],
  "question_number": 2
}
```

**Response**:
```json
{
  "question": "What's your ideal weekend?",
  "options": ["Adventure outdoors", "Cozy at home", "Social activities"]
}
```

### Swagger Documentation

When running locally, visit: `http://localhost:5000/apidocs`

## 🎮 How to Use

1. **Visit the website** or open `index.html`
2. **Click the Agent avatar** (animated GIF in bottom-right corner)
3. **Answer 3 questions**:
   - Question 1: Location (from database)
   - Questions 2-3: AI-generated based on your answers
4. **View recommendations** - Top 50 matches appear as swipeable cards
5. **Swipe cards**:
   - Swipe right or press `→` to like
   - Swipe left or press `←` to skip
   - Click profile for details

## 🛠️ Development

### Available Scripts

All development scripts are in the `scripts/` folder:

```bash
# Generate new user database
python scripts/generate_users.py

# Download avatar images
python scripts/download_avatars.py

# Interactive CLI recommendation tool
python scripts/interactive_recommend.py

# Test API endpoints
python scripts/test_api.py
```

### Configuration Files

- **`config.js`**: Frontend API configuration
  - Automatically switches between local and production
  - Modify `production` URL to use your own backend

- **`.env`**: Backend environment variables
  ```bash
  GEMINI_API_KEY=your_api_key_here
  FLASK_ENV=development  # or production
  PORT=5000
  ```

### Testing

**Test Backend Locally**:
```bash
python app.py
curl http://localhost:5000/api/health
```

**Test Frontend Connection**:
- Open `docs/test-connection.html` in browser
- Run all API tests
- Check console for errors

**Test Full Flow**:
1. Start backend: `python app.py`
2. Open `index.html`
3. Click agent and answer questions
4. Verify recommendations appear

## 🐛 Troubleshooting

### Frontend Issues

**404 Not Found**:
- ✅ **Fixed**: Vercel now deploys only frontend static files
- Backend runs separately on Railway

**CORS Errors**:
- ✅ **Fixed**: Backend CORS configured to allow Vercel domain
- Check `app.py` line 16-31 for CORS settings

**API Connection Failed**:
- Check if backend is running (Railway or local)
- Verify `config.js` has correct backend URL
- Use `docs/test-connection.html` to diagnose

### Backend Issues

**"API key not found"**:
- Set `GEMINI_API_KEY` in `.env` (local) or Railway environment variables
- Get API key from: https://makersuite.google.com/app/apikey

**"No recommendations found"**:
- Check if location exists in `users_database.json`
- Try broader search criteria
- Increase `top_k` value

**Port 5000 in use**:
```bash
# Find and kill process
lsof -ti:5000 | xargs kill -9

# Or change port in app.py
port = int(os.environ.get('PORT', 5001))
```

### Common Questions

**Q: Can I customize the questions?**
A: Yes! Edit the prompt in `app.py` → `generate_question()` function

**Q: How do I add more users?**
A: Edit `users_database.json` or use `scripts/generate_users.py`

**Q: Can I change the number of questions?**
A: Yes! Edit `index.html` line 126: `const TOTAL_QUESTIONS = 3`

**Q: How to replace avatars?**
A: Place new images in `avatars/` folder and update `users_database.json`

## 📦 Dependencies

### Backend (Python)
- **Flask** - Web framework
- **Flask-CORS** - Cross-origin resource sharing
- **requests** - HTTP library
- **python-dotenv** - Environment variable management
- **flasgger** - API documentation (Swagger)
- **gunicorn** - Production WSGI server

### Frontend (JavaScript)
- Vanilla JavaScript (no frameworks)
- Modern ES6+ features
- CSS3 animations

## 🤝 Contributing

Contributions are welcome! Please:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License.

## 🙏 Acknowledgments

- **Google Gemini AI** - Intelligent recommendation ranking
- **[ThisAnimeDoesNotExist](https://thisanimedoesnotexist.ai/)** - Anime avatars
- **[Unsplash](https://unsplash.com/)** - Real photo avatars
- **Vercel** - Frontend hosting
- **Railway** - Backend hosting

## 📞 Support

For questions, issues, or feature requests:
- 📧 Open an issue on [GitHub](https://github.com/WellyXY/vibe_coding/issues)
- 📚 Check the [documentation](docs/)
- 🧪 Use the [API tester](docs/test-connection.html)

---

**Made with ❤️ by WellyXY**

Last Updated: December 2024
