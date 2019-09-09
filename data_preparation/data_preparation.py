from PIL import Image
import cv2
import numpy as np
from flask import Flask
from flask_restful import Resource ,Api ,reqparse
from flask_cors import CORS, cross_origin
from flask_swagger_ui import get_swaggerui_blueprint
from flask import jsonify
import werkzeug
import matplotlib.pyplot as plt
import csv
import biosppy


# ************************** data preparation microservice **************************#
# inputs : real image , coordinates 2 points of V5 , number of pulses inside the V5  #
# outputs : bw.png , cropped* images                                                 #
# ***********************************************************************************#

# --------------------------- TREAT ( 1 ) ---------------------------

# 1- ************* crop the real ecg V5 into 800 * 220 *************

def crop_v5(p1,p2):
    real_img = cv2.imread('static/real.jpg')
    height,width = real_img.shape[:2]
    # print(height,width)

    # start_row, start_col = int(height * 0.72), int(width * .55)  # left top
    # end_row, end_col = int(height * 0.85), int(width * .99)  # buttom right

    start_row, start_col = int(p1[1]), int(p1[0])  # left top
    end_row, end_col = int(p2[1]), int(p2[0])  # buttom right
    cropped = real_img[start_row:end_row, start_col:end_col]

    re = cv2.resize(cropped, (800, 220))  # make it 800 * 220
    cv2.imwrite('static/v5.png', re)


# 2- ************* make the image black and white with pilow *************

def black_white_v5():
    im_name = 'static/v5.png'
    im = Image.open(im_name)
    pixels = list(im.getdata())
    width, height = im.size

    # just let black pixels and replace others with white
    changed_pixels = [pixel if pixel < ( 100, 100, 100) else (255, 255, 255) for pixel in pixels]
    # make it black and white
    changed_pixels = [pixel if pixel==(255, 255, 255) else (0, 0, 0) for pixel in changed_pixels]

    new_im = Image.new("RGB",(width,height))
    new_im.putdata(changed_pixels)
    new_im.save("static/bw.png")

# 3- ************* crop multiple pulses into 128 * 128 with openCV *************

def multiple_images(pulses):
    img = cv2.imread('static/bw.png')
    height,width = img.shape[:2]


    col_padding = 100/pulses/100
    col_parser = 0

    for i in range(pulses):
        start_row, start_col = int(height * 0), int(width * col_parser)  # left top
        end_row, end_col = int(height * 1), int(width * (col_parser+col_padding))  # buttom right
        cropped = img[start_row:end_row, start_col:end_col]

        # make white border
        bordersize = 100
        border = cv2.copyMakeBorder(cropped, top=0, bottom=0, left=bordersize, right=bordersize,borderType=cv2.BORDER_CONSTANT, value=[255, 255, 255])

        #resize 128 * 128
        re = cv2.resize(border,(128,128)) # make it 128 * 128
        
        col_parser+=col_padding

        if(i == 0 or i == pulses-1):
            pass
        else:
            cv2.imwrite('static/cropped' + str(i) + '.png', re)



# --------------------------- TREAT ( 2 ) ---------------------------

# 1- detect peak R

def detect_peak(samp_rate):
    data = np.loadtxt('static/file.txt')
    signals = []
    count = 1
    peaks = biosppy.signals.ecg.christov_segmenter(signal=data, sampling_rate=samp_rate)[0]
    for i in (peaks[1:-1]):
        diff1 = abs(peaks[count - 1] - i)
        diff2 = abs(peaks[count + 1] - i)
        x = peaks[count - 1] + diff1 // 2
        y = peaks[count + 1] - diff2 // 2
        signal = data[x:y]
        signals.append(signal)
        count += 1
    return signals

# 2 - generate multiple images into 128*128 with openCV & matplotlib

def ETI(array):
    count = 0
    # print('nombre de photo : '+str(len(array)))
    for i in array:
        fig = plt.figure(frameon=False)
        plt.plot(i)
        plt.xticks([]), plt.yticks([])
        for spine in plt.gca().spines.values():
            spine.set_visible(False)
        filename = 'static/generate_data/' + str(count) + '.png'
        fig.savefig(filename)
        im_gray = cv2.imread(filename, cv2.IMREAD_GRAYSCALE)
        im_gray = cv2.resize(im_gray, (128, 128), interpolation=cv2.INTER_LANCZOS4)
        cv2.imwrite(filename, im_gray)
        count += 1
        plt.close('all')



########## Flask #########


app = Flask(__name__)

### swagger specific ###
SWAGGER_URL = '/swagger'
API_URL = '/static/swagger.json'
SWAGGERUI_BLUEPRINT = get_swaggerui_blueprint(
    SWAGGER_URL,
    API_URL,
    config={
        'app_name': "Data preparation microservice"
    }
)
app.register_blueprint(SWAGGERUI_BLUEPRINT, url_prefix=SWAGGER_URL)
### end swagger specific ###

cors = CORS(app, resources={r"/*": {"origins": "*"}})

api = Api(app)

# cros config
app.config['CORS_HEADERS'] = 'application/json'



@app.route('/')
def index():
    return jsonify({'message': 'Hello, World!'})

# views

parser = reqparse.RequestParser()

parser.add_argument('real_image',type=werkzeug.datastructures.FileStorage, location='files', help='real_image field cannot be blank', required=True)
parser.add_argument('p2', help='p1 field cannot be blank', required=True)
parser.add_argument('p1', help='p1 field cannot be blank', required=True)
parser.add_argument('pulses',type=int, help='pulses field cannot be blank', required=True)


parser2 = reqparse.RequestParser()

parser2.add_argument('v5',type=werkzeug.datastructures.FileStorage, location='files', help='v5 field cannot be blank', required=True)
parser2.add_argument('pulses',type=int, help='pulses field cannot be blank', required=True)


parser3 = reqparse.RequestParser()

parser3.add_argument('myfile',type=werkzeug.datastructures.FileStorage, location='files', help='file field cannot be blank', required=True)
parser3.add_argument('rate',type=int, help='Sampling rate field cannot be blank', required=True)


# Resources

class Preparation(Resource):
    def post(self):
        data = parser.parse_args()
        # inputs :
        # real_img_name = 'real.jpg'
        # p1 , p2 = (704.0,621.36),(1267.2,733.55)
        # pulses = 6
        real_img_name, p1, p2, pulses = data['real_image'],(float(data['p1'].split(',')[0]),float(data['p1'].split(',')[1])), (float(data['p2'].split(',')[0]),float(data['p2'].split(',')[1])), data['pulses']
        real_img_name.save('static/real.jpg')
        # print(p1,type(p1),p2,type(p2))
        try:
            crop_v5(p1,p2)
        except:
            return jsonify({'message': 'the size of the image is very small'})

        black_white_v5()
        multiple_images(pulses)
        return jsonify({'message': 'success'})


class LightPreparation(Resource):
    def post(self):
        # inputs :
        # v5 = 'v5.png'
        # pulses = 3
        data = parser2.parse_args()
        v5 , pulses = data['v5'], data['pulses']
        v5.save('static/v5.png')
        black_white_v5()
        multiple_images(pulses)
        return jsonify({'message': 'success'})

class File2Image(Resource):
    def post(self):
        # inputs :
        # file = file.txt
        # rate = 1000
        data = parser3.parse_args()
        myfile , samp_rate = data['myfile'], data['rate']
        myfile.save('static/file.txt')
        ETI(detect_peak(samp_rate))
        return jsonify({'message': 'success'})




api.add_resource(Preparation,'/prepare')
api.add_resource(LightPreparation,'/light_prepare')
api.add_resource(File2Image,'/file2image')


if __name__ == '__main__':
    app.run(host='0.0.0.0',debug=True)







