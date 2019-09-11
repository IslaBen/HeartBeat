from __future__ import division, print_function
import os
import glob
import numpy as np
from keras.models import load_model
from keras.preprocessing import image
from flask import Flask, request
from werkzeug.utils import secure_filename
from flask import jsonify
import shutil
from glob import glob

# Define a flask app
app = Flask(__name__)

# Model saved with Keras model.save()
MODEL_PATH = 'models/best_modelT.h5'

# Load your trained model
model = load_model(MODEL_PATH)
model._make_predict_function()
print('Model loaded. Start serving...')

modelENE = load_model('models/modelT.h5')
modelENE._make_predict_function()


def isECG_Img(img_path, modelE):
    img = image.load_img(img_path, target_size=(128, 128), color_mode="grayscale")

    # Preprocessing the image
    x = image.img_to_array(img)
    x = np.array(x)
    x = np.expand_dims(x, axis=0)

    preds = modelE.predict(x)
    print(preds)

    val = 0
    somme = 0
    for x in np.nditer(preds):
        somme += x

    for x in np.nditer(preds):
        val = x / somme
        break
    print(val)

    if val < 0.8:
        return False
    else:
        return True


def model_predict(img_path, model):
    img = image.load_img(img_path, target_size=(128, 128), color_mode="grayscale")

    # Preprocessing the image
    x = image.img_to_array(img)
    x = np.array(x)
    x = np.expand_dims(x, axis=0)

    #make prediction
    preds = model.predict(x)
    return preds


@app.route('/predict', methods=['POST'])
def upload():
    data1 = {}
    data2 = []
    result = {}
    # Get the file from post request
    f = request.files['data']

    # Save the file to ./uploads
    basepath = os.path.dirname(__file__)
    file_path = os.path.join(basepath, 'uploads', secure_filename('data.zip'))
    f.save(file_path)
    # extract the file
    shutil.unpack_archive('uploads/data.zip', extract_dir="extracted")

    n = 0
    ty = ['A', 'L', 'N', 'P', 'R', 'V']
    paths = glob('extracted/*.png')
    for path in paths:
        print(path)
        # test if the image is a ECG signal image or not
        if (isECG_Img(path, modelENE)):
            # Make prediction
            preds = model_predict(path, model)
            # Process your result for human
            somme = 0
            for x in np.nditer(preds):
                somme += x
            i = 0
            for x in np.nditer(preds):
                data1[ty[i]] = round(x / somme * 100, 3)
                i += 1
            data2.append(data1.copy())
            n = n + 1

    # claculat the avg of %
    for elm1 in ty:
        result[elm1] = 0
    for elm2 in data2:
        for i in range(6):
            result[ty[i]] += elm2[ty[i]]
    for elm1 in ty:
        result[elm1] /= n

    # if there is no images of ECG signal
    if n == 0:
        result = {"error": "the image is not an ECG image"}

    # delete the extracted directory
    shutil.rmtree('extracted')
    return jsonify(result)


if __name__ == '__main__':
    # Serve the app
    app.run(debug=True, host='0.0.0.0')
