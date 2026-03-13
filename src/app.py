import os

import click
from flask import Flask, current_app
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager


#configurando o banco
class Base(DeclarativeBase):
    pass

db = SQLAlchemy(model_class=Base)
migrate = Migrate()

jwt = JWTManager()

#aaa


@click.command('init-db')
def init_db_command():
    """Clear the existing data and create new tables."""
    global db
    with current_app.app_context():
        db.create_all()
    click.echo('Initialized the database.')

#criando a aplicação
def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    
    app.config.from_mapping(
        SECRET_KEY='dev',
        SQLALCHEMY_DATABASE_URI='sqlite:///bank.sqlite',
        JWT_SECRET_KEY="super-secret"
    )

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    app.cli.add_command(init_db_command)
    db.init_app(app) #inicializando o banco de dados
    migrate.init_app(app, db)
    jwt.init_app(app)



    from src.Controllers.user import app as user_blueprint
    from src.Controllers.auth import app as auth_blueprint
    from src.Controllers.role import app as role_blueprint
    app.register_blueprint(user_blueprint)
    app.register_blueprint(auth_blueprint)
    app.register_blueprint(role_blueprint)


    return app