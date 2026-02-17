from typing import List, Dict
from datetime import datetime, timedelta
import random

class RecommendationEngine:
    """Smart recommendation system for shopping items"""
    
    # Seasonal items by month
    SEASONAL_ITEMS = {
        'summer': ['watermelon', 'strawberries', 'ice cream', 'popsicles', 'sunscreen'],
        'winter': ['hot chocolate', 'soup', 'bread', 'wine', 'cheese'],
        'spring': ['fresh vegetables', 'berries', 'salad', 'spring onions'],
        'fall': ['pumpkin', 'apples', 'squash', 'cranberries', 'turkey'],
    }
    
    # Frequently bought together
    FREQUENTLY_TOGETHER = {
        'milk': ['bread', 'eggs', 'butter'],
        'eggs': ['milk', 'butter', 'bread'],
        'bread': ['butter', 'jam', 'milk'],
        'pasta': ['sauce', 'cheese', 'olive oil'],
        'chicken': ['garlic', 'onion', 'salt'],
    }
    
    # Low stock alerts
    RESTOCK_ITEMS = {
        'milk': 7,  # every 7 days
        'bread': 3,
        'eggs': 14,
        'water': 7,
    }
    
    def __init__(self):
        self.user_history = {}  # Store shopping history per user
    
    def get_recommendations(self, user_id: str, current_items: List[str]) -> List[Dict]:
        """Get personalized recommendations"""
        recommendations = []
        
        # 1. Frequently bought together
        for item in current_items:
            if item in self.FREQUENTLY_TOGETHER:
                for rec_item in self.FREQUENTLY_TOGETHER[item]:
                    if rec_item not in current_items:
                        recommendations.append({
                            'item': rec_item,
                            'reason': f'Often bought with {item}',
                            'confidence': 0.8,
                            'type': 'frequently_together'
                        })
        
        # 2. Seasonal items
        seasonal_recs = self._get_seasonal_recommendations()
        recommendations.extend(seasonal_recs)
        
        # 3. Low stock alerts
        low_stock_recs = self._get_low_stock_recommendations(user_id)
        recommendations.extend(low_stock_recs)
        
        # Remove duplicates
        seen = set()
        unique_recs = []
        for rec in recommendations:
            if rec['item'] not in seen:
                unique_recs.append(rec)
                seen.add(rec['item'])
        
        return unique_recs[:5]  # Return top 5 recommendations
    
    def _get_seasonal_recommendations(self) -> List[Dict]:
        """Get recommendations based on current season"""
        month = datetime.now().month
        
        if month in [3, 4, 5]:
            season = 'spring'
        elif month in [6, 7, 8]:
            season = 'summer'
        elif month in [9, 10, 11]:
            season = 'fall'
        else:
            season = 'winter'
        
        items = self.SEASONAL_ITEMS.get(season, [])
        return [{
            'item': item,
            'reason': f'In season this {season}',
            'confidence': 0.6,
            'type': 'seasonal'
        } for item in items[:3]]
    
    def _get_low_stock_recommendations(self, user_id: str) -> List[Dict]:
        """Get recommendations for items that need restocking"""
        recommendations = []
        
        if user_id not in self.user_history:
            return recommendations
        
        history = self.user_history[user_id]
        
        for item, last_purchased in history.items():
            if item in self.RESTOCK_ITEMS:
                days_since = (datetime.now() - last_purchased).days
                restock_interval = self.RESTOCK_ITEMS[item]
                
                if days_since > restock_interval:
                    recommendations.append({
                        'item': item,
                        'reason': f'Time to restock (last bought {days_since} days ago)',
                        'confidence': 0.9,
                        'type': 'restock'
                    })
        
        return recommendations
    
    def record_purchase(self, user_id: str, items: List[str]):
        """Record purchase history for recommendations"""
        if user_id not in self.user_history:
            self.user_history[user_id] = {}
        
        for item in items:
            self.user_history[user_id][item] = datetime.now()
    
    def get_substitute_products(self, item: str) -> List[Dict]:
        """Get substitute products if item is unavailable"""
        substitutes = {
            'milk': ['almond milk', 'soy milk', 'oat milk', 'coconut milk'],
            'eggs': ['tofu', 'applesauce', 'mashed banana'],
            'butter': ['coconut oil', 'olive oil', 'margarine'],
            'wheat bread': ['rye bread', 'sourdough', 'multigrain'],
            'chicken': ['turkey', 'tofu', 'fish'],
            'beef': ['ground turkey', 'lean pork', 'veggie burger'],
        }
        
        item_lower = item.lower()
        for key, subs in substitutes.items():
            if key in item_lower:
                return [{'item': sub, 'reason': f'Substitute for {item}'} for sub in subs]
        
        return []
    
    def get_price_range_by_item(self, item: str) -> Dict:
        """Get average price range for an item"""
        # Mock data - in production, fetch from real pricing API
        price_data = {
            'milk': {'min': 2.50, 'max': 4.00, 'avg': 3.20},
            'bread': {'min': 1.50, 'max': 3.50, 'avg': 2.50},
            'eggs': {'min': 2.50, 'max': 4.50, 'avg': 3.50},
            'apple': {'min': 0.50, 'max': 1.50, 'avg': 1.00},
            'chicken': {'min': 4.00, 'max': 8.00, 'avg': 6.00},
        }
        
        return price_data.get(item.lower(), {
            'min': 1.00, 'max': 10.00, 'avg': 5.00
        })
