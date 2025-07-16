from flask import Flask, request, jsonify, render_template
import pandas as pd

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/upload", methods=["POST"])
def upload():
    files = request.files.getlist("files[]")
    dfs = []
    for file in files:
        df = pd.read_excel(file)
        dfs.append(df)
    combined = pd.concat(dfs, ignore_index=True)
    return jsonify(combined.head(10).to_dict(orient="records"))

if __name__ == "__main__":
    app.run(debug=True)
