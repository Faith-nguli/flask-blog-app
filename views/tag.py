from flask import Blueprint, request, jsonify
from models import Tag, db

tag_bp = Blueprint('tag', __name__)

@tag_bp.route('/tags', methods=['GET'])
def get_tags():
    tags = Tag.query.all()
    return jsonify([tag.name for tag in tags])


@tag_bp.route('/tags', methods=['POST'])
def add_tag():
    data = request.get_json()
    new_tag = Tag(name=data['name'])
    db.session.add(new_tag)
    db.session.commit()
    return jsonify({'message': 'Tag added successfully'})
