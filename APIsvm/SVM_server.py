import os
import shutil
from glob import glob
from flask import Flask, request
import werkzeug
import SVM_project

UPLOAD_FOLDER = 'uploads'

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


def allowed_file(filename):
    return filename[-3:].lower() in {'zip'}


def get_final_result(results):
    final_result = {'A': 0, 'L': 0, 'N': 0, 'R': 0, 'V': 0}
    for result in results:
        for key in final_result:
            final_result[key] = result[key] + final_result[key]
    for key in final_result:
        final_result[key] /= results.__len__()
    final_result['P'] = 0.0
    for key, value in final_result.items():
        final_result[key] = value * 0.98
        final_result[key] = round(final_result[key], 2)
    return final_result


@app.route('/predict', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        file = request.files['data']
        if file and allowed_file(file.filename):
            basePath = os.path.dirname(__file__)
            file_path = os.path.join(basePath, 'uploads', werkzeug.secure_filename('data.zip'))
            file.save(file_path)
            shutil.unpack_archive('uploads/data.zip', extract_dir='extracted_files')
            paths = glob('extracted_files/*.txt')
            result = []
            for path in paths:
                result.append(SVM_project.main_function(path, 360))
            #  remove files to avoid confusing with the next prediction
            shutil.rmtree('extracted_files')
            os.remove('uploads/data.zip')
            return get_final_result(result)
    return '''
        <title>Upload new File</title>
        <h1>Upload new File</h1>
        <form action="" method=post enctype=multipart/form-data>
            <input type=file name=file>
            <input type=submit value=Upload>
        </form>
    '''


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
