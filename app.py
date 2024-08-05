from flask import Flask, request, render_template
import mysql.connector

app = Flask(__name__)

# MySQLの接続情報
db_config = {
    'user': 'root',
    'password': 'root',
    'host': 'localhost',
    'database': 'comics_db',
    'port': '3307'
}

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/search', methods=['POST'])
def search():
    query = request.form.get('query', '')
    if not query:
        return render_template('results.html', results=[])

    try:
        # データベース接続
        connection = mysql.connector.connect(**db_config)
        cursor = connection.cursor(dictionary=True)
        
        # クエリ実行
        cursor.execute("SELECT * FROM comics WHERE title LIKE %s", ('%' + query + '%',))
        results = cursor.fetchall()
        
        # データベース接続終了
        connection.close()

    except mysql.connector.Error as err:
        print(f"Error: {err}")
        results = []

    return render_template('results.html', results=results)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)
