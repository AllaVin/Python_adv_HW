# ++++++++++++++++++++++++++++++++++++++++++++++++++++++
# The file with descriptions of all API endpoints
# Each route is the functions, wich reacts to your request
# ++++++++++++++++++++++++++++++++++++++++++++++++++++++

from flask import request, jsonify, Blueprint
# from Home_Works.HW_5.models import db, Category, Question
from .models import db, Category, Question

api = Blueprint('api', __name__)

@api.route('/categories', methods=['POST'])
def create_category():
    print("Raw data:", request.data)
    print("JSON:", request.get_json(force=True, silent=True))

    data = request.get_json(force=True)
    if not data or 'name' not in data:
        return jsonify({'error': 'Name is required'}), 400

    new_category = Category(name=data['name'])
    db.session.add(new_category)
    db.session.commit()
    return jsonify({'id': new_category.id, 'name': new_category.name}), 201


@api.route('/categories', methods=['GET'])
def get_categories():
    categories = Category.query.all()
    return jsonify([{'id': c.id, 'name': c.name} for c in categories])


# @api.route('/categories/<int:category_id>', methods=['PUT'])
# def update_category(category_id):
#     data = request.get_json()
#     category = Category.query.get_or_404(category_id)
#     name = data.get('name')
#     if not name:
#         return jsonify({'error': 'Name is required'}), 400
#     category.name = name
#     db.session.commit()
#     return jsonify({'id': category.id, 'name': category.name})
#
#
# @api.route('/categories/<int:category_id>', methods=['DELETE'])
# def delete_category(category_id):
#     category = Category.query.get_or_404(category_id)
#     db.session.delete(category)
#     db.session.commit()
#     return jsonify({'message': 'Category deleted'})

@api.route('/questions', methods=['POST'])
def create_question():
    data = request.get_json()
    if not data or 'text' not in data or 'category_id' not in data:
        return jsonify({'error': 'Text and category_id are required'}), 400
    category = Category.query.get(data['category_id'])
    if not category:
        return jsonify({'error': 'Category not found'}), 404
    question = Question(text=data['text'], category_id=data['category_id'])
    db.session.add(question)
    db.session.commit()
    return jsonify({'id': question.id, 'text': question.text, 'category_id': question.category_id}), 201

@api.route('/questions', methods=['GET'])
def get_question():
    questions = Question.query.all()
    return jsonify([
        {'id': q.id, 'text': q.text, 'category_id': q.category_id}
        for q in questions
    ])
