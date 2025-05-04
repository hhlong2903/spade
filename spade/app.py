from flask import Flask, render_template
import pandas as pd
import spade  # Đây là module bạn đã tạo (spade.py trong cùng thư mục)

app = Flask(__name__)

@app.route("/")
def home():
    # Đọc dữ liệu từ file CSV
    df = pd.read_csv('C:\\Users\\hhl27\\Desktop\\LongCT\\spade\\spade\\data.csv')  # Đọc file CSV

    # Chuyển đổi dữ liệu từ DataFrame sang định dạng phù hợp với spade.read_sequences
    raw_data = df.apply(lambda row: f"{row['sid']} {row['eid']} {row['item']}", axis=1).tolist()

    # Chuyển đổi thành cấu trúc phù hợp
    sequences = spade.read_sequences(raw_data)

    # Chạy thuật toán SPADE
    result = spade.spade_mine(sequences, min_support=2)

    # Chuyển đổi kết quả thành list tuple để truyền sang template
    result_list = sorted(
        [(str(pattern), count) for pattern, count in result.items()],
        key=lambda x: (len(eval(x[0])), x[0])
    )

    # Phân loại kết quả theo số lượng item trong pattern, tính cả phần tử bên trong tuple
    grouped_results = {}
    for pattern, count in result_list:
        # Tính số lượng phần tử trong pattern (bao gồm cả các phần tử bên trong tuple con)
        length = sum([len(item) if isinstance(item, tuple) else 1 for item in eval(pattern)])
        
        if length not in grouped_results:
            grouped_results[length] = []
        grouped_results[length].append((pattern, count))

    # Truyền grouped_results vào template
    return render_template("index.html", grouped_results=grouped_results)

if __name__ == "__main__":
    app.run(debug=True)
