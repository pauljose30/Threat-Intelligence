from flask import Flask, render_template, request
import sqlite3

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    conn = sqlite3.connect("ioc_database.db")
    cursor = conn.cursor()

    if request.method == "POST":
        search_ioc = request.form["search_ioc"]
        query = f"SELECT * FROM iocs WHERE ioc LIKE '%{search_ioc}%'"
        result = cursor.execute(query).fetchall()
        conn.close()
        return render_template("index.html", result=result, search_ioc=search_ioc)
    else:
        query = "SELECT * FROM iocs"
        result = cursor.execute(query).fetchall()
        conn.close()
        return render_template("index.html", result=result, search_ioc="")

if __name__ == "__main__":
    app.run(debug=True)
