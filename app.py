from flask import Flask, request, render_template
import firebase_admin
from firebase_admin import credentials, firestore
import os
import base64
import json

app = Flask(__name__)

# Firebase Admin SDK の初期化
def initialize_firebase():
    if 'GOOGLE_CREDENTIALS_BASE64' in os.environ:
        try:
            # Base64デコード
            encoded_credentials = os.environ.get('GOOGLE_CREDENTIALS_BASE64')
            decoded_credentials = base64.b64decode(encoded_credentials).decode('utf-8')
            # JSONとしてパース
            cred_dict = json.loads(decoded_credentials)
            # 認証情報オブジェクトを作成
            cred = credentials.Certificate(cred_dict)
        except Exception as e:
            print(f"Error decoding credentials: {e}")
            return None
    elif os.path.exists('manga.json'):
        cred = credentials.Certificate('manga.json')  # ローカル開発用
    else:
        print("No credentials found")
        return None

    try:
        firebase_admin.initialize_app(cred)
        return firestore.client()
    except Exception as e:
        print(f"Error initializing Firebase: {e}")
        return None

# Firestore インスタンスの取得
db = initialize_firebase()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/search', methods=['POST'])
def search():
    if db is None:
        return render_template('error.html', message="Database connection error"), 500

    query = request.form.get('query', '').strip()
    if not query:
        return render_template('results.html', results=[])

    try:
        # Firestore からデータを取得
        comics_ref = db.collection('comics')
        query_ref = comics_ref.where('title', '>=', query).where('title', '<=', query + '\uf8ff')
        results = query_ref.stream()

        # 結果をリストに変換
        results_list = [doc.to_dict() for doc in results]
        print(f"Search Results: {results_list}")  

    except Exception as e:
        print(f"Error: {e}")
        return render_template('error.html', message="An error occurred during search"), 500

    return render_template('results.html', results=results_list)

if __name__ == '__main__':
    # Heroku環境変数からポート番号を取得
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)