from http import HTTPStatus
from flask import Blueprint, request

from src.Entities import user
from src.Entities.user import User
from src.app import db
from flask_jwt_extended import create_access_token


app = Blueprint('auth', __name__, url_prefix='/auth')

@app.route('/login', methods=['POST'])
def login():
    username = request.json.get('username', None)
    password = request.json.get('password', None)
    user = db.session.execute(db.select(User).where(User.username == username)).scalar()

    if not user or user.password != password:
        return {"message": "Invalid credentials"}, HTTPStatus.UNAUTHORIZED
    
    access_token = create_access_token(identity=username)
    return {"access_token": access_token}