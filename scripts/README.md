# Development Scripts

This folder contains utility scripts for development and data management.

## 📝 Scripts Overview

### User Database Management

#### `generate_users.py`
Generate a user database with random data.

```bash
python scripts/generate_users.py
```

**What it does**:
- Creates `users_database.json` with 100 users
- Generates random names, ages, occupations, locations
- Assigns avatar images
- Uses Chinese/English mixed data

#### `generate_users_english.py`
Generate an English-only user database.

```bash
python scripts/generate_users_english.py
```

**What it does**:
- Same as above but with English names only
- Western locations and occupations

### Avatar Management

#### `download_avatars.py`
Download real photo avatars.

```bash
python scripts/download_avatars.py
```

**What it does**:
- Downloads 70 real portrait photos
- Saves to `avatars/avatar_001.jpg` - `avatar_070.jpg`
- Uses Unsplash API

#### `download_anime_avatars.py`
Download anime-style avatars.

```bash
python scripts/download_anime_avatars.py
```

**What it does**:
- Downloads 30 anime character images
- Saves to `avatars/avatar_071.png` - `avatar_100.png`
- Uses ThisAnimeDoesNotExist API

#### `download_hd_avatars.py`
Download high-definition avatars.

```bash
python scripts/download_hd_avatars.py
```

#### `download_large_avatars.py`
Download larger avatar images.

```bash
python scripts/download_large_avatars.py
```

### Data Cleanup

#### `replace_inappropriate.py`
Clean up inappropriate content from user database.

```bash
python scripts/replace_inappropriate.py
```

**What it does**:
- Scans `users_database.json` for inappropriate content
- Replaces with safe alternatives
- Creates backup before modifying

#### `retry_failed.py`
Retry failed avatar downloads.

```bash
python scripts/retry_failed.py
```

**What it does**:
- Checks for missing avatar files
- Re-downloads failed images
- Reports success/failure

#### `convert_svg_to_jpg.py`
Convert SVG icons to JPG format.

```bash
python scripts/convert_svg_to_jpg.py
```

### Testing & Interactive Tools

#### `test_api.py`
Test all API endpoints.

```bash
python scripts/test_api.py
```

**What it does**:
- Tests `/api/health`
- Tests `/api/options`
- Tests `/api/recommend`
- Tests `/api/generate-question`
- Reports results

#### `interactive_recommend.py`
Interactive CLI recommendation tool.

```bash
python scripts/interactive_recommend.py
```

**What it does**:
- Prompts for search criteria
- Displays recommendations in terminal
- Shows match scores
- Useful for testing recommendation logic

**Example**:
```
🌍 Location: New York
🎨 Hobbies (comma-separated): Photography, Travel
💼 Occupation: Engineer
🎂 Age range: 25-35
⚧ Gender: Female

✨ Top 5 Recommendations:
1. Sarah (28) - Engineer - New York
   Match Score: 0.95
   Hobbies: Photography, Travel, Cooking
```

#### `example_chatbot.py`
Example of using Gemini AI for chat.

```bash
python scripts/example_chatbot.py
```

**What it does**:
- Demonstrates Gemini API usage
- Interactive chatbot example
- Useful for testing API key

## 🔧 Common Tasks

### Fresh Start
To reset everything and start fresh:

```bash
# 1. Generate new users
python scripts/generate_users.py

# 2. Download avatars
python scripts/download_avatars.py
python scripts/download_anime_avatars.py

# 3. Clean up data
python scripts/replace_inappropriate.py

# 4. Test
python scripts/test_api.py
```

### Update Only Avatars
To update just the avatar images:

```bash
python scripts/download_avatars.py
python scripts/download_anime_avatars.py
```

### Test Recommendations
To test the recommendation system:

```bash
# Interactive testing
python scripts/interactive_recommend.py

# Or API testing
python scripts/test_api.py
```

## ⚠️ Important Notes

- **Backup**: These scripts modify `users_database.json`. Make backups!
- **API Keys**: Some scripts require `GEMINI_API_KEY` in `.env`
- **Internet**: Avatar download scripts require internet connection
- **Rate Limits**: Be aware of API rate limits when downloading avatars

## 🚫 What NOT to Run in Production

These scripts are for **development only**. Do not run in production:

- ❌ Don't run generators on production database
- ❌ Don't download avatars in production
- ✅ Only use test scripts for diagnostics

## 📚 Learn More

For detailed information about:
- **Recommendation System**: See `docs/RECOMMENDATION_README.md`
- **Gemini API**: See `docs/GEMINI_README.md`
- **API Documentation**: See main `README.md`
