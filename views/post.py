from flask import Blueprint, request, jsonify
from flask_login import current_user, login_required
from models import BlogPost, db

post_bp = Blueprint('post', __name__)

# Get all posts
@post_bp.route('/posts', methods=['GET'])
def get_posts():
    posts = BlogPost.query.all()
    return jsonify([
        {
            'id': post.id,
            'title': post.title,
            'content': post.content,
            'author': post.author.username,
            'created_at': post.created_at
        } for post in posts
    ])

# Get a single post
@post_bp.route('/posts/<int:post_id>', methods=['GET'])
def get_post(post_id):
    post = BlogPost.query.get_or_404(post_id)
    return jsonify({
        'id': post.id,
        'title': post.title,
        'content': post.content,
        'author': post.author.username,
        'created_at': post.created_at
    })

# Create a new post
@post_bp.route('/posts', methods=['POST'])
@login_required
def create_post():
    data = request.get_json()
    new_post = BlogPost(
        title=data['title'],
        content=data['content'],
        author_id=current_user.id
    )
    db.session.add(new_post)
    db.session.commit()
    return jsonify({'message': 'Post created successfully'}), 201

# Update a post
@post_bp.route('/posts/<int:post_id>', methods=['PUT'])
@login_required
def update_post(post_id):
    post = BlogPost.query.get_or_404(post_id)
    if post.author_id != current_user.id:
        return jsonify({'error': 'Unauthorized'}), 403

    data = request.get_json()
    post.title = data.get('title', post.title)
    post.content = data.get('content', post.content)
    db.session.commit()
    return jsonify({'message': 'Post updated'})

# Delete a post
@post_bp.route('/posts/<int:post_id>', methods=['DELETE'])
@login_required
def delete_post(post_id):
    post = BlogPost.query.get_or_404(post_id)
    if post.author_id != current_user.id:
        return jsonify({'error': 'Unauthorized'}), 403

    db.session.delete(post)
    db.session.commit()
    return jsonify({'message': 'Post deleted'})
