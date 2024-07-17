from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
from bs4 import BeautifulSoup
import requests
import os

app = Flask(__name__, static_folder='static')
CORS(app)

@app.route('/')
def serve_index():
    return send_from_directory(app.static_folder, 'index.html')

@app.route('/search', methods=['GET'])
def search():
    url = request.args.get('url')
    if not url:
        return jsonify({'success': False, 'message': 'URLが指定されていません。'})

    try:
        response = requests.get(url)
        soup = BeautifulSoup(response.content, 'html.parser')

        results = []
        for element in soup.find_all(text=True):
            if '教育' in element:
                results.append(element.strip())

        if results:
            return jsonify({'success': True, 'results': results})
        else:
            return jsonify({'success': False, 'message': '教育に関する情報が見つかりませんでした。'})
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)})

if __name__ == '__main__':
    app.run(debug=True)
