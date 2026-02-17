from flask import Blueprint, request, jsonify
import uuid
from app.models.shopping_list import ShoppingList, ShoppingItem
from app.services.nlp_processor import NLPProcessor

bp = Blueprint('shopping', __name__, url_prefix='/api/shopping')

# In-memory storage (replace with database in production)
shopping_lists = {}
nlp = NLPProcessor()

@bp.route('/list', methods=['GET'])
def get_shopping_list():
    """Get user's shopping list"""
    user_id = request.args.get('user_id', 'default_user')
    
    if user_id not in shopping_lists:
        shopping_list = ShoppingList(
            id=str(uuid.uuid4()),
            user_id=user_id
        )
        shopping_lists[user_id] = shopping_list
    
    return jsonify(shopping_lists[user_id].to_dict())

@bp.route('/add', methods=['POST'])
def add_item():
    """Add item to shopping list using voice command"""
    data = request.json
    user_id = data.get('user_id', 'default_user')
    command = data.get('command', '')
    
    if not command:
        return jsonify({'error': 'Command is required'}), 400
    
    # Process natural language command
    nlp_result = nlp.process_command(command)
    
    if nlp_result['intent'] not in ['ADD', 'UNKNOWN']:
        return jsonify({'error': 'Invalid command for adding items'}), 400
    
    if not nlp_result['items']:
        return jsonify({'error': 'No items found in command'}), 400
    
    # Create shopping list if doesn't exist
    if user_id not in shopping_lists:
        shopping_lists[user_id] = ShoppingList(
            id=str(uuid.uuid4()),
            user_id=user_id
        )
    
    # Add items to shopping list
    added_items = []
    for item_name in nlp_result['items']:
        item = ShoppingItem(
            id=str(uuid.uuid4()),
            name=item_name,
            quantity=nlp_result['quantity'][0],
            unit=nlp_result['quantity'][1],
            category=nlp_result['category'] or 'uncategorized'
        )
        shopping_lists[user_id].add_item(item)
        added_items.append(item.to_dict())
    
    return jsonify({
        'success': True,
        'message': f'Added {len(added_items)} item(s)',
        'items': added_items,
        'shopping_list': shopping_lists[user_id].to_dict()
    })

@bp.route('/remove', methods=['POST'])
def remove_item():
    """Remove item from shopping list"""
    data = request.json
    user_id = data.get('user_id', 'default_user')
    item_id = data.get('item_id')
    
    if not item_id:
        return jsonify({'error': 'Item ID is required'}), 400
    
    if user_id not in shopping_lists:
        return jsonify({'error': 'User has no shopping list'}), 404
    
    shopping_lists[user_id].remove_item(item_id)
    
    return jsonify({
        'success': True,
        'message': 'Item removed',
        'shopping_list': shopping_lists[user_id].to_dict()
    })

@bp.route('/clear', methods=['POST'])
def clear_list():
    """Clear entire shopping list"""
    data = request.json
    user_id = data.get('user_id', 'default_user')
    
    if user_id in shopping_lists:
        shopping_lists[user_id].items = []
    
    return jsonify({
        'success': True,
        'message': 'Shopping list cleared'
    })

@bp.route('/category/<category>', methods=['GET'])
def get_by_category(category):
    """Get items by category"""
    user_id = request.args.get('user_id', 'default_user')
    
    if user_id not in shopping_lists:
        return jsonify({'items': []})
    
    items = shopping_lists[user_id].get_by_category(category)
    
    return jsonify({
        'category': category,
        'items': [item.to_dict() for item in items],
        'total_items': len(items)
    })
