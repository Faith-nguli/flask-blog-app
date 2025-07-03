from flask import Blueprint, jsonify
from models import Notification
from flask_login import current_user, login_required

notification_bp = Blueprint('notification', __name__)

@notification_bp.route('/notifications', methods=['GET'])
@login_required
def get_notifications():
    notifs = Notification.query.filter_by(user_id=current_user.id).all()
    return jsonify([
        {
            'message': n.message,
            'is_read': n.is_read,
            'created_at': n.created_at
        } for n in notifs
    ])
