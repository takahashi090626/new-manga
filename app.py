import os
from flask import Flask, request, render_template
import firebase_admin
from firebase_admin import credentials, firestore

app = Flask(__name__)

# Firebase Admin SDK の初期化
cred = credentials.Certificate('manga.json')  # サービスアカウントキーのパスを指定
firebase_admin.initialize_app(cred)

# Firestore インスタンスの取得
db = firestore.client()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/search', methods=['POST'])
def search():
    query = request.form.get('query', '')
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
        results_list = []

    return render_template('results.html', results=results_list)

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 8080))
    app.run(host='0.0.0.0', port=port, debug=True)
