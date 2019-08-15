from PIL import Image
import cv2
import numpy as np
from flask import Flask
from flask_restful import Resource ,Api ,reqparse
from flask_cors import CORS, cross_origin
from flask_swagger_ui import get_swaggerui_blueprint
from flask import jsonify
import werkzeug


# ************************** data preparation microservice **************************#
# inputs : real image , coordinates 2 points of V5 , number of pulses inside the V5  #
# outputs : bw.png , cropped* images                                                 #
# ***********************************************************************************#



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
    changed_pixels = [pixel if pixel < ( 120, 120, 120) else (255, 255, 255) for pixel in pixels]
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
        re = cv2.resize(cropped,(128,128)) # make it 128 * 128
        cv2.imwrite('static/cropped'+str(i)+'.png', re)
        col_parser+=col_padding




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



api.add_resource(Preparation,'/prepare')


if __name__ == '__main__':
    app.run(debug=True,port=5001)







