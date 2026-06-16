import os
import sys
import hashlib
import json
import webbrowser
from threading import Timer
from flask import Flask, render_template, request, jsonify

VERSION = "1.0.0"
SIG_FILE = "signatures.json"

if getattr(sys, 'frozen', False):
    base_path = sys._MEIPASS
    template_folder = os.path.join(base_path, 'templates')
    static_folder = os.path.join(base_path, 'static')
    app = Flask(__name__, template_folder=template_folder, static_folder=static_folder)
else:
    app = Flask(__name__)

# Initialize signature database
if not os.path.exists(SIG_FILE):
    with open(SIG_FILE, 'w') as f:
        json.dump({}, f)

def get_file_hash(filepath):
    """Calculate SHA-256 hash of a file efficiently."""
    sha256_hash = hashlib.sha256()
    try:
        with open(filepath, "rb") as f:
            # Read file in chunks to handle large files without crashing RAM
            for byte_block in iter(lambda: f.read(4096), b""):
                sha256_hash.update(byte_block)
        return sha256_hash.hexdigest()
    except Exception as e:
        return str(e)

@app.route('/')
def index():
    return render_template('index.html', version=VERSION)

@app.route('/monitor', methods=['POST'])
def monitor():
    filepath = request.json.get('path')
    if not os.path.exists(filepath):
        return jsonify({"status": "error", "message": "File not found"}), 404

    current_hash = get_file_hash(filepath)
    
    with open(SIG_FILE, 'r') as f:
        sigs = json.load(f)

    # If file exists in DB, compare. Otherwise, save as new baseline.
    if filepath in sigs:
        old_hash = sigs[filepath]
        if old_hash == current_hash:
            return jsonify({"status": "verified", "hash": current_hash})
        else:
            return jsonify({"status": "alert", "current": current_hash, "old": old_hash})
    else:
        sigs[filepath] = current_hash
        with open(SIG_FILE, 'w') as f:
            json.dump(sigs, f, indent=4)
        return jsonify({"status": "baseline_created", "hash": current_hash})

def open_browser():
    webbrowser.open_new('http://127.0.0.1:5005/')

if __name__ == '__main__':
    Timer(1, open_browser).start()
    app.run(host='127.0.0.1', port=5005, debug=False)
