from flask import Flask, request, jsonify, render_template
import pandas as pd

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html")

@app.route('/upload', methods=['POST'])
def upload():
    files = request.files.getlist('files[]')
    dfs = []
    filenames = []

    for f in files:
        df = pd.read_excel(f)
        dfs.append(df)
        filenames.append(f.filename)

    combined = pd.concat(dfs, ignore_index=True)

    return jsonify({
        "message": "업로드 성공!",
        "files": filenames,
        "preview": combined.head(10).to_dict(orient='records')
    })

if __name__ == "__main__":
    app.run(debug=True)
