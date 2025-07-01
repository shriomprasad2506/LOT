from flask import Flask, render_template, request, redirect, url_for, send_from_directory
from datetime import datetime
import os

app = Flask(__name__)
UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Ensure upload folder exists
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

# Helper to check if a file is allowed
ALLOWED_EXTENSIONS = {'pdf'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def index():
    today = datetime.now().strftime('%d %B %Y')
    # Check if files exist
    morning_exists = os.path.exists(os.path.join(UPLOAD_FOLDER, 'morning_pdf.pdf'))
    night_exists = os.path.exists(os.path.join(UPLOAD_FOLDER, 'night_pdf.pdf'))
    return render_template('index.html', today=today,
                           morning_exists=morning_exists,
                           night_exists=night_exists)

@app.route('/admin')
def admin():
    success = request.args.get('success')
    morning_exists = os.path.exists(os.path.join(UPLOAD_FOLDER, 'morning_pdf.pdf'))
    night_exists = os.path.exists(os.path.join(UPLOAD_FOLDER, 'night_pdf.pdf'))
    return render_template('admin.html', success=success,
                           morning_exists=morning_exists,
                           night_exists=night_exists)

@app.route('/upload', methods=['POST'])
def upload():
    for key in ['morning_pdf', 'night_pdf']:
        file = request.files.get(key)
        if file and allowed_file(file.filename):
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], f'{key}.pdf'))
    return redirect(url_for('admin', success='Files uploaded successfully.'))

@app.route('/results/<filename>')
def serve_result(filename):
    return send_from_directory(UPLOAD_FOLDER, filename)

if __name__ == '__main__':
    app.run(debug=True, port=5001)
