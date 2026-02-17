from flask import Blueprint, request, jsonify
from app.services.nlp_processor import NLPProcessor

bp = Blueprint('voice', __name__, url_prefix='/api/voice')

nlp = NLPProcessor()

@bp.route('/process-command', methods=['POST'])
def process_command():
    """Process voice command"""
    data = request.json
    command = data.get('command', '')
    language = data.get('language', 'en')
    
    if not command:
        return jsonify({'error': 'Command is required'}), 400
    
    result = nlp.process_command(command)
    
    return jsonify({
        'command': command,
        'language': language,
        'processed': result
    })

@bp.route('/extract-items', methods=['POST'])
def extract_items():
    """Extract items from natural language"""
    data = request.json
    text = data.get('text', '')
    
    if not text:
        return jsonify({'error': 'Text is required'}), 400
    
    items = nlp._extract_items(text)
    categories = [nlp._categorize_item(item) for item in items]
    
    return jsonify({
        'text': text,
        'items': items,
        'categories': categories,
        'count': len(items)
    })

@bp.route('/get-alternatives', methods=['GET'])
def get_alternatives():
    """Get alternative products"""
    item = request.args.get('item', '')
    
    if not item:
        return jsonify({'error': 'Item is required'}), 400
    
    alternatives = nlp.find_alternatives(item)
    
    return jsonify({
        'item': item,
        'alternatives': alternatives,
        'count': len(alternatives)
    })

@bp.route('/supported-languages', methods=['GET'])
def get_supported_languages():
    """Get supported languages"""
    languages = {
        'en': 'English',
        'es': 'Spanish',
        'fr': 'French',
        'de': 'German',
        'hi': 'Hindi'
    }
    
    return jsonify({'languages': languages})
