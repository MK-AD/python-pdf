from flask import Flask, jsonify, send_file, request
from models.PdfClass import PdfClass

app = Flask(__name__)


@app.route('/create-pdf', methods=["POST"])
def create_pdf():
    # retrieve data from json
    content = request.get_json()

    generate_model = PdfClass(content)
    output = generate_model.generate_document()
    response = jsonify({'message': output})
    response.status_code = 200
    return response

@app.route('/health', methods=["GET"])
def health_action():
    response = jsonify({'message': 'OK'})
    response.status_code = 200
    return response


if __name__ == '__main__':
    app.run(debug=True, port=8000)