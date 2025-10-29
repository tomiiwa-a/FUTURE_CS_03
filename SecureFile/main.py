from flask import Flask, render_template, request, flash, redirect, url_for
from flask_wtf import FlaskForm
from flask_wtf.csrf import CSRFProtect  # ← ADD THIS
from wtforms import FileField, SubmitField 
from werkzeug.utils import secure_filename
import os
from wtforms.validators import InputRequired

app = Flask(__name__)
app.config['SECRET_KEY'] = 'supersecretkey'
app.config['UPLOAD_FOLDER'] = 'static/files'

# Initialize CSRF protection
csrf = CSRFProtect(app)  # ← ADD THIS

class UploadFileForm(FlaskForm):
    file = FileField("File", validators=[InputRequired()])
    submit = SubmitField("Upload File") 

@app.route('/', methods=['GET', 'POST'])
@app.route('/home', methods=['GET', 'POST'])
def home():
    form = UploadFileForm()
    
    if form.validate_on_submit():
        file = form.file.data
        
        # Create upload directory if it doesn't exist
        if not os.path.exists(app.config['UPLOAD_FOLDER']):
            os.makedirs(app.config['UPLOAD_FOLDER'])
        
        # Save the file
        filename = secure_filename(file.filename)
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(file_path)
        
        flash(f'File "{filename}" uploaded successfully!', 'success')
        return redirect(url_for('home'))
    
    return render_template('index.html', form=form)

if __name__ == '__main__':
    app.run(debug=True)