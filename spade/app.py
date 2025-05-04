from flask import Flask, render_template, request, redirect, url_for
import pandas as pd
import spade  # Đây là module bạn đã tạo (spade.py trong cùng thư mục)
import os

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'  # Thư mục để lưu tệp tải lên

@app.route("/", methods=["GET", "POST"])
def home():
    if request.method == "POST":
        # Lấy tệp CSV và giá trị minsup từ form
        file = request.files['file']
        minsup = int(request.form['minsup'])

        if file:
            # Lưu tệp CSV vào thư mục uploads
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
            file.save(filepath)

            # Đọc dữ liệu từ tệp CSV
            df = pd.read_csv(filepath)
            raw_data = df.apply(lambda row: f"{row['sid']} {row['eid']} {row['item']}", axis=1).tolist()

            # Chuyển đổi thành cấu trúc phù hợp
            sequences = spade.read_sequences(raw_data)

            # Chạy thuật toán SPADE
            result = spade.spade_mine(sequences, min_support=minsup)

            # Chuyển đổi kết quả thành list tuple để truyền sang template
            result_list = sorted(
                [(str(pattern), count) for pattern, count in result.items()],
                key=lambda x: (len(eval(x[0])), x[0])
            )

            # Phân loại kết quả theo số lượng item trong pattern
            grouped_results = {}
            for pattern, count in result_list:
                length = sum([len(item) if isinstance(item, tuple) else 1 for item in eval(pattern)])
                if length not in grouped_results:
                    grouped_results[length] = []
                grouped_results[length].append((pattern, count))

            # Hiển thị kết quả
            return render_template("index.html", grouped_results=grouped_results)

    return render_template("upload.html")

if __name__ == "__main__":
    app.run(debug=True)