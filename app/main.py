from flask import Flask, request, jsonify
import pdfplumber
import io

app = Flask(__name__)

@app.route("/parse_pdf", methods=["POST"])
def parse_pdf():
    if 'file' not in request.files:
        return jsonify({"error": "Файл не найден"}), 400

    file = request.files['file']
    if file.filename == "":
        return jsonify({"error": "Файл не выбран"}), 400

    # Читаем бинарные данные файла в память
    file_bytes = file.read()
    
    # Открываем PDF из бинарника
    pdf_data = io.BytesIO(file_bytes)
    
    result = {"text": [], "tables": []}

    with pdfplumber.open(pdf_data) as pdf:
        for page in pdf.pages:
            # Текст страницы
            text = page.extract_text()
            
            if text:
                result["text"].extend(text.split('\n'))
            
            # Таблицы страницы
            tables = page.extract_tables()
            if tables:
                result["tables"].extend(tables)

    return jsonify(result)


if __name__ == "__main__":
    app.run(debug=True)
