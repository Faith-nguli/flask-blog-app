from flask import Blueprint, request, jsonify
from models import Comment, db
from flask_login import current_user, login_required

comment_bp = Blueprint('comment', __name__)

@comment_bp.route('/comments', methods=['POST'])
@login_required
def add_comment():
    data = request.get_json()
    comment = Comment(content=data['content'], user_id=current_user.id, post_id=data['post_id'])
    db.session.add(comment)
    db.session.commit()
    return jsonify({'message': 'Comment added'})
