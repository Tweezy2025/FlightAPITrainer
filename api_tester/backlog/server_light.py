from flask import Flask, jsonify
from flask_cors import CORS

app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False  # Отключает экранирование Unicode
CORS(app)

@app.route('/')
def home():
    return jsonify({
        "status": "OK",
        "message": "Сервер работает!"
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000, debug=True)
