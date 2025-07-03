from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from datetime import datetime

db = SQLAlchemy()


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)  
    username = db.Column(db.String(150), unique=True, nullable=False)
    email = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(256), nullable=False)
    role = db.Column(db.String(20), default='reader') 
    profile_image = db.Column(db.String(200), nullable=True, default='default.jpg')

    
    # One-to-many: A user can write many posts
    posts = db.relationship('BlogPost', backref='author', lazy=True)
    comments = db.relationship('Comment', backref='user', lazy=True)
    likes = db.relationship('Like', backref='user', lazy=True)


class BlogPost(db.Model):
    __tablename__ = 'blog_post'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    content = db.Column(db.Text, nullable=False)
    status = db.Column(db.String(20), default='draft')  
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    author_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    
    # Relationships
    comments = db.relationship('Comment', backref='post', lazy=True)
    likes = db.relationship('Like', backref='post', lazy=True)
    tags = db.relationship('Tag', secondary='post_tags', backref='posts', lazy='dynamic')

class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False, unique=True)



class Tag(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)


post_tags = db.Table('post_tags',
    db.Column('post_id', db.Integer, db.ForeignKey('blog_post.id')),
    db.Column('tag_id', db.Integer, db.ForeignKey('tag.id'))
)


class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    post_id = db.Column(db.Integer, db.ForeignKey('blog_post.id'), nullable=False)


class Like(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    post_id = db.Column(db.Integer, db.ForeignKey('blog_post.id'), nullable=False)


class Notification(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    message = db.Column(db.String(200), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    is_read = db.Column(db.Boolean, default=False)

    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))


class SiteSettings(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    site_name = db.Column(db.String(100), default='My Blog')
    maintenance_mode = db.Column(db.Boolean, default=False)
