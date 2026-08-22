# 🍽️ DineMatch — AI-Powered Restaurant Recommendation System

# live at : https://dine-match-restaurant-recommendatio.vercel.app
## Overview
DineMatch is a content-based restaurant recommendation system developed using the Cognifyz Technologies restaurant dataset. It helps users discover their perfect dining spot by analyzing restaurant attributes and matching them intelligently against user preferences.

## Features
- Personalized restaurant recommendations
- Content-based filtering
- TF-IDF vectorization
- Cosine similarity
- Cuisine-based recommendations
- City-based filtering
- Price range filtering
- Minimum rating filtering
- Restaurant type filtering
- Table booking preference
- Online delivery preference
- Progressive fallback recommendations
- Exact Match / Alternative Match classification
- Match percentage
- Responsive premium UI
- Restaurant image categorization
- Mobile-friendly interface

## Machine Learning Methodology

The engine operates on a robust content-based filtering pipeline:

**Dataset** ↓ **Preprocessing** ↓ **Feature Engineering** ↓ **Content Features** ↓ **TF-IDF** ↓ **User Preference Vector** ↓ **Cosine Similarity** ↓ **Filtering** ↓ **Ranking** ↓ **Recommendations**

- **TF-IDF (Term Frequency-Inverse Document Frequency):** In simple terms, this technique looks at the text descriptions (like cuisines and restaurant types) and assigns a mathematical weight to words. Rare, specific cuisines (like "Goan") get higher importance than common words, allowing the engine to understand exactly what makes a restaurant unique.
- **Cosine Similarity:** This mathematical formula measures the angle between two vectors (in this case, what the user wants vs. what the restaurant offers). A smaller angle means they are highly similar, resulting in a higher Match Percentage.
- **Progressive Fallback:** If you request an impossible combination (e.g. 5-star Seafood in a city with no seafood), the system does not silently fail. It progressively relaxes optional filters (like delivery, then price, then city) while maintaining your core cuisine preference, eventually serving you the closest "Alternative Match".

## Dataset
- **9,551 restaurants**
- **21 columns**
- **141 cities**

This dataset was provided as part of the Cognifyz Technologies internship task.

## Technology Stack
- **Python**
- **Pandas & NumPy** (Data processing)
- **Scikit-learn** (TF-IDF & Cosine Similarity)
- **Flask** (Backend Web Framework)
- **HTML, CSS, JavaScript** (Frontend UI)

## Project Structure
```text
DineMatch/
├── data/
│   ├── Dataset.csv
│   └── processed_restaurants.csv
├── static/
│   ├── css/
│   │   └── style.css
│   ├── images/
│   │   └── restaurants/
│   └── js/
│       └── script.js
├── templates/
│   ├── index.html
│   ├── results.html
│   └── error.html
├── app.py
├── recommender.py
├── preprocessing.py
├── restaurant_images.py
├── requirements.txt
├── render.yaml
└── README.md
```

## Installation

```bash
git clone <repository-url>
cd restaurant-recommendation-system
python -m venv venv
```

**Windows:**
```bash
venv\Scripts\activate
```

**Install Dependencies:**
```bash
pip install -r requirements.txt
```

**Run locally:**
```bash
python app.py
```
Then navigate to: `http://127.0.0.1:5000`

## Production

For production environments, the app uses Gunicorn:
```bash
gunicorn app:app
```

## Usage
1. Open the application homepage.
2. Select your desired **Cuisine**, **City**, **Price Range**, **Minimum Rating**, **Restaurant Type**, and delivery/booking preferences.
3. Click "Find My Restaurant".
4. View your exact or alternative recommendation cards, beautifully categorized with dynamic imagery.

## Screenshots
<!-- Add your screenshots here -->
- `screenshots/home.png`
- `screenshots/recommendations.png`
- `screenshots/mobile.png`

## Project Highlights
- **Machine learning recommendation engine**
- **Responsive UI**
- **Progressive fallback**
- **Dynamic dataset-driven dropdowns**
- **Deterministic restaurant images**
- **Professional UX**

## Future Improvements
- User accounts
- Collaborative filtering
- Location/GPS integration
- Restaurant reviews
- Personalized history
- Hybrid recommendation system
- Real-time restaurant availability

## Author
**jonnalagadda venkata mahesh**

## Internship
**Cognifyz Technologies Internship**
