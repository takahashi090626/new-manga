from flask import Flask, request, render_template
import mysql.connector

app = Flask(__name__)

# MySQLの接続情報
db_config = {
    'user': 'root',
    'password': 'root',
    'host': 'localhost',
    'database': 'comics_db',
    'port':'3307'
}

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/search', methods=['POST'])
def search():
    query = request.form['query']
    connection = mysql.connector.connect(**db_config)
    cursor = connection.cursor(dictionary=True)
    cursor.execute("SELECT * FROM comics WHERE title LIKE %s", ('%' + query + '%',))
    results = cursor.fetchall()
    connection.close()
    return render_template('results.html', results=results)

if __name__ == '__main__':
    app.run(debug=True)
