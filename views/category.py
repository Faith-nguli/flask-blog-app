from flask import Blueprint, request, jsonify
from models import db, Category

category_bp = Blueprint('category', __name__)

@category_bp.route('/categories', methods=['POST'])
def add_category():
    data = request.get_json()
    new_category = Category(name=data['name'])
    db.session.add(new_category)
    db.session.commit()
    return jsonify({'message': 'Category added'})


@category_bp.route('/categories', methods=['GET'])
def list_categories():
    categories = Category.query.all()
    return jsonify([c.name for c in categories])
