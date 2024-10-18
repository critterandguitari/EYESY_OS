
import os
import imp
from flask import Flask, request, make_response, jsonify, send_from_directory, send_file
from flask_socketio import SocketIO, emit
import subprocess

GRABS_PATH = "/sdcard/Grabs/"
MODES_PATH = "/"
USER_DIR =   "/sdcard/"

current_dir = os.path.dirname(os.path.abspath(__file__))
file_operations = imp.load_source('file_operations', current_dir + '/file_operations.py')

app = Flask(__name__, static_folder='static')
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app)

def background_thread(sid):
    with subprocess.Popen(["tail", "-F", "/home/music/testlog"], stdout=subprocess.PIPE) as p:
        for line in iter(p.stdout.readline, b''):
            socketio.emit('log_output', {'data': line.decode()}, room=sid, namespace='/test')

@app.route('/')
def index():
    #return render_template('index.html')
    return send_from_directory(app.static_folder, 'index.html')

#@app.route('/get_file')
#def get_file():

@app.route('/get_file', methods=['GET'])
def get_file():
    fpath = request.args.get('fpath')
    mode_path = os.path.join(MODES_PATH, fpath)
    return send_file(mode_path, mimetype='text/plain')


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

@socketio.on('connect', namespace='/test')
def test_connect():
    sid = request.sid
    socketio.start_background_task(target=background_thread, sid=sid)

if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', debug=True)



