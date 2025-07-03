from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_bcrypt import Bcrypt
from dotenv import load_dotenv
from models import db



from views.auth import auth_bp  
from views.comment import comment_bp
from views.like import like_bp
from views.post import post_bp
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

    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)
    bcrypt.init_app(app)


    app.register_blueprint(auth_bp)
    app.register_blueprint(comment_bp)
    app.register_blueprint(like_bp)
    app.register_blueprint(tag_bp)
    app.register_blueprint(post_bp)
    app.register_blueprint(category_bp)
    app.register_blueprint(notification_bp)

    

    return app 

app = create_app() 

if __name__ == "__main__":
    app = create_app() 
    app.run(debug=True)
