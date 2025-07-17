from flask import Flask, request, jsonify, render_template
import pandas as pd

combined = None  # 전역 선언

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/chart')
def chart():
    return render_template('chart.html')

@app.route('/report')
def report():
    return render_template('research.html')


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
            if not df.empty:
                dfs.append(df)
                filenames.append(f.filename)

        if not dfs:
            return jsonify({"error": "업로드된 파일 중 유효한 데이터가 없습니다."}), 400

        combined = pd.concat(dfs, ignore_index=True)

        # 날짜형 컬럼 문자열로 변환
        for col in combined.select_dtypes(include=['datetime']):
            combined[col] = combined[col].astype(str)

        # NaN/NaT 처리
        combined = combined.fillna('')

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
        return jsonify({"error": "먼저 파일을 업로드해주세요."}), 400

    keyword = request.args.get('q', '').lower()

    if not keyword:
        return jsonify({"error": "검색어가 필요합니다."}), 400

    # 해당 키워드가 들어간 열 찾기
    matched_cols = [col for col in combined.columns if keyword in col.lower()]

    if not matched_cols:
        return jsonify({"error": "해당 키워드를 포함한 열이 없습니다."}), 404

    # 가장 첫 번째 일치한 열로 그래프 만들기
    target_col = matched_cols[0]

    # 학과명이나 분류 열 추정 (시각화 x축용)
    category_col = None
    for cand in ['학과명', '학과', '학부', '계열', '단과대']:
        if cand in combined.columns:
            category_col = cand
            break

    if not category_col:
        return jsonify({"error": "시각화를 위한 분류 열(예: 학과명)이 필요합니다."}), 400

    labels = combined[category_col].astype(str).tolist()
    values = combined[target_col].tolist()

    return jsonify({
        "labels": labels,
        "values": values,
        "column": target_col,
        "category": category_col
    })

@app.route('/columns')
def get_columns():
    global combined

    if combined is None:
        return jsonify({"error": "먼저 엑셀 파일을 업로드해주세요."}), 400

    columns = list(combined.columns)
    return jsonify({"columns": columns})


if __name__ == "__main__":
    app.run(debug=True)
