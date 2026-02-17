from flask import Blueprint, request, jsonify
from app.services.recommendation_engine import RecommendationEngine

bp = Blueprint('recommendations', __name__, url_prefix='/api/recommendations')

recommendation_engine = RecommendationEngine()

@bp.route('/personalized', methods=['GET'])
def get_personalized_recommendations():
    """Get personalized recommendations for user"""
    user_id = request.args.get('user_id', 'default_user')
    current_items = request.args.getlist('items')
    
    recommendations = recommendation_engine.get_recommendations(user_id, current_items)
    
    return jsonify({
        'user_id': user_id,
        'recommendations': recommendations,
        'count': len(recommendations)
    })

@bp.route('/alternatives', methods=['POST'])
def get_alternatives():
    """Get alternative products for an item"""
    data = request.json
    item = data.get('item', '')
    
    if not item:
        return jsonify({'error': 'Item is required'}), 400
    
    alternatives = recommendation_engine.get_substitute_products(item)
    
    return jsonify({
        'item': item,
        'alternatives': alternatives,
        'count': len(alternatives)
    })

@bp.route('/price-range', methods=['GET'])
def get_price_range():
    """Get price range for an item"""
    item = request.args.get('item', '')
    
    if not item:
        return jsonify({'error': 'Item is required'}), 400
    
    price_data = recommendation_engine.get_price_range_by_item(item)
    
    return jsonify({
        'item': item,
        'price_range': price_data
    })

@bp.route('/record-purchase', methods=['POST'])
def record_purchase():
    """Record purchase for recommendation tracking"""
    data = request.json
    user_id = data.get('user_id', 'default_user')
    items = data.get('items', [])
    
    if not items:
        return jsonify({'error': 'Items are required'}), 400
    
    recommendation_engine.record_purchase(user_id, items)
    
    return jsonify({
        'success': True,
        'message': 'Purchase recorded'
    })

@bp.route('/seasonal', methods=['GET'])
def get_seasonal():
    """Get seasonal recommendations"""
    recommendations = recommendation_engine._get_seasonal_recommendations()
    
    return jsonify({
        'recommendations': recommendations,
        'count': len(recommendations)
    })
