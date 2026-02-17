import re
from typing import Dict, List, Tuple

class NLPProcessor:
    """Natural Language Processing for voice commands"""
    
    # Intent patterns
    INTENTS = {
        'ADD': [
            r'(add|buy|get|need|add me|purchase|put|include)',
            r'(i\s+(?:need|want|should|must)\s+(?:to\s+)?(?:buy|get|purchase))',
        ],
        'REMOVE': [
            r'(remove|delete|cancel|take off|strike|eliminate)',
        ],
        'LIST': [
            r'(show|display|list|what.*have|what.*got|check)',
        ],
        'SEARCH': [
            r'(search|find|look for|where)',
        ],
        'QUANTITY': [
            r'(\d+)\s*(bottle|piece|kg|liter|pack|box|item|items)',
        ],
    }
    
    # Categories mapping
    CATEGORIES = {
        'dairy': ['milk', 'cheese', 'butter', 'yogurt', 'cream', 'eggs'],
        'produce': ['apple', 'banana', 'orange', 'carrot', 'broccoli', 'tomato', 'lettuce'],
        'meat': ['chicken', 'beef', 'pork', 'fish', 'turkey', 'lamb'],
        'snacks': ['chips', 'cookie', 'candy', 'chocolate', 'popcorn', 'nuts'],
        'beverages': ['water', 'juice', 'soda', 'coffee', 'tea', 'milk', 'wine', 'beer'],
        'bakery': ['bread', 'roll', 'bagel', 'donut', 'cake', 'pastry'],
        'frozen': ['ice cream', 'frozen vegetable', 'frozen pizza', 'frozen meal'],
        'pantry': ['rice', 'pasta', 'oil', 'salt', 'sugar', 'flour', 'spice'],
        'personal_care': ['soap', 'shampoo', 'toothpaste', 'deodorant', 'lotion'],
        'household': ['detergent', 'paper towel', 'soap', 'cleaner'],
    }
    
    def __init__(self):
        self.synonyms = {
            'milk': ['dairy milk', 'whole milk', 'skim milk'],
            'bread': ['whole wheat bread', 'white bread', 'brown bread'],
            'water': ['mineral water', 'sparkling water'],
        }
    
    def process_command(self, text: str) -> Dict:
        """Process voice command and extract intent and entities"""
        text = text.lower().strip()
        
        result = {
            'original': text,
            'intent': self._extract_intent(text),
            'items': self._extract_items(text),
            'quantity': self._extract_quantity(text),
            'category': None,
        }
        
        if result['items']:
            result['category'] = self._categorize_item(result['items'][0])
        
        return result
    
    def _extract_intent(self, text: str) -> str:
        """Extract intent from text"""
        for intent, patterns in self.INTENTS.items():
            for pattern in patterns:
                if re.search(pattern, text, re.IGNORECASE):
                    return intent
        return 'UNKNOWN'
    
    def _extract_items(self, text: str) -> List[str]:
        """Extract items from text"""
        # Remove common stopwords and prepositions
        stopwords = {'the', 'a', 'an', 'of', 'to', 'and', 'or', 'from', 'in', 'on', 'at', 'by'}
        
        # Clean the text
        cleaned = re.sub(r'(add|buy|get|need|remove|delete|search|find)', '', text, flags=re.IGNORECASE)
        cleaned = re.sub(r'(\d+\s*(?:bottle|piece|kg|liter|pack|box))', '', cleaned, flags=re.IGNORECASE)
        cleaned = re.sub(r'(to\s+my\s+list|from\s+my\s+list)', '', cleaned, flags=re.IGNORECASE)
        
        # Extract items
        items = [word.strip() for word in cleaned.split(',') if word.strip() and word.strip() not in stopwords]
        return [item for item in items if len(item) > 1]
    
    def _extract_quantity(self, text: str) -> Tuple[int, str]:
        """Extract quantity and unit from text"""
        match = re.search(r'(\d+)\s*([a-z]+)?', text, re.IGNORECASE)
        if match:
            quantity = int(match.group(1))
            unit = match.group(2) or 'piece'
            return quantity, unit
        return 1, 'piece'
    
    def _categorize_item(self, item: str) -> str:
        """Categorize item based on keywords"""
        item_lower = item.lower()
        
        for category, keywords in self.CATEGORIES.items():
            for keyword in keywords:
                if keyword in item_lower:
                    return category
        
        return 'uncategorized'
    
    def find_alternatives(self, item: str) -> List[str]:
        """Find alternative products for a given item"""
        item_lower = item.lower()
        
        # Simple alternative suggestions
        alternatives = {
            'milk': ['almond milk', 'soy milk', 'oat milk', 'coconut milk'],
            'bread': ['whole wheat bread', 'sourdough bread', 'multigrain bread'],
            'apple': ['pear', 'orange', 'banana'],
            'coffee': ['tea', 'espresso'],
        }
        
        for key, alts in alternatives.items():
            if key in item_lower:
                return alts
        
        return []
