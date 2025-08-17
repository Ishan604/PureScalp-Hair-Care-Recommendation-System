import pandas as pd
import os

def load_recommendations_data():
    """Load the hair recommendations CSV file"""
    try:
        csv_path = 'datasets/hair_recommendations.csv'
        df = pd.read_csv(csv_path)
        print(f"Recommendations data loaded successfully. Shape: {df.shape}")
        print(f"Columns: {df.columns.tolist()}")
        return df
    except FileNotFoundError:
        print(f"Error: hair_recommendations.csv not found in datasets folder")
        return None
    except Exception as e:
        print(f"Error loading recommendations data: {e}")
        return None

def get_recommendation_by_score(patient_score):
    """
    Get recommendation from CSV based on patient's score
    Returns the exact recommendation from the CSV file
    """
    try:
        # Load the CSV data
        df = load_recommendations_data()
        if df is None:
            return get_fallback_recommendation(patient_score)
        
        # Clean column names (remove any extra spaces)
        df.columns = df.columns.str.strip()
        
        # Look for exact score match first
        exact_match = df[df['Score'] == patient_score]
        
        if not exact_match.empty:
            recommendation = exact_match.iloc[0]['Recommendation']
            return {
                'recommendation': recommendation,
                'score': patient_score,
                'match_type': 'exact',
                'source': 'CSV lookup'
            }
        
        # If no exact match, find the closest score
        df['score_diff'] = abs(df['Score'] - patient_score)
        closest_match = df.loc[df['score_diff'].idxmin()]
        
        recommendation = closest_match['Recommendation']
        closest_score = closest_match['Score']
        
        return {
            'recommendation': recommendation,
            'score': patient_score,
            'matched_score': closest_score,
            'match_type': 'closest',
            'source': 'CSV lookup'
        }
        
    except Exception as e:
        print(f"Error getting recommendation: {e}")
        return get_fallback_recommendation(patient_score)

def get_fallback_recommendation(score):
    """Fallback recommendation when CSV is not available"""
    if score >= 50:
        recommendation = "Intensive hair treatment with keratin-based products and professional consultation recommended"
    elif score >= 25:
        recommendation = "Moderate hair care routine with moisturizing treatments and regular scalp massage"
    else:
        recommendation = "Basic hair maintenance with gentle products and regular care routine"
    
    return {
        'recommendation': recommendation,
        'score': score,
        'match_type': 'fallback',
        'source': 'Built-in logic'
    }

def get_all_recommendations():
    """Get all recommendations from CSV for debugging/testing"""
    df = load_recommendations_data()
    if df is not None:
        return df.to_dict('records')
    return []

def test_recommendation_lookup():
    """Test function to verify the lookup system works"""
    print("Testing recommendation lookup system...")
    
    # Test with sample scores
    test_scores = [15, 30, 45, 60, 75]
    
    for score in test_scores:
        result = get_recommendation_by_score(score)
        print(f"\nScore: {score}")
        print(f"Recommendation: {result['recommendation']}")
        print(f"Match type: {result['match_type']}")
        print(f"Source: {result['source']}")
        if 'matched_score' in result:
            print(f"Matched CSV score: {result['matched_score']}")

if __name__ == "__main__":
    test_recommendation_lookup()