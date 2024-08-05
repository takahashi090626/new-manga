from flask import Flask, render_template, request
import mysql.connector

app = Flask(__name__)

# データベース接続情報
db_config = {
    'host': 'localhost',
    'user': 'root',
    'password': 'root',
    'database': 'comics_db',
    'port':'3307'
}

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/search', methods=['POST'])
def search():
    query = request.form.get('query', '')
    if not query:
        return render_template('index.html', results=[])

    connection = mysql.connector.connect(**db_config)
    cursor = connection.cursor(dictionary=True)
    cursor.execute("SELECT * FROM comics WHERE title LIKE %s", ('%' + query + '%',))
    results = cursor.fetchall()
    cursor.close()
    connection.close()

    return render_template('results.html', results=results)

if __name__ == '__main__':
    app.run(debug=True)
