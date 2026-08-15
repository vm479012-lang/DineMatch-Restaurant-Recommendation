import pandas as pd
from recommender import recommend_restaurants

def run_test(test_name, **kwargs):
    print(f"\n{'='*50}")
    print(f"Executing {test_name}")
    print(f"User preferences: {kwargs}")
    print(f"{'='*50}")
    
    results = recommend_restaurants(**kwargs)
    
    if results.empty:
        print("Number of results: 0")
        print("No matching restaurants found.")
    else:
        print(f"Number of results: {len(results)}")
        for _, row in results.iterrows():
            name = str(row['Restaurant Name']).encode('ascii', 'ignore').decode('ascii')
            cuisine = str(row['Cuisines']).encode('ascii', 'ignore').decode('ascii')
            print(f"- [{row.get('Recommendation Type', 'Exact Match')}] {name} | Rating: {row['Aggregate rating']} | "
                  f"Cuisine: {cuisine} | Price: {row['Price range']} | "
                  f"Score: {row['Recommendation Score']:.4f} | Match: {row['Match Percentage']}")

if __name__ == "__main__":
    # Test 1: Cuisine = Indian
    run_test("Test 1: Single Cuisine", cuisine="Indian")
    
    # Test 2: Cuisine = Indian, City = Chennai
    run_test("Test 2: Cuisine and City", cuisine="Indian", city="Chennai")
    
    # Test 3: Cuisine = Indian, Price range = 2, Minimum rating = 4.0
    run_test("Test 3: Cuisine, Price, Min Rating", cuisine="Indian", price_range=2, min_rating=4.0)
    
    # Test 4: City = Chennai, Online delivery = Yes
    run_test("Test 4: City and Online Delivery", city="Chennai", online_delivery="Yes")
    
    # Test 5: A combination that produces no results (Fallback expected due to zero result avoidance)
    # Using absurd filters: City = "Atlantis", Price range = 10 (invalid), Min rating = 10.0 (invalid)
    run_test("Test 5: Absurd combination (Fallback expectation)", city="Atlantis", price_range=10, min_rating=10.0)
    
    # Test 6: No preferences
    run_test("Test 6: No preferences")
