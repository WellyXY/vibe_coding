#!/usr/bin/env python3
"""
Flask API 後端服務
提供推薦接口
"""

from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
from flasgger import Swagger
from recommendation_system import UserRecommendationSystem
import json
import os

app = Flask(__name__)

# 配置 CORS - 允許來自 Vercel 和本地開發的請求
CORS(app, resources={
    r"/api/*": {
        "origins": [
            "https://vibe-coding-one-pink.vercel.app",  # Vercel 生產環境
            "http://localhost:*",  # 本地開發
            "http://127.0.0.1:*",  # 本地開發
            "http://localhost:8000",  # 常用本地端口
            "http://localhost:5500",  # Live Server
            "http://localhost:3000"   # 其他常用端口
        ],
        "methods": ["GET", "POST", "OPTIONS"],
        "allow_headers": ["Content-Type"],
        "supports_credentials": False
    }
})

# 配置 Swagger
app.config['SWAGGER'] = {
    'title': 'Gemini Recommendation API',
    'uiversion': 3,
    'version': '1.0.0',
    'description': '基於 Gemini AI 的智能用戶推薦系統 API',
    'termsOfService': '',
    'contact': {
        'email': 'support@example.com',
    },
    'license': {
        'name': 'Apache 2.0',
        'url': 'http://www.apache.org/licenses/LICENSE-2.0.html',
    }
}

swagger = Swagger(app)

# 初始化推薦系統
try:
    rec_system = UserRecommendationSystem()
    print("✅ 推薦系統初始化成功")
except Exception as e:
    print(f"❌ 推薦系統初始化失敗: {e}")
    rec_system = None

# 獲取所有可用選項
try:
    with open('users_database.json', 'r', encoding='utf-8') as f:
        users = json.load(f)
    
    # 提取唯一的地區、職業、興趣
    locations = sorted(list(set([user['location'] for user in users])))
    occupations = sorted(list(set([user['occupation'] for user in users])))
    all_hobbies = []
    for user in users:
        all_hobbies.extend(user['hobby'])
    hobbies = sorted(list(set(all_hobbies)))
except Exception as e:
    print(f"⚠️  警告: 無法加載用戶數據庫: {e}")
    locations, occupations, hobbies = [], [], []


@app.route('/')
def index():
    """返回主頁面"""
    return send_from_directory('.', 'index.html')


@app.route('/<path:filename>')
def serve_static(filename):
    """提供靜態文件（CSS, JS, JSON等）"""
    return send_from_directory('.', filename)


@app.route('/assets/<path:filename>')
def serve_assets(filename):
    """提供 assets 資料夾下的靜態資源"""
    return send_from_directory('assets', filename)


@app.route('/avatars/<path:filename>')
def serve_avatars(filename):
    """提供 avatars 資料夾下的頭像圖片"""
    return send_from_directory('avatars', filename)



@app.route('/api/generate-question', methods=['POST'])
def generate_question():
    """
    動態生成問題
    ---
    tags:
      - Agent
    description: 使用 Gemini AI 根據之前的回答生成下一個問題
    parameters:
      - name: body
        in: body
        required: true
        schema:
          type: object
          properties:
            previous_answers:
              type: array
              items:
                type: string
              description: 用戶之前的回答
            question_number:
              type: integer
              description: 當前問題編號
    responses:
      200:
        description: 成功生成問題
        schema:
          type: object
          properties:
            question:
              type: string
            options:
              type: array
              items:
                type: string
    """
    try:
        data = request.json
        if not data:
            return jsonify({'error': '無效的請求'}), 400
        
        previous_answers = data.get('previous_answers', [])
        question_number = data.get('question_number', 2)
        
        # 構建 Gemini prompt
        prompt = f"""You are a dating app matchmaker AI. Based on the user's previous answers:
{previous_answers}

Generate a creative, engaging question (question #{question_number}) to learn more about their dating preferences or personality.

IMPORTANT:
- Provide EXACTLY 3 distinct, concise options
- Keep options short (2-4 words max)
- Make the question conversational and fun
- Vary the question type (personality, activities, values, lifestyle)
- Each option should be different enough to be meaningful

Return ONLY valid JSON in this exact format (no markdown, no extra text):
{{
  "question": "Your question here?",
  "options": ["Option 1", "Option 2", "Option 3"]
}}"""

        # 調用 Gemini
        from gemini_client import GeminiClient
        gemini = GeminiClient()
        response = gemini.generate_text(prompt, temperature=0.9)
        
        # 解析回應
        if response and 'candidates' in response:
            text = response['candidates'][0]['content']['parts'][0]['text']
            
            # 清理可能的 markdown 格式
            text = text.strip()
            if text.startswith('```json'):
                text = text[7:]
            if text.startswith('```'):
                text = text[3:]
            if text.endswith('```'):
                text = text[:-3]
            text = text.strip()
            
            # 解析 JSON
            import json
            result = json.loads(text)
            
            # 驗證格式
            if 'question' not in result or 'options' not in result:
                raise ValueError('Invalid response format')
            
            # 確保只有 3 個選項
            result['options'] = result['options'][:3]
            
            return jsonify(result), 200
        else:
            return jsonify({'error': '無法生成問題'}), 500
            
    except Exception as e:
        print(f"❌ Error generating question: {e}")
        # 返回備用問題
        fallback_questions = [
            {
                "question": "What's your ideal weekend?",
                "options": ["Adventure outdoors", "Cozy at home", "Social activities"]
            },
            {
                "question": "What matters most to you?",
                "options": ["Humor & fun", "Deep conversations", "Shared hobbies"]
            }
        ]
        return jsonify(fallback_questions[question_number % 2]), 200


@app.route('/api/health', methods=['GET'])
def health_check():
    """
    健康檢查接口
    ---
    tags:
      - System
    responses:
      200:
        description: 系統運行正常
        schema:
          type: object
          properties:
            status:
              type: string
              example: ok
            version:
              type: string
              example: 1.0.0
    """
    return jsonify({"status": "ok", "version": "1.0.0"})


@app.route('/api/options', methods=['GET'])
def get_options():
    """
    獲取所有可用的篩選選項
    ---
    tags:
      - Data
    description: 返回系統中所有可用的地點、職業和興趣選項，用於前端構建篩選器。
    responses:
      200:
        description: 成功獲取選項
        schema:
          type: object
          properties:
            locations:
              type: array
              items:
                type: string
              description: 可用地點列表
            occupations:
              type: array
              items:
                type: string
              description: 可用職業列表
            hobbies:
              type: array
              items:
                type: string
              description: 可用興趣列表
    """
    return jsonify({
        'locations': locations,
        'occupations': occupations,
        'hobbies': hobbies
    })


@app.route('/avatars/<path:filename>')
def serve_avatar(filename):
    """提供頭像圖片"""
    # 嘗試 JPG 和 PNG
    jpg_path = os.path.join('avatars', filename)
    png_path = os.path.join('avatars', filename.replace('.jpg', '.png'))

    if os.path.exists(jpg_path):
        return send_from_directory('avatars', filename)
    elif os.path.exists(png_path):
        return send_from_directory('avatars', filename.replace('.jpg', '.png'))
    else:
        return "File not found", 404


@app.route('/api/recommend', methods=['POST'])
def recommend():
    """
    智能推薦接口
    ---
    tags:
      - Recommendation
    description: 根據用戶提供的條件，使用 Gemini AI 進行智能排序並返回推薦用戶。
    parameters:
      - name: body
        in: body
        required: true
        schema:
          type: object
          required:
            - criteria
          properties:
            criteria:
              type: object
              description: 篩選條件
              properties:
                location:
                  type: string
                  description: 目標地點
                hobby:
                  type: string
                  description: 目標興趣
                occupation:
                  type: string
                  description: 目標職業
                age_min:
                  type: integer
                  description: 最小年齡
                age_max:
                  type: integer
                  description: 最大年齡
                gender:
                  type: string
                  description: 性別偏好
            top_k:
              type: integer
              default: 5
              description: 返回結果數量
    responses:
      200:
        description: 推薦成功
        schema:
          type: object
          properties:
            success:
              type: boolean
            count:
              type: integer
            recommendations:
              type: array
              items:
                type: object
                properties:
                  id:
                    type: integer
                  name:
                    type: string
                  age:
                    type: integer
                  location:
                    type: string
                  occupation:
                    type: string
                  hobby:
                    type: array
                    items:
                      type: string
      400:
        description: 請求參數錯誤
      500:
        description: 服務器內部錯誤
    """
    if not rec_system:
        return jsonify({
            'success': False,
            'error': '推薦系統未初始化'
        }), 500

    try:
        data = request.json
        if not data:
            return jsonify({
                'success': False,
                'error': '無效的 JSON 數據'
            }), 400

        criteria = data.get('criteria', {})
        top_k = data.get('top_k', 5)
        
        # 驗證 top_k
        if not isinstance(top_k, int) or top_k < 1 or top_k > 100:
            top_k = 50

        # 執行推薦
        recommendations = rec_system.recommend(criteria, top_k=top_k, use_ai_ranking=True)

        return jsonify({
            'success': True,
            'recommendations': recommendations,
            'count': len(recommendations)
        })

    except Exception as e:
        print(f"推薦過程出錯: {e}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


if __name__ == '__main__':
    import os
    port = int(os.environ.get('PORT', 8000))
    debug = os.environ.get('FLASK_ENV') == 'development'

    print("🚀 推薦系統 API 服務器啟動中...")
    print(f"📄 API 文檔: http://localhost:{port}/apidocs")
    print("=" * 50)
    app.run(host='0.0.0.0', port=port, debug=debug)
