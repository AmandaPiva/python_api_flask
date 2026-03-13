from http import HTTPStatus
from flask import Blueprint, request

from src.Entities import user
from src.Entities.user import User
from src.app import db
from flask_jwt_extended import jwt_required
from flask_jwt_extended import get_jwt_identity

#definindo a url padrao
app = Blueprint('user', __name__, url_prefix='/users')

def _create_user():
    data = request.json
    user = User(
        username=data['username'],
        password=data['password'],
        role_id=data['role_id'],
    )
    db.session.add(user)
    db.session.commit()

def _list_users():
    query = db.select(User)
    users = db.session.execute(query).scalars()
    return [
        {
            "id": user.id,
            "username": user.username,
            "role_id": user.role_id,
            "role": user.role.name if user.role else None
        }
        for user in users
    ]

@app.route('/', methods=['GET','POST'])
@jwt_required()
def handle_user():
    user_id = get_jwt_identity()
    user = db.get_or_404(User, user_id)

    if user.roles.name != 'admin':
        return {"message": "User dont have access"}, HTTPStatus.FORBIDDEN

    if request.method == 'POST':
        _create_user() #chamamos o método que adicionará o user no banco
        return {"message": "Usuário criado"}, HTTPStatus.CREATED
    else:
        return {"users": _list_users()}
    


@app.route('/<int:user_id>', methods=['PATCH'])
@jwt_required()
def update_user(user_id):
    user = db.get_or_404(User, user_id)
    data = request.json
    user.username = data['username']
    user.role_id = data['role_id']
    db.session.commit()

    return {
        "id": user.id,
        "username": user.username
    }

@app.route('/<int:user_id>', methods=['GET'])
@jwt_required()
def get_user(user_id):
    user = db.get_or_404(User, user_id)
    return {
        "id": user.id,
        "username": user.username
    }

@app.route('/<int:user_id>', methods=['DELETE'])
@jwt_required()
def delete_user(user_id):
    user = db.get_or_404(User, user_id)
    db.session.delete(user)
    db.session.commit()

    return {"message": "Usuário deletado"}, HTTPStatus.NO_CONTENT