"""
Test validation of insights.json against Pydantic model
"""

import json
import sys
sys.path.append('../api')

from pydantic import BaseModel, ValidationError
from typing import Optional

class Insight(BaseModel):
    title: str
    source: str
    summary: str
    type: Optional[str] = "insight"
    product: Optional[str] = None
    feature: Optional[str] = None
    channel: Optional[str] = None
    social_media: Optional[str] = None
    sentiment: Optional[str] = "neutral"
    urgency_score: Optional[int] = 50
    date: Optional[str] = None
    category: Optional[str] = None
    rating: Optional[int] = None
    user: Optional[str] = None
    
    class Config:
        extra = "allow"

# Load data
data_path = '../data/insights.json'
with open(data_path, 'r') as f:
    data = json.load(f)

items = data.get('items', [])
print(f"Total items in file: {len(items)}")

# Try to validate each item
valid_count = 0
invalid_count = 0
errors = []

for idx, item in enumerate(items):
    try:
        if isinstance(item, dict) and all(key in item for key in ['title', 'source', 'summary']):
            Insight(**item)
            valid_count += 1
        else:
            invalid_count += 1
            missing_keys = [key for key in ['title', 'source', 'summary'] if key not in item]
            errors.append(f"Item {idx}: Missing keys: {missing_keys}")
    except ValidationError as e:
        invalid_count += 1
        errors.append(f"Item {idx}: {str(e)[:200]}")
    except Exception as e:
        invalid_count += 1
        errors.append(f"Item {idx}: {type(e).__name__}: {str(e)[:100]}")

print(f"\n✅ Valid items: {valid_count}")
print(f"❌ Invalid items: {invalid_count}")

if errors:
    print(f"\n📋 Sample errors (first 10):")
    for error in errors[:10]:
        print(f"  {error}")

