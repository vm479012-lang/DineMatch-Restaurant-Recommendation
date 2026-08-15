import pandas as pd
import os

def test_processed_data():
    filepath = "data/processed_restaurants.csv"
    
    # Verify dataset loads
    assert os.path.exists(filepath), f"File {filepath} does not exist"
    df = pd.read_csv(filepath)
    print("Dataset loaded successfully.")
    
    # Required columns exist
    required_cols = [
        'Restaurant Name', 'City', 'Locality', 'Cuisines', 
        'Aggregate rating', 'Votes', 'Price range', 'Average Cost for two', 
        'Has Table booking', 'Has Online delivery', 'content_features'
    ]
    for col in required_cols:
        assert col in df.columns, f"Missing required column: {col}"
    print("All required columns exist.")
    
    # Price range is numeric
    assert pd.api.types.is_numeric_dtype(df['Price range']), "Price range is not numeric"
    print("Price range is numeric.")
    
    # Aggregate rating is numeric
    assert pd.api.types.is_numeric_dtype(df['Aggregate rating']), "Aggregate rating is not numeric"
    print("Aggregate rating is numeric.")
    
    # Cuisines contains no missing values
    assert df['Cuisines'].isnull().sum() == 0, "Cuisines contains missing values"
    print("Cuisines has no missing values.")
    
    # No duplicate rows remain
    assert df.duplicated().sum() == 0, "Duplicate rows found in the dataset"
    print("No duplicate rows found.")
    
    # content_features exists
    assert 'content_features' in df.columns, "content_features column is missing"
    assert df['content_features'].notnull().all(), "content_features contains null values"
    print("content_features exists and is valid.")
    
    print("\nAll tests passed successfully!")

if __name__ == "__main__":
    test_processed_data()
