from flask import Flask
from flask import jsonify
from flask_restful import Resource ,Api ,reqparse
from flask_sqlalchemy import SQLAlchemy
from passlib.hash import pbkdf2_sha256
from flask_jwt_extended import JWTManager
from flask_jwt_extended import (create_access_token, create_refresh_token, jwt_required, jwt_refresh_token_required, get_jwt_identity, get_raw_jwt)
from hashlib import sha256
from flask_cors import CORS, cross_origin



app = Flask(__name__)
cors = CORS(app, resources={r"/*": {"origins": "*"}})

api = Api(app)

# cros config
app.config['CORS_HEADERS'] = 'application/json'

# JWT Config

app.config['JWT_SECRET_KEY'] = '4Si_S8A'
jwt = JWTManager(app)


# Token Blacklisting

app.config['JWT_BLACKLIST_ENABLED'] = True
app.config['JWT_BLACKLIST_TOKEN_CHECKS'] = ['access', 'refresh']

@jwt.token_in_blacklist_loader
def check_if_token_in_blacklist(decrypted_token):
    jti = decrypted_token['jti']
    return RevokedTokenModel.is_jti_blacklisted(jti)


# DB Config

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'SuperSecretPasswd'

db = SQLAlchemy(app)

@app.before_first_request
def create_tables():
    db.create_all()


# Models

class UserModel(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(120), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)
    name = db.Column(db.String(255),nullable=False)

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    @classmethod
    def find_by_username(cls, username):
        return cls.query.filter_by(username=username).first()

    @classmethod
    def find_by_email(cls, email):
        return cls.query.filter_by(email=email).first()

    @classmethod
    def return_all(cls):
        def to_json(x):
            return {
                'username': x.username,
                'email': x.email,
                'password': x.password,
                'name' :x.name,
            }

        return {'users': list(map(lambda x: to_json(x), UserModel.query.all()))}

    @classmethod
    def delete_all(cls):
        try:
            num_rows_deleted = db.session.query(cls).delete()
            db.session.commit()
            return {'message': '{} row(s) deleted'.format(num_rows_deleted)}
        except:
            return {'message': 'Something went wrong'}

    @staticmethod
    def generate_hash(password):
        return pbkdf2_sha256.hash(password)

    @staticmethod
    def verify_hash(password, hash):
        return pbkdf2_sha256.verify(password, hash)


 # Blacklisting

class RevokedTokenModel(db.Model):
    __tablename__ = 'revoked_tokens'
    id = db.Column(db.Integer, primary_key=True)
    jti = db.Column(db.String(120))

    def add(self):
        db.session.add(self)
        db.session.commit()

    @classmethod
    def is_jti_blacklisted(cls, jti):
        query = cls.query.filter_by(jti=jti).first()
        return bool(query)

    @classmethod
    def delete_all(cls):
        try:
            num_rows_deleted = db.session.query(cls).delete()
            db.session.commit()
            return {'message': '{} row(s) deleted'.format(num_rows_deleted)}
        except:
            return {'message': 'Something went wrong'}


# views

parser = reqparse.RequestParser()

parser.add_argument('username', help = 'Username field cannot be blank', required = True)
parser.add_argument('email', help = 'Email field cannot be blank', required = True)
parser.add_argument('password', help = 'Password field cannot be blank', required = True)
parser.add_argument('name', help = 'Name field cannot be blank', required = True)

parser_login = reqparse.RequestParser()
parser_login.add_argument('username_email', help = 'Username/Email field cannot be blank', required = True)
parser_login.add_argument('password', help = 'Password field cannot be blank', required = True)


@app.route('/')
def index():
    return jsonify({'message': 'Hello, World!'})
lim

 # Resources

class UserRegistration(Resource):
    def post(self):
        data = parser.parse_args()

        if UserModel.find_by_username(data['username']):
            return {'message': 'Username {} already exists'.format(data['username'])}
        if UserModel.find_by_email(data['email']):
            return {'message': 'Email {} already exists'.format(data['email'])}


        new_user = UserModel(
            username=data['username'],
            email=data['email'],
            password=UserModel.generate_hash(data['password']), # hashpass change randomlly
            name=data['name']
        )
        try:
            new_user.save_to_db()
            access_token = create_access_token(identity=data['username']+","+data['name']+","+data['email'])
            refresh_token = create_refresh_token(identity=data['username']+","+data['name']+","+data['email'])
            return {
                'message': 'User {} was created'.format(data['username']),
                'access_token': access_token,
                'refresh_token': refresh_token
                }
        except:
            return {'message': 'Something went wrong'}, 500


class UserLogin(Resource):
    def post(self):
        data = parser_login.parse_args()

        if("@" in data['username_email']):
            current_user = UserModel.find_by_email(data['username_email'])
            if not current_user:
                return {'message': 'Email {} doesn\'t exist'.format(data['username_email'])}
        else:
            current_user = UserModel.find_by_username(data['username_email'])
            if not current_user:
                return {'message': 'Username {} doesn\'t exist'.format(data['username_email'])}

        if UserModel.verify_hash(data['password'], current_user.password):
            access_token = create_access_token(identity=current_user.username + "," + current_user.name + "," + current_user.email)
            refresh_token = create_refresh_token(identity=current_user.username + "," + current_user.name + "," + current_user.email)
            return {'message': 'Logged in as {}'.format(current_user.username),
                    'access_token': access_token,
                    'refresh_token': refresh_token
                    }
        else:
            return {'message': 'Wrong credentials'}

class UserLogoutAccess(Resource):
    @jwt_required
    def post(self):
        jti = get_raw_jwt()['jti']
        try:
            revoked_token = RevokedTokenModel(jti=jti)
            revoked_token.add()
            return {'message': 'Access token has been revoked'}
        except:
            return {'message': 'Something went wrong'}, 500




class UserLogoutRefresh(Resource):
    @jwt_refresh_token_required
    def post(self):
        jti = get_raw_jwt()['jti']
        try:
            revoked_token = RevokedTokenModel(jti=jti)
            revoked_token.add()
            return {'message': 'Refresh token has been revoked'}
        except:
            return {'message': 'Something went wrong'}, 500




class TokenRefresh(Resource):
    @jwt_refresh_token_required
    def post(self):
        current_user = get_jwt_identity()
        access_token = create_access_token(identity=current_user)
        return {'access_token': access_token}

class AllUsers(Resource):
    def get(self):
        return UserModel.return_all()


    def delete(self):
        return UserModel.delete_all()


class SecretResource(Resource):
    @jwt_required
    def get(self):
        # Access the identity of the current user with get_jwt_identity
        current_user = get_jwt_identity()  # username name email
        return {'username':current_user.split(',')[0],'name':current_user.split(',')[1],'email':current_user.split(',')[2]}, 200


api.add_resource(UserRegistration, '/register')
api.add_resource(UserLogin, '/login')
api.add_resource(UserLogoutAccess, '/logout/access')
api.add_resource(UserLogoutRefresh, '/logout/refresh')
api.add_resource(TokenRefresh, '/token/refresh')
api.add_resource(AllUsers, '/users')
api.add_resource(SecretResource, '/profil')


if __name__ == '__main__':
    app.run(debug=True)