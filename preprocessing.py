import pandas as pd
import os

def preprocess_data(input_path, output_path):
    print(f"Loading data from {input_path}...")
    df = pd.read_csv(input_path)
    
    initial_rows = len(df)
    missing_before = df.isnull().sum().to_dict()
    
    print("Handling missing values...")
    # 3. Handle missing values
    df['Cuisines'] = df['Cuisines'].fillna('Unknown')
    # Fill remaining missing if any, though our analysis showed none
    
    print("Removing duplicates...")
    # 4. Remove duplicate rows
    df = df.drop_duplicates()
    final_rows = len(df)
    
    missing_after = df.isnull().sum().to_dict()
    
    print("Cleaning text columns...")
    # 5. Clean text columns
    text_cols = ['Restaurant Name', 'City', 'Locality', 'Cuisines', 'Has Table booking', 'Has Online delivery']
    for col in text_cols:
        if col in df.columns:
            df[col] = df[col].astype(str).str.strip()
    
    print("Converting numeric columns...")
    # 6. Convert numeric types
    df['Aggregate rating'] = pd.to_numeric(df['Aggregate rating'], errors='coerce').fillna(0.0)
    df['Votes'] = pd.to_numeric(df['Votes'], errors='coerce').fillna(0)
    df['Price range'] = pd.to_numeric(df['Price range'], errors='coerce').fillna(1)
    
    print("Creating content_features...")
    # 9. Create content_features
    def create_features(row):
        features = []
        if pd.notna(row.get('Cuisines')):
            features.append(str(row['Cuisines']).replace(',', ' '))
        if pd.notna(row.get('City')):
            features.append(str(row['City']).replace(' ', ''))
        if pd.notna(row.get('Locality')):
            features.append(str(row['Locality']).replace(' ', ''))
        if pd.notna(row.get('Price range')):
            features.append(f"Price{row['Price range']}")
        if pd.notna(row.get('Has Table booking')):
            features.append(f"TableBooking_{row['Has Table booking']}")
        if pd.notna(row.get('Has Online delivery')):
            features.append(f"Delivery_{row['Has Online delivery']}")
        
        # We don't have 'Restaurant Type' in the dataset, omitting it.
        return " ".join(features)
        
    df['content_features'] = df.apply(create_features, axis=1)
    
    # 11. Keep columns for display + content_features + Restaurant ID (useful as unique key)
    keep_cols = [
        'Restaurant ID',
        'Restaurant Name',
        'City',
        'Locality',
        'Cuisines',
        'Aggregate rating',
        'Votes',
        'Price range',
        'Average Cost for two',
        'Has Table booking',
        'Has Online delivery',
        'content_features'
    ]
    
    # Select available columns
    final_cols = [c for c in keep_cols if c in df.columns]
    df = df[final_cols]
    
    print(f"Saving processed dataset to {output_path}...")
    # 12. Save processed dataset
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    df.to_csv(output_path, index=False)
    print("Preprocessing complete!")
    
    return initial_rows, final_rows, missing_before, missing_after

if __name__ == "__main__":
    # If the user has dataset inside 'data/Dataset.csv' use it, otherwise root 'Dataset.csv'
    input_file = "data/Dataset.csv" if os.path.exists("data/Dataset.csv") else "Dataset.csv"
    output_file = "data/processed_restaurants.csv"
    
    preprocess_data(input_file, output_file)
