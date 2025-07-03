from flask import Blueprint, request, jsonify
from models import Like, db
from flask_login import current_user, login_required

like_bp = Blueprint('like', __name__)

@like_bp.route('/like/<int:post_id>', methods=['POST'])
@login_required
def like_post(post_id):
    existing = Like.query.filter_by(user_id=current_user.id, post_id=post_id).first()
    if existing:
        db.session.delete(existing)
        db.session.commit()
        return jsonify({'message': 'Like removed'})
    else:
        like = Like(user_id=current_user.id, post_id=post_id)
        db.session.add(like)
        db.session.commit()
        return jsonify({'message': 'Post liked'})
