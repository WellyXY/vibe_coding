# 🤝 Project Handoff Document

**Project**: Vibe Coding - AI-Powered Dating Discovery App
**Last Updated**: December 2024
**Status**: ✅ Production Ready

## 📋 Quick Overview

This is a **full-stack dating recommendation app** using AI to match users based on preferences.

- **Live Demo**: https://vibe-coding-one-pink.vercel.app
- **GitHub**: https://github.com/WellyXY/vibe_coding
- **Tech Stack**: Python Flask (backend) + Vanilla JS (frontend) + Gemini AI

## 🏗️ Architecture

```
Frontend (Vercel)          Backend (Railway)
┌─────────────┐            ┌──────────────┐
│ Static HTML │  ──API──>  │  Flask API   │
│ Vanilla JS  │            │  Gemini AI   │
│ CSS3        │            │  Python      │
└─────────────┘            └──────────────┘
```

### Deployment URLs

| Component | Platform | URL |
|-----------|----------|-----|
| Frontend  | Vercel   | https://vibe-coding-one-pink.vercel.app |
| Backend   | Railway  | https://vibe-coding-production-cdb4.up.railway.app |

## 📁 Project Structure (Organized for You!)

```
vibe_coding/
├── 📄 Core Application (What Users See)
│   ├── index.html              # Main app page
│   ├── discover.html           # Alternative UI (not used in production)
│   ├── app.js                  # Card swipe logic
│   ├── styles.css              # All styling
│   └── config.js               # ⭐ API URL config (dev/prod switching)
│
├── 🐍 Backend API
│   ├── app.py                  # ⭐ Main Flask server with all API endpoints
│   ├── recommendation_system.py # AI recommendation engine
│   ├── gemini_client.py        # Gemini API wrapper
│   └── users_database.json     # 100 user profiles
│
├── 🛠️ Development Tools
│   └── scripts/
│       ├── README.md           # ⭐ Explains all scripts
│       ├── generate_users.py   # Create user database
│       ├── test_api.py         # Test all endpoints
│       └── ... (other utilities)
│
├── 📚 Documentation
│   └── docs/
│       ├── DEPLOYMENT_GUIDE.md      # How to deploy
│       ├── RAILWAY_DEPLOYMENT.md    # Railway setup
│       ├── test-connection.html     # ⭐ Test API connectivity
│       └── ... (other guides)
│
├── 🖼️ Assets
│   ├── avatars/                # 100 user avatar images
│   └── assets/                 # UI icons and images
│
└── ⚙️ Configuration
    ├── requirements.txt        # Python dependencies
    ├── Procfile               # Railway startup command
    ├── vercel.json            # Vercel config
    ├── .env.example           # Environment variables template
    └── README.md              # ⭐ START HERE - Complete documentation
```

## 🚀 Getting Started (For New Developer)

### 1. Clone & Setup (5 minutes)

```bash
# Clone the repo
git clone https://github.com/WellyXY/vibe_coding.git
cd vibe_coding

# Install Python dependencies
pip install -r requirements.txt

# Setup environment variables
cp .env.example .env
# Edit .env and add: GEMINI_API_KEY=your_key_here
```

### 2. Run Locally (2 minutes)

```bash
# Start backend
python app.py
# Backend runs on http://localhost:5000

# Open frontend
# Just open index.html in your browser
# Or use: python -m http.server 8000
```

### 3. Test Everything Works

Open `docs/test-connection.html` in browser and click all test buttons. Should see all ✅.

## 🔑 Important Files to Know

### Must Understand

| File | What It Does | When to Edit |
|------|-------------|--------------|
| `app.py` | All API endpoints | Add new features, change AI logic |
| `config.js` | API URL switching | Change backend URL |
| `index.html` | Main UI + Agent logic | Change questions, UI behavior |
| `users_database.json` | User data | Add/modify users |

### Configuration Files

| File | Purpose | Important Settings |
|------|---------|-------------------|
| `.env` | Local environment vars | `GEMINI_API_KEY` |
| `vercel.json` | Vercel deployment | Keep minimal (static files only) |
| `Procfile` | Railway startup | `gunicorn app:app` |
| `requirements.txt` | Python packages | Update if adding libraries |

## 🔐 Environment Variables

### Local Development (.env)
```bash
GEMINI_API_KEY=your_api_key_here
FLASK_ENV=development
PORT=5000
```

### Railway (Production)
Set these in Railway Dashboard > Variables:
```
GEMINI_API_KEY=your_api_key_here
FLASK_ENV=production
PORT=8080
```

### Get Gemini API Key
https://makersuite.google.com/app/apikey

## 📡 API Endpoints

All endpoints are in `app.py`. Here's what each does:

| Endpoint | Method | Purpose | Important? |
|----------|--------|---------|-----------|
| `/api/health` | GET | Check if backend is alive | ⭐ Test first |
| `/api/options` | GET | Get all locations/occupations/hobbies | ⭐ Used by UI |
| `/api/recommend` | POST | Get AI-ranked user recommendations | ⭐ Core feature |
| `/api/generate-question` | POST | Generate dynamic questions with AI | ⭐ Agent feature |

**Test them**: Use `scripts/test_api.py` or `docs/test-connection.html`

## 🎯 How The App Works (User Flow)

1. **User clicks Agent avatar** (bottom-right animated GIF)
2. **Agent asks 3 questions**:
   - Q1: Location (randomly selected from database)
   - Q2-Q3: AI-generated questions based on previous answers
3. **Backend processes**:
   - Filters users by location
   - Uses Gemini AI to rank by compatibility
   - Returns top 50 matches
4. **Frontend displays**: Swipeable cards (Tinder-style)
5. **User swipes**: Left to skip, right to like

## 🐛 Common Issues & Solutions

### Issue: "404 Not Found" on Vercel
**Solution**: ✅ Already fixed! Vercel deploys only frontend. Backend is on Railway.

### Issue: "CORS Error"
**Solution**: ✅ Already fixed! Check `app.py` lines 16-31 for CORS config.

### Issue: "API Key Not Found" on Railway
**Solution**: Set `GEMINI_API_KEY` in Railway Dashboard > Variables

### Issue: Frontend can't connect to backend
**Solution**:
1. Check `config.js` has correct Railway URL
2. Test backend: Visit https://vibe-coding-production-cdb4.up.railway.app/api/health
3. Use `docs/test-connection.html` to diagnose

### Issue: No recommendations returned
**Solution**:
- Check if location exists in `users_database.json`
- Increase `top_k` value in request
- Check Railway logs for errors

## 🔧 Making Changes

### Add New Users
Edit `users_database.json`:
```json
{
  "id": 101,
  "name": "New User",
  "age": 28,
  "occupation": "Engineer",
  "location": "San Francisco, CA",
  "hobby": ["Coding", "Coffee"],
  "gender": "Male",
  "image": "avatars/avatar_101.jpg"
}
```

### Change Number of Questions
Edit `index.html` line 126:
```javascript
const TOTAL_QUESTIONS = 3;  // Change this
```

### Modify AI Prompts
Edit `app.py` → `generate_question()` function → modify the prompt string

### Add New API Endpoint
Add to `app.py`:
```python
@app.route('/api/your-endpoint', methods=['GET'])
def your_endpoint():
    return jsonify({"data": "your data"})
```

## 📦 Deployment

### Frontend (Vercel)
- **Auto-deploys** on every `git push` to main
- **Config**: `vercel.json` (keep it simple!)
- **Check status**: https://vercel.com/dashboard

### Backend (Railway)
- **Auto-deploys** on every `git push` to main
- **Config**: `Procfile` + environment variables
- **Check logs**: Railway Dashboard > Logs
- **Important**: Must set `GEMINI_API_KEY` in Railway variables!

### To Deploy Changes
```bash
git add .
git commit -m "Your changes"
git push origin main
# Both Vercel and Railway will auto-deploy
```

## 🧪 Testing Checklist

Before deploying major changes:

- [ ] Run `python scripts/test_api.py` locally
- [ ] Open `docs/test-connection.html` and test all endpoints
- [ ] Test full user flow:
  - [ ] Click agent
  - [ ] Answer 3 questions
  - [ ] See recommendations
  - [ ] Swipe cards work
- [ ] Check browser console for errors (F12)
- [ ] Test on mobile (responsive design)

## 📞 Resources

### Documentation
- **Start Here**: `README.md` - Complete overview
- **Deployment**: `docs/DEPLOYMENT_GUIDE.md`
- **Railway**: `docs/RAILWAY_DEPLOYMENT.md`
- **Scripts**: `scripts/README.md`
- **Gemini AI**: `docs/GEMINI_README.md`

### Tools
- **API Tester**: `docs/test-connection.html`
- **API Docs**: http://localhost:5000/apidocs (when running locally)
- **Example Usage**: `scripts/interactive_recommend.py`

### External Links
- **GitHub Repo**: https://github.com/WellyXY/vibe_coding
- **Gemini API**: https://makersuite.google.com/app/apikey
- **Vercel Dashboard**: https://vercel.com/dashboard
- **Railway Dashboard**: https://railway.app/dashboard

## 💡 Tips for Next Developer

### Good Practices
1. **Always test locally first** before deploying
2. **Use `docs/test-connection.html`** to quickly test API
3. **Check Railway logs** if something breaks in production
4. **Make small commits** with clear messages
5. **Document your changes** in commit messages

### Avoid Common Mistakes
- ❌ Don't modify `vercel.json` (frontend is static only)
- ❌ Don't hardcode API URLs (use `config.js`)
- ❌ Don't commit `.env` file (has API key!)
- ❌ Don't run scripts from `scripts/` in production
- ✅ Always test changes with `test-connection.html`

### If You Get Stuck
1. Check the error in browser console (F12)
2. Check Railway logs for backend errors
3. Read the relevant doc in `docs/`
4. Test with `scripts/test_api.py` or `docs/test-connection.html`
5. Look at commit history: `git log --oneline`

## 📝 Project Status

### ✅ Working Features
- AI-powered recommendations
- Dynamic question generation
- Swipeable card interface
- Agent interaction
- Location-based filtering
- Production deployment (Vercel + Railway)
- CORS properly configured
- API documentation

### 🚧 Known Limitations
- `discover.html` exists but not used in production
- Only 100 users in database
- Gemini API has rate limits
- Agent asks exactly 3 questions (hardcoded)

### 💡 Potential Improvements
- Add user authentication
- Save liked profiles
- More sophisticated matching algorithm
- Real-time chat feature
- User profile editing
- More users in database
- Caching for faster responses

## 🎉 You're Ready!

You now have everything you need to:
- ✅ Understand the project structure
- ✅ Run it locally
- ✅ Make changes
- ✅ Deploy to production
- ✅ Debug issues
- ✅ Add new features

**Start with**: Open `README.md` for detailed documentation, then run the app locally!

---

**Questions?** Check the `docs/` folder or open an issue on GitHub.

**Good luck!** 🚀

---

*Prepared by: WellyXY*
*Last Updated: December 2024*
