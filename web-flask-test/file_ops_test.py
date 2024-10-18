import imp
import os
from flask import Flask, request, make_response, jsonify,  send_from_directory 

current_dir = os.path.dirname(os.path.abspath(__file__))
file_operations = imp.load_source('file_operations', current_dir + '/file_operations.py')


app = Flask(__name__, static_folder='static')

@app.route('/')
def home():
    return send_from_directory(app.static_folder, 'index.html')

@app.route('/fmdata', methods=['GET', 'POST'])
def fmdata():

    data = request.args if request.method == 'GET' else request.get_json()

    if 'operation' in data:
        if data['operation'] == 'get_node':
            return jsonify(file_operations.get_node(data['path']))
        elif data['operation'] == 'create_node':
            return jsonify(file_operations.create(data['path'], data['name']))
        elif data['operation'] == 'rename_node':
            return jsonify(file_operations.rename(data['path'], data['name']))
        elif data['operation'] == 'delete_node':
            return jsonify(file_operations.delete(data['path']))
        elif data['operation'] == 'move_node':
            return jsonify(file_operations.move(data['src'], data['dst']))
        elif data['operation'] == 'copy_node':
            return jsonify(file_operations.copy(data['src'], data['dst']))
        elif data['operation'] == 'unzip_node':
            return jsonify(file_operations.unzip(data['path']))
        elif data['operation'] == 'download_node':
            return jsonify(file_operations.download(data['path']))
        elif data['operation'] == 'zip_node':
            return jsonify(file_operations.zip(data['path']))
    else:
        response = make_response(jsonify(message="No operation specified"), 400)
        response.headers['Content-Type'] = "application/json"
        return response

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
