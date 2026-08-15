import pandas as pd
from recommender import recommend_restaurants

def display_recommendations(scenario_name, recommendations):
    print(f"\n{'-'*60}")
    print(f"SCENARIO: {scenario_name}")
    print(f"{'-'*60}")
    
    if recommendations.empty:
        print("Sorry, we couldn't find any recommendations matching your exact preferences.")
        return
        
    for idx, row in recommendations.iterrows():
        name = str(row['Restaurant Name']).encode('ascii', 'ignore').decode('ascii')
        loc = str(row['Locality']).encode('ascii', 'ignore').decode('ascii')
        city = str(row['City']).encode('ascii', 'ignore').decode('ascii')
        cuisines = str(row['Cuisines']).encode('ascii', 'ignore').decode('ascii')
        
        print(f"\n[{idx+1}] {name}")
        print(f"    Location: {loc}, {city}")
        print(f"    Cuisines: {cuisines}")
        print(f"    Rating: {row['Aggregate rating']} ({row['Votes']} votes)")
        print(f"    Price Range: {row['Price range']}")
        print(f"    Table Booking: {row['Has Table booking']} | Delivery: {row['Has Online delivery']}")
        print(f"    Match Percentage: {row['Match Percentage']} | Type: {row.get('Recommendation Type', 'Exact Match')}")

if __name__ == "__main__":
    # Scenario 1: User wants high-end Italian food in New Delhi with table booking
    results_1 = recommend_restaurants(
        cuisine="Italian", 
        city="New Delhi", 
        price_range=4, 
        table_booking="Yes",
        top_n=3
    )
    # Re-indexing for clean display indices
    results_1 = results_1.reset_index(drop=True)
    display_recommendations("High-end Italian in New Delhi (with Table Booking)", results_1)
    
    # Scenario 2: User wants affordable casual dining (no specific cuisine) in Gurgaon with online delivery
    results_2 = recommend_restaurants(
        city="Gurgaon",
        price_range=1,
        online_delivery="Yes",
        min_rating=3.5,
        top_n=3
    )
    results_2 = results_2.reset_index(drop=True)
    display_recommendations("Affordable good food in Gurgaon (with Delivery)", results_2)
    
    # Scenario 3: User wants Mexican or American food, high rating
    results_3 = recommend_restaurants(
        cuisine="Mexican American",
        min_rating=4.5,
        top_n=3
    )
    results_3 = results_3.reset_index(drop=True)
    display_recommendations("Top-rated Mexican/American food", results_3)
