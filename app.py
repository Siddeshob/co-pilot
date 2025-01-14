from flask import Flask, render_template, request, jsonify
from werkzeug.utils import secure_filename
from Read_File_Content_File import read_file_content
import os
import PyPDF2
import pandas as pd

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'

# Create uploads directory if it doesn't exist
if not os.path.exists(app.config['UPLOAD_FOLDER']):
    os.makedirs(app.config['UPLOAD_FOLDER'])

# Add this root route
@app.route('/')
def index():
    return render_template('index.html')

# Rest of your routes remain the same
@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return 'No file uploaded'
    
    file = request.files['file']
    if file.filename == '':
        return 'No file selected'
    
    if file:
        try:
            file_ext = os.path.splitext(file.filename)[1].lower()
            filename = secure_filename(file.filename)
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(filepath)
            content = read_file_content(filepath, file_ext)
            
            return jsonify({
                'message': 'File processed successfully',
                'content': content,
                'filepath': filepath
            })
            
        except Exception as e:
            return str(e), 400
        

@app.route('/files')
def list_files():
    files = os.listdir(app.config['UPLOAD_FOLDER'])
    return jsonify({'files': files})

@app.route('/file/<filename>')
def get_file_content(filename):
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    if os.path.exists(filepath):
        file_ext = os.path.splitext(filename)[1].lower()
        content = read_file_content(filepath, file_ext)
        return jsonify({'content': content, 'filename': filename})
    return 'File not found', 404
if __name__ == '__main__':
    app.run(debug=True)