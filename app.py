from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_bcrypt import Bcrypt
from dotenv import load_dotenv
from flask_jwt_extended import JWTManager, jwt_required
from blacklist import blacklist
from models import db



from views.auth import auth_bp  
from views.comment import comment_bp
from views.like import like_bp
from views.BlogPost import blogpost_bp
from views.category import category_bp
from views.tag import tag_bp
from views.notification import notification_bp


import os
import models


migrate = Migrate()
login_manager = LoginManager()
bcrypt = Bcrypt()





def create_app():
    load_dotenv()

    app = Flask(__name__)
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL', 'sqlite:///blog.db')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    app.config['JWT_SECRET_KEY'] = os.getenv('JWT_SECRET_KEY')


    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)
    bcrypt.init_app(app)

    jwt = JWTManager(app)

    @jwt.token_in_blocklist_loader
    def check_if_token_revoked(jwt_header, jwt_payload):
        jti = jwt_payload["jti"]  # jti = token's unique ID
        return jti in blacklist
    
    @app.route('/protected', methods=['GET'])
    @jwt_required()
    def protected():
        return jsonify(message="You are logged in!"), 200


    app.register_blueprint(auth_bp)
    app.register_blueprint(comment_bp)
    app.register_blueprint(like_bp)
    app.register_blueprint(tag_bp)
    app.register_blueprint(blogpost_bp)
    app.register_blueprint(category_bp)
    app.register_blueprint(notification_bp)

    

    return app 

app = create_app() 

if __name__ == "__main__":
    app = create_app() 
    app.run(debug=True)
