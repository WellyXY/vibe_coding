# Vibe Coding - AI-Powered Dating Discovery App

An intelligent dating recommendation system powered by Gemini AI, featuring an interactive agent and swipeable card interface.

![Python](https://img.shields.io/badge/Python-3.9+-blue.svg)
![Flask](https://img.shields.io/badge/Flask-2.3+-green.svg)
![License](https://img.shields.io/badge/license-MIT-blue.svg)

## 🌟 Features

- **AI-Powered Recommendations**: Uses Google Gemini AI to intelligently rank and recommend users
- **Interactive Agent**: Conversational UI that asks personalized questions
- **Swipeable Cards**: Tinder-like card interface with smooth animations
- **Dynamic Questions**: AI-generated questions based on user preferences
- **Anime Avatars**: Beautiful anime-style character avatars
- **RESTful API**: Clean API for easy integration

## 🚀 Quick Start

### Prerequisites

- Python 3.9 or higher
- pip (Python package manager)
- A Gemini API key (get it from [Google AI Studio](https://makersuite.google.com/app/apikey))

### Installation

1. **Clone the repository**
   ```bash
   git clone git@github.com:WellyXY/vibe_coding.git
   cd vibe_coding
   ```

2. **Create virtual environment**
   ```bash
   python3 -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure environment variables**
   ```bash
   cp .env.example .env
   # Edit .env and add your Gemini API key
   ```

5. **Start the server**
   ```bash
   python3 app.py
   ```

6. **Open your browser**
   ```
   http://localhost:5000
   ```

## 📁 Project Structure

```
vibe_coding/
├── app.py                          # Flask backend server
├── app.js                          # Frontend card stack logic
├── index.html                      # Main web interface
├── styles.css                      # Styling
├── recommendation_system.py        # AI recommendation engine
├── gemini_client.py               # Gemini API client
├── users_database.json            # User data (100 users)
├── avatars/                       # User avatar images
│   ├── avatar_001.jpg - avatar_070.jpg   # Real photos
│   └── avatar_071.png - avatar_100.png   # Anime characters
├── assets/                        # UI assets
├── requirements.txt               # Python dependencies
├── .env.example                   # Environment variables template
└── README.md                      # This file
```

## 🎮 How to Use

1. **Click the Agent avatar** (bottom right corner)
2. **Answer questions** about your preferences:
   - Location (randomly selected from database)
   - Dynamically generated questions by AI
3. **View recommendations** - Top 50 matches appear as swipeable cards
4. **Swipe cards**:
   - Swipe right or press → to like
   - Swipe left or press ← to skip

## 🔧 API Endpoints

### Get Available Options
```bash
GET /api/options
```
Returns all available locations, occupations, and hobbies.

### Get Recommendations
```bash
POST /api/recommend
Content-Type: application/json

{
  "criteria": {
    "location": "New York",
    "hobby": "Photography",
    "occupation": "Engineer",
    "age_min": 25,
    "age_max": 35
  },
  "top_k": 5
}
```

### Generate Dynamic Question
```bash
POST /api/generate-question
Content-Type: application/json

{
  "previous_answers": ["New York", "Outdoor adventures"],
  "question_number": 2
}
```

### Health Check
```bash
GET /api/health
```

## 🎨 Customization

### Add More Users

Edit `users_database.json`:
```json
{
  "id": 101,
  "name": "Your Name",
  "age": 25,
  "occupation": "Your Job",
  "location": "Your City",
  "hobby": ["Hobby1", "Hobby2"],
  "gender": "Male",
  "image": "avatars/avatar_101.jpg"
}
```

### Change Number of Questions

Edit `index.html`:
```javascript
const TOTAL_QUESTIONS = 3; // Change this number
```

### Customize Agent Behavior

Edit the prompt in `app.py` → `/api/generate-question` endpoint.

## 🛠️ Development

### Replace Avatars

To replace cartoon avatars with anime characters:
```bash
python3 download_anime_avatars.py
```

This will:
- Backup old avatars to `avatars/backup_cartoon/`
- Download 30 new anime avatars from online APIs
- Replace avatars 71-100

### Test API

```bash
# Test recommendations
curl -X POST http://localhost:5000/api/recommend \
  -H "Content-Type: application/json" \
  -d '{"criteria": {"location": "Chicago"}, "top_k": 5}'

# Test options endpoint
curl http://localhost:5000/api/options
```

## 🐛 Troubleshooting

### Issue: "No recommendations found"
- Check if the location you selected exists in `users_database.json`
- The agent now dynamically loads locations from the database

### Issue: "API Error"
- Verify your Gemini API key in `.env`
- Check if you have internet connection

### Issue: "Avatars not loading"
- Ensure avatars are in `avatars/` directory
- Check file permissions

### Issue: "Port 5000 already in use"
- Stop other services using port 5000
- Or change the port in `app.py`: `app.run(port=5001)`

## 📦 Dependencies

- **Flask** - Web framework
- **Flask-CORS** - Cross-origin resource sharing
- **requests** - HTTP library
- **python-dotenv** - Environment variable management
- **flasgger** - API documentation (Swagger UI)

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📄 License

This project is licensed under the MIT License.

## 🙏 Acknowledgments

- Google Gemini AI for intelligent recommendations
- [ThisAnimeDoesNotExist](https://thisanimedoesnotexist.ai/) for anime avatars
- [Waifu.pics](https://waifu.pics/) for additional anime images

## 📞 Contact

For questions or support, please open an issue on GitHub.

---

Made with ❤️ by WellyXY
