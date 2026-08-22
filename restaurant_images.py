import os
import hashlib

# Define a STRICT priority order from most specific to least specific
PRIORITY_ORDER = [
    'seafood',
    'burger',
    'bbq',
    'dessert',
    'cafe',
    'japanese',
    'mexican',
    'middle-eastern',
    'fast-food',
    'italian',
    'indian',
    'chinese',
    'bar',
    'fine-dining',
    'casual',
    'general'
]

# Mapping cuisines to categories
CATEGORY_MAP = {
    'seafood': ['seafood', 'goan', 'coastal'],
    'burger': ['burger', 'american'],
    'bbq': ['bbq', 'barbecue', 'grill', 'steak'],
    'dessert': ['dessert', 'ice cream', 'sweet', 'mithai', 'bakery', 'pastries'],
    'cafe': ['cafe', 'coffee', 'tea', 'beverages', 'drinks'],
    'japanese': ['japanese', 'sushi'],
    'mexican': ['mexican'],
    'middle-eastern': ['arabic', 'lebanese', 'middle eastern'],
    'fast-food': ['fast food', 'pizza', 'street food', 'fries', 'quick bites'],
    'italian': ['italian', 'pasta', 'pizza'],
    'chinese': ['chinese', 'asian', 'thai', 'korean'],
    'indian': ['mughlai', 'north indian', 'south indian', 'indian', 'chettinad', 'bengali', 'rajasthani'],
    'bar': ['bar', 'pub', 'lounge'],
    'fine-dining': ['fine dining'],
    'casual': ['casual dining'],
    'general': ['fallback']
}

def get_restaurant_image(cuisine, restaurant_type, restaurant_name):
    """
    Returns the path to a relevant restaurant image based on cuisine/type.
    """
    hash_obj = hashlib.md5(str(restaurant_name).encode('utf-8'))
    hash_int = int(hash_obj.hexdigest(), 16)
    
    cuisines = str(cuisine).lower()
    rest_type = str(restaurant_type).lower() if restaurant_type else ""
    
    selected_category = 'general'
    
    # Check each category in PRIORITY_ORDER to find the MOST SPECIFIC match
    for cat in PRIORITY_ORDER:
        if cat in CATEGORY_MAP:
            keywords = CATEGORY_MAP[cat]
            if any(kw in cuisines or kw in rest_type for kw in keywords):
                selected_category = cat
                break # We found the highest priority match!
                
    # Find all images in that category
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    cat_dir = os.path.join(BASE_DIR, "static", "images", "restaurants", selected_category)
    images = []
    if os.path.exists(cat_dir):
        images = [f for f in os.listdir(cat_dir) if f.endswith('.jpg')]
        
    if not images:
        return "/static/images/restaurants/general/general-1.jpg" # Safe fallback
        
    # Pick deterministically
    index = hash_int % len(images)
    selected_image = images[index]
    
    # Return web path
    return f"/static/images/restaurants/{selected_category}/{selected_image}"
