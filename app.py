from flask import Flask, request, jsonify
from flask_cors import CORS
import openai
import os
from dotenv import load_dotenv

app = Flask(__name__)
CORS(app)

# 加载环境变量
load_dotenv()

# 设置OpenAI API密钥
openai.api_key = os.getenv('OPENAI_API_KEY')

# Vercel 不支持文件系统操作，所以我们需要修改文件上传逻辑
# 这里我们可以使用云存储服务，比如 AWS S3 或其他替代方案
# 暂时返回提示信息
@app.route('/api/upload', methods=['POST'])
def upload_file():
    return jsonify({
        "message": "File upload is not supported in this deployment. Please contact administrator."
    }), 400

@app.route('/api/chat', methods=['POST'])
def chat():
    data = request.json
    messages = data.get('messages', [])
    
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=messages
        )
        return jsonify({"response": response.choices[0].message.content})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# 添加健康检查端点
@app.route('/health', methods=['GET'])
def health_check():
    return jsonify({"status": "healthy"}), 200

# 添加根路由
@app.route('/')
def home():
    return jsonify({"message": "API is running"}), 200

# Vercel 需要这个
app.debug = True 