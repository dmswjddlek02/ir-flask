from flask import Flask, request, jsonify, render_template
import pandas as pd

combined = None  # 전역 선언

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html")

@app.route('/upload', methods=['POST'])
def upload():
    global combined
    try:
        files = request.files.getlist('files')
        if not files:
            return jsonify({"error": "파일이 없습니다."}), 400

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
    except Exception as e:
        return jsonify({"error": f"서버 오류: {str(e)}"}), 500


@app.route('/search')
def search():
    global combined

    if combined is None:
        return jsonify({"error": "먼저 파일을 업로드해야 검색할 수 있어요."}), 400

    keyword = request.args.get('q', '').lower()
    if not keyword:
        return jsonify({"error": "검색어가 필요합니다"}), 400

    matched_cols = [col for col in combined.columns if keyword in col.lower()]
    if not matched_cols:
        return jsonify({"result": [], "message": "일치하는 열 없음"})

    result = combined[matched_cols].to_dict(orient="records")
    return jsonify({"columns": matched_cols, "data": result})


if __name__ == "__main__":
    app.run(debug=True)
