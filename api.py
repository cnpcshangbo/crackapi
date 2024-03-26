from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route('/api', methods=['GET'])
def get_fake_number():
    print(request.args)
    html_file = request.args.get('html_file')
    print(html_file)
    html_file_name = html_file.split('/')[-1]
    print(html_file_name)
    if html_file_name == 'copc_bayonne_crackoverlay_meta.html':
        print('find the right las file')
    response = jsonify({'number': 2.456})
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response

if __name__ == '__main__':
    app.run(port=5002)
