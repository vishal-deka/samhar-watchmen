import sqlite3 as sql
from flask import Flask, jsonify, render_template

app = Flask(__name__)



@app.route('/', methods=['GET'])
def home():
	return render_template('index.html')
	
@app.route('/fetch', methods=['GET'])
def get():
	conn = sql.connect('example.db')
	c = conn.cursor()
	res = c.execute("SELECT * FROM maindb")
	
	resp = []
	for i in res:
		d = {"id": i[0], "time": i[1], "lat": i[2], "lot": i[3], "count": i[4]}
		resp.append(d)
	return jsonify(resp)
	
if __name__ == "__main__":
	app.run('localhost', 5000, debug=True)
conn.close()