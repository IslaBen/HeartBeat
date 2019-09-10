import os
from flask import Flask, request, url_for, send_from_directory
import werkzeug
import SVM_project

UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'txt'}

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


def allowed_file(filename):
    # this has changed from the original example because the original did not work for me
    return filename[-3:].lower() in ALLOWED_EXTENSIONS


@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        file = request.files['file']
        if file and allowed_file(file.filename):
            filename = werkzeug.secure_filename(file.filename)
            file.save('uploads/' + filename)
            x = SVM_project.main_function(file_path='uploads/' + filename)
            return x
    return '''
        <title>Upload new File</title>
        <h1>Upload new File</h1>
        <form action="" method=post enctype=multipart/form-data>
            <input type=file name=file>
            <input type=submit value=Upload>
        </form>
    '''


# @app.route('/uploads/<filename>')
# def uploaded_file(filename):
#     print(filename)
#     SVM_project.main_function(file_path='uploads/' + filename)
#     return "done"


if __name__ == '__main__':
    app.run(debug=True)
