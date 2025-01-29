import os
from flask import Flask, request, make_response, jsonify, send_from_directory, send_file
from flask_sock import Sock
import subprocess
import urllib.parse
import werkzeug
import mimetypes
import liblo
import file_operations

GRABS_PATH = "/sdcard/Grabs/"
MODES_PATH = "/"
USER_DIR =   "/sdcard/"

# osc to eyesy app
try:
	osc_target = liblo.Address(4000)
except liblo.AddressError as err:
	print(err)
	sys.exit()

app = Flask(__name__, static_folder='static')
app.config['SECRET_KEY'] = 'secret!'
sock = Sock(app)  # Use Flask-Sock for WebSockets

def background_thread(ws):
    cmd = ["journalctl", "-f", "-u", "eyesypy.service", "-o", "cat"]
    with subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE) as p:
        try:
            for line in iter(p.stdout.readline, b''):
                try:
                    ws.send(line.decode())  # Send output over WebSocket
                except:
                    print("WebSocket disconnected. Stopping journalctl...")
                    break  # Exit the loop when the WebSocket is closed
        finally:
            p.terminate()  # Forcefully stop journalctl
            p.wait()       # Ensure process is fully terminated
            print("journalctl process terminated.")

@app.route('/test')
def test():
    return "asdf"

@app.route('/stop_video_engine')
def stop_video_engine():
    print("stopping video...")
    os.system("sudo systemctl stop eyesypy")
    return "stopping video..."

@app.route('/start_video_engine')
def start_video_engine():
    print("starting video...")
    os.system("sudo systemctl start eyesypy")
    return "starting video..."

@app.route('/')
def index():
    return send_from_directory(app.static_folder, 'index.html')

@app.route('/reload_mode', methods=['GET', 'POST'])
def reload_mode():
    liblo.send(osc_target, "/reload", 1)
    return "reloaded mode"

@app.route('/get_file', methods=['GET'])
def get_file():
    fpath = request.args.get('fpath')
    file_path = os.path.join(MODES_PATH, fpath)

    # Guess the MIME type of the file
    mime_type, _ = mimetypes.guess_type(file_path)
    if mime_type is None:
        mime_type = 'application/octet-stream'  # Default MIME type

    return send_file(file_path, mimetype=mime_type)

@app.route('/download')
def download():
    fpath = request.args.get('fpath')
    src = os.path.join(file_operations.BASE_DIR, urllib.parse.unquote(fpath))
    fname = os.path.basename(src)
    fname = urllib.parse.quote(fname)
    return send_file(src, mimetype='application/octet-stream', as_attachment=True, download_name=fname)

@app.route('/upload', methods=['POST'])
def upload():
    upload = request.files['files[]']
    dst = request.form['dst']
    folder = dst
    filename = werkzeug.utils.secure_filename(upload.filename)
    size = 0
    filepath = os.path.join(file_operations.BASE_DIR, folder, filename)
    filepath = file_operations.check_and_inc_name(filepath)  # As per your function

    with open(filepath, 'wb') as newfile:
        data = upload.read()
        size += len(data)
        newfile.write(data)

    print(f"Saved file, size: {size}")

    response = {
        "files": [
            {
                "name": "x",
                "size": size,
                "url": "na",
                "thumbnailUrl": "na",
                "deleteUrl": "na",
                "deleteType": "DELETE"
            }
        ]
    }
    return jsonify(response)

@app.route('/save', methods=['POST'])
def save():
    fpath = request.form.get('fpath')
    content = request.form.get('content')
    
    if not fpath or not content:
        return "Missing 'fpath' or 'content' in form data.", 400
    
    mode_path = MODES_PATH + fpath
    with open(mode_path, "w") as text_file:
        text_file.write(content)
    
    print("SAVED " + fpath)
    return "SAVED " + fpath

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

#@socketio.on('connect', namespace='/test')
#def test_connect():
#    sid = request.sid
#    socketio.start_background_task(target=background_thread, sid=sid)

#if __name__ == '__main__':
#    socketio.run(app, host='0.0.0.0', debug=True, port=8080)

@sock.route('/log_stream')
def log_stream(ws):
    background_thread(ws)  # Start sending logs to the WebSocket client

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=False, port=8080)




