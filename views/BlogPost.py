from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from datetime import datetime
from app import db
from models import BlogPost, User, Tag  

blogpost_bp = Blueprint('blogpost', __name__)


@blogpost_bp.route('/posts', methods=['POST'])
@jwt_required()
def create_post():
    data = request.get_json()
    title = data.get('title')
    content = data.get('content')
    status = data.get('status', 'draft')
    user_id = get_jwt_identity()

    if not title or not content:
        return jsonify({'error': 'Title and content are required'}), 400

    post = BlogPost(title=title, content=content, status=status, author_id=user_id)
    db.session.add(post)
    db.session.commit()

    return jsonify({'message': 'Post created successfully', 'post_id': post.id}), 201


@blogpost_bp.route('/posts', methods=['GET'])
def get_all_posts():
    posts = blogpost_bp.query.order_by(blogpost_bp.created_at.desc()).all()
    return jsonify([
        {
            'id': post.id,
            'title': post.title,
            'content': post.content,
            'status': post.status,
            'author_id': post.author_id,
            'created_at': post.created_at.isoformat()
        } for post in posts
    ])


@blogpost_bp.route('/posts/<int:post_id>', methods=['GET'])
def get_single_post(post_id):
    post = blogpost_bp.query.get_or_404(post_id)
    return jsonify({
        'id': post.id,
        'title': post.title,
        'content': post.content,
        'status': post.status,
        'author_id': post.author_id,
        'created_at': post.created_at.isoformat()
    })


@blogpost_bp.route('/posts/<int:post_id>', methods=['PUT'])
@jwt_required()
def update_post(post_id):
    user_id = get_jwt_identity()
    post = blogpost_bp.query.get_or_404(post_id)

    if post.author_id != user_id:
        return jsonify({'error': 'You can only edit your own posts'}), 403

    data = request.get_json()
    post.title = data.get('title', post.title)
    post.content = data.get('content', post.content)
    post.status = data.get('status', post.status)
    db.session.commit()

    return jsonify({'message': 'Post updated successfully'})


@blogpost_bp.route('/posts/<int:post_id>', methods=['DELETE'])
@jwt_required()
def delete_post(post_id):
    user_id = get_jwt_identity()
    post = blogpost_bp.query.get_or_404(post_id)

    if post.author_id != user_id:
        return jsonify({'error': 'You can only delete your own posts'}), 403

    db.session.delete(post)
    db.session.commit()

    return jsonify({'message': 'Post deleted successfully'})

