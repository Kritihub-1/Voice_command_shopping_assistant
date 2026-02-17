from dataclasses import dataclass, field, asdict
from typing import List
from datetime import datetime

@dataclass
class ShoppingItem:
    """Represents a single shopping item"""
    id: str
    name: str
    quantity: int = 1
    unit: str = "piece"
    category: str = "uncategorized"
    price_estimate: float = 0.0
    added_at: str = field(default_factory=lambda: datetime.now().isoformat())
    
    def to_dict(self):
        return asdict(self)

@dataclass
class ShoppingList:
    """Represents a shopping list"""
    id: str
    user_id: str
    items: List[ShoppingItem] = field(default_factory=list)
    created_at: str = field(default_factory=lambda: datetime.now().isoformat())
    
    def add_item(self, item: ShoppingItem):
        """Add item to shopping list"""
        # Check if item already exists
        existing = next((i for i in self.items if i.name.lower() == item.name.lower()), None)
        if existing:
            existing.quantity += item.quantity
        else:
            self.items.append(item)
    
    def remove_item(self, item_id: str):
        """Remove item from shopping list"""
        self.items = [i for i in self.items if i.id != item_id]
    
    def get_by_category(self, category: str) -> List[ShoppingItem]:
        """Get items by category"""
        return [i for i in self.items if i.category.lower() == category.lower()]
    
    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'items': [item.to_dict() for item in self.items],
            'created_at': self.created_at
        }
