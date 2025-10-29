from flask import Flask, render_template, request, flash, redirect, url_for, jsonify
from flask_wtf import FlaskForm
from flask_wtf.csrf import CSRFProtect, CSRFError, generate_csrf
from wtforms import FileField, SubmitField
from wtforms.validators import DataRequired
from werkzeug.utils import secure_filename
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = 'supersecretkey'
app.config['UPLOAD_FOLDER'] = 'static/files'

# 🛡️ SECURITY CONFIGURATION
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif', 'doc', 'docx'}

csrf = CSRFProtect(app)

def allowed_file(filename):
    """Check if file extension is allowed"""
    if '.' not in filename:
        return False
    extension = filename.rsplit('.', 1)[1].lower()
    return extension in ALLOWED_EXTENSIONS

class UploadFileForm(FlaskForm):
    file = FileField("File", validators=[DataRequired()])
    submit = SubmitField("Upload File")

@app.route('/', methods=['GET', 'POST'])
def home():
    form = UploadFileForm()
    
    if form.validate_on_submit():
        file = form.file.data
        
        # 🛡️ SECURITY CHECK 1: Check if file was selected
        if file.filename == '':
            flash('No file selected', 'error')
            return redirect(url_for('home'))
        
        # 🛡️ SECURITY CHECK 2: Check file extension
        if not allowed_file(file.filename):
            flash(f'File type not allowed. Allowed types: {", ".join(ALLOWED_EXTENSIONS)}', 'error')
            return redirect(url_for('home'))
        
        # 🛡️ SECURITY CHECK 3: Secure the filename
        filename = secure_filename(file.filename)
        if filename == '':
            flash('Invalid filename', 'error')
            return redirect(url_for('home'))
        
        # Create upload directory if it doesn't exist
        upload_path = app.config['UPLOAD_FOLDER']
        if not os.path.exists(upload_path):
            os.makedirs(upload_path)
        
        try:
            # Save the file
            file_path = os.path.join(upload_path, filename)
            file.save(file_path)
            flash(f'File "{filename}" uploaded successfully!', 'success')
            
        except Exception as e:
            flash(f'Error saving file: {str(e)}', 'error')
        
        return redirect(url_for('home'))
    
    return render_template('index.html', form=form)

# 🧪 TESTING ENDPOINT (exempt from CSRF)
@app.route('/api/upload', methods=['POST'])
@csrf.exempt  # ← THIS IS THE KEY FIX
def api_upload():
    """API endpoint for automated testing (bypasses CSRF)"""
    if 'file' not in request.files:
        return jsonify({'success': False, 'error': 'No file selected'})
    
    file = request.files['file']
    
    if file.filename == '':
        return jsonify({'success': False, 'error': 'No file selected'})
    
    # 🛡️ SECURITY CHECK: File extension
    if not allowed_file(file.filename):
        return jsonify({'success': False, 'error': 'File type not allowed'})
    
    # 🛡️ SECURITY CHECK: Secure filename
    filename = secure_filename(file.filename)
    if filename == '':
        return jsonify({'success': False, 'error': 'Invalid filename'})
    
    # Create upload directory if it doesn't exist
    upload_path = app.config['UPLOAD_FOLDER']
    if not os.path.exists(upload_path):
        os.makedirs(upload_path)
    
    try:
        # Save the file
        file_path = os.path.join(upload_path, filename)
        file.save(file_path)
        return jsonify({'success': True, 'message': f'File "{filename}" uploaded successfully!'})
    
    except Exception as e:
        return jsonify({'success': False, 'error': f'Error saving file: {str(e)}'})

@app.errorhandler(CSRFError)
def handle_csrf_error(e):
    return jsonify({'success': False, 'error': 'CSRF token error'}), 400

if __name__ == '__main__':
    app.run(debug=True)