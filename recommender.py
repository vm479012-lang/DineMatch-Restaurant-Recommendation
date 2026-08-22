import pandas as pd
import numpy as np
import os
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# 1. Load data
try:
    df = pd.read_csv(os.path.join(BASE_DIR, 'data', 'processed_restaurants.csv'))
    
    # 3. Create a TF-IDF vectorizer
    # What TF-IDF does: 
    # Term Frequency-Inverse Document Frequency (TF-IDF) converts text into mathematical vectors.
    # It assigns higher weights to rare, distinguishing terms (like a specific cuisine) 
    # and lower weights to common terms, allowing for meaningful text comparison.
    tfidf = TfidfVectorizer(stop_words='english')
    
    # 4. Transform the restaurant content_features into TF-IDF vectors
    tfidf_matrix = tfidf.fit_transform(df['content_features'].fillna(''))
except FileNotFoundError:
    df = None
    tfidf = None
    tfidf_matrix = None

# 6. Create reusable recommendation function
def recommend_restaurants(cuisine=None, city=None, price_range=None, min_rating=None, 
                          restaurant_type=None, table_booking=None, online_delivery=None, top_n=5):
    """
    Recommends restaurants based on content similarity and hard filters.
    """
    if df is None or df.empty:
        return pd.DataFrame()

    # 10. Create a user preference profile from the selected preferences
    # How the user profile is created:
    # We combine the textual representations of the user's selected preferences into a single string.
    # This string is then vectorized into the same feature space as the restaurant content features.
    user_features = []
    if cuisine:
        user_features.append(str(cuisine).replace(',', ' '))
    if city:
        user_features.append(str(city).replace(' ', ''))
    if price_range:
        user_features.append(f"Price{price_range}")
    if table_booking:
        user_features.append(f"TableBooking_{table_booking}")
    if online_delivery:
        user_features.append(f"Delivery_{online_delivery}")
    if restaurant_type: # Handling even though not in original data
        user_features.append(str(restaurant_type).replace(' ', ''))
        
    user_profile_str = " ".join(user_features)
    
    # Helper to parse numeric filters safely
    safe_price = None
    if price_range:
        try: safe_price = int(price_range)
        except ValueError: pass
        
    safe_rating = None
    if min_rating:
        try: safe_rating = float(min_rating)
        except ValueError: pass

    def apply_filters(data, use_city, use_price, use_rating, use_booking, use_deliv):
        t = data.copy()
        if use_city and city:
            t = t[t['City'].str.contains(city, case=False, na=False)]
        if use_price and safe_price is not None:
            t = t[t['Price range'] == safe_price]
        if use_rating and safe_rating is not None:
            t = t[t['Aggregate rating'] >= safe_rating]
        if use_booking and table_booking:
            t = t[t['Has Table booking'].str.lower() == str(table_booking).lower()]
        if use_deliv and online_delivery:
            t = t[t['Has Online delivery'].str.lower() == str(online_delivery).lower()]
        return t

    filtered_df = df.copy()
    recommendation_type = "Exact Match"
    
    # 1. Exact Match
    temp_df = apply_filters(filtered_df, True, True, True, True, True)
    
    # 2. Relax booking and delivery
    if len(temp_df) == 0:
        recommendation_type = "Alternative"
        temp_df = apply_filters(filtered_df, True, True, True, False, False)
        
    # 3. Relax price range
    if len(temp_df) == 0:
        temp_df = apply_filters(filtered_df, True, False, True, False, False)
        
    # 4. Relax city
    if len(temp_df) == 0:
        temp_df = apply_filters(filtered_df, False, False, True, False, False)
        
    # 5. Relax everything (fallback to entire dataset)
    if len(temp_df) == 0:
        temp_df = filtered_df.copy()

    filtered_df = temp_df

    # 16. Handle Empty user preferences
    if not user_profile_str.strip():
        if filtered_df.empty:
            return pd.DataFrame()
        # Ranking strategy for empty profile: Highest rating and most votes
        results = filtered_df.sort_values(by=['Aggregate rating', 'Votes'], ascending=[False, False]).head(top_n).copy()
        results['Recommendation Score'] = 0.0
        results['Match Percentage'] = "0.0%"
        results['Recommendation Type'] = recommendation_type
        return format_results(results)

    # 5. Calculate cosine similarity
    user_vector = tfidf.transform([user_profile_str])
    filtered_indices = filtered_df.index
    filtered_matrix = tfidf_matrix[filtered_indices]
    
    sim_scores = cosine_similarity(user_vector, filtered_matrix).flatten()
    
    filtered_df = filtered_df.copy()
    filtered_df['Recommendation Score'] = sim_scores
    filtered_df['Match Percentage'] = pd.Series(sim_scores * 100, index=filtered_df.index).round(1).astype(str) + "%"
    filtered_df['Recommendation Type'] = recommendation_type
    
    if (sim_scores > 0).any():
        filtered_df = filtered_df[filtered_df['Recommendation Score'] > 0]
        
    results = filtered_df.sort_values(
        by=['Recommendation Score', 'Aggregate rating'], 
        ascending=[False, False]
    ).head(top_n)
    
    return format_results(results)

def format_results(df):
    """Ensure output format requirements are met."""
    if df.empty:
        return df
        
    # 14. Required returned results
    cols = [
        'Restaurant Name', 'City', 'Locality', 'Cuisines', 'Aggregate rating', 
        'Votes', 'Price range', 'Average Cost for two', 'Has Table booking', 
        'Has Online delivery', 'Recommendation Score', 'Match Percentage', 'Recommendation Type'
    ]
    available_cols = [c for c in cols if c in df.columns]
    
    # 17. Do not allow duplicate restaurants in the result.
    df = df.drop_duplicates(subset=['Restaurant Name', 'City', 'Locality'])
    
    return df[available_cols]
