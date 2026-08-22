import os
import sys
import pandas as pd
from flask import Flask, render_template, request, jsonify

# Startup validation
print("Performing startup validation...")

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
dataset_path = os.path.join(BASE_DIR, 'data', 'processed_restaurants.csv')
if not os.path.exists(dataset_path):
    print(f"CRITICAL ERROR: Dataset not found at {dataset_path}")
    sys.exit(1)

try:
    df = pd.read_csv(dataset_path)
    required_cols = ['Restaurant Name', 'City', 'Locality', 'Cuisines', 'Aggregate rating']
    for col in required_cols:
        if col not in df.columns:
            print(f"CRITICAL ERROR: Required column '{col}' missing from dataset.")
            sys.exit(1)
except Exception as e:
    print(f"CRITICAL ERROR loading dataset: {e}")
    sys.exit(1)

try:
    from recommender import recommend_restaurants
except ImportError as e:
    print(f"CRITICAL ERROR: Could not import recommender.py. {e}")
    sys.exit(1)

# Extract unique cuisines and cities for the form
# Since Cuisines can be comma separated, we need to split them
unique_cities = sorted(df['City'].dropna().unique().tolist())

cuisine_set = set()
for c_list in df['Cuisines'].dropna():
    for c in str(c_list).split(','):
        cuisine_set.add(c.strip())
unique_cuisines = sorted(list(cuisine_set))

print("Startup validation successful!")

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html', cities=unique_cities, cuisines=unique_cuisines)

@app.route('/health')
def health():
    return jsonify({"status": "healthy"})

@app.route('/recommend', methods=['POST'])
def recommend():
    try:
        # Extract form data and handle 'Any' selections
        def get_val(key):
            val = request.form.get(key, '').strip()
            return val if val and val.lower() != 'any' else None

        cuisine = get_val('cuisine')
        city = get_val('city')
        price_range = get_val('price_range')
        min_rating = get_val('min_rating')
        restaurant_type = get_val('restaurant_type')
        table_booking = get_val('table_booking')
        online_delivery = get_val('online_delivery')
        
        # Parse top_n safely
        try:
            top_n = int(request.form.get('top_n', 5))
        except ValueError:
            top_n = 5

        # Call recommendation engine
        recommendations = recommend_restaurants(
            cuisine=cuisine,
            city=city,
            price_range=price_range,
            min_rating=min_rating,
            restaurant_type=restaurant_type,
            table_booking=table_booking,
            online_delivery=online_delivery,
            top_n=top_n
        )

        preferences = {
            "Cuisine": cuisine or "Any",
            "City": city or "Any",
            "Price Range": price_range or "Any",
            "Minimum Rating": min_rating or "Any",
            "Restaurant Type": restaurant_type or "Any",
            "Table Booking": table_booking or "Any",
            "Online Delivery": online_delivery or "Any",
            "Requested Results": top_n
        }

        from restaurant_images import get_restaurant_image
        
        # Convert dataframe to list of dicts for template
        results_list = recommendations.to_dict('records') if not recommendations.empty else []
        
        for r in results_list:
            r['image'] = get_restaurant_image(r.get('Cuisines', ''), '', r.get('Restaurant Name', ''))

        return render_template('results.html', results=results_list, preferences=preferences)

    except Exception as e:
        print(f"Error processing recommendation: {e}")
        return render_template('error.html', error_message="An unexpected error occurred while processing your request. Please try again.")

if __name__ == '__main__':
    import os
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)
