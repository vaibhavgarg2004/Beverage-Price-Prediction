import joblib
import pandas as pd

MODEL_PATH = 'artifacts/model_data.joblib'

model = joblib.load(MODEL_PATH)

def preprocess_input(input_dict):
    # Expected one-hot encoded + numerical columns
    expected_columns = [
        'income_levels', 'consume_frequency(weekly)', 'preferable_consumption_size',
        'awareness_of_other_brands', 'health_concerns', 'age_group', 'cf_ab_score', 'zas_score', 'bsi',
        'gender_M', 'zone_Rural', 'zone_Semi-Urban', 'zone_Urban',
        'occupation_Retired', 'occupation_Student', 'occupation_Working Professional',
        'current_brand_Newcomer', 'reasons_for_choosing_brands_Brand Reputation',
        'reasons_for_choosing_brands_Price', 'reasons_for_choosing_brands_Quality',
        'flavor_preference_Traditional', 'purchase_channel_Retail Store',
        'packaging_preference_Premium', 'packaging_preference_Simple',
        'typical_consumption_situations_Casual (eg. At home)',
        'typical_consumption_situations_Social (eg. Parties)'
    ]
    
    # Initialize DataFrame with zeros
    df = pd.DataFrame(0, columns=expected_columns, index=[0])
    
    # -------------------
    # Step 1: Age group
    # -------------------
    age = input_dict['age']
    if 18 <= age <= 25:
        df['age_group'] = 1
    elif 26 <= age <= 35:
        df['age_group'] = 2
    elif 36 <= age <= 45:
        df['age_group'] = 3
    elif 46 <= age <= 55:
        df['age_group'] = 4
    elif 56 <= age <= 70:
        df['age_group'] = 5
    else:
        df['age_group'] = 6  # 70+

    # Step 2: cf_ab_score (1-based mapping)
    freq_map = {'0-2 times': 1, '3-4 times': 2, '5-7 times': 3}
    awareness_map = {'0 to 1': 1, '2 to 4': 2, 'above 4': 3}
    fs = freq_map[input_dict['consume_frequency(weekly)']]
    as_ = awareness_map[input_dict['awareness_of_other_brands']]
    df['cf_ab_score'] = round((fs / (as_ + fs)), 2) if (as_ + fs) != 0 else 0

    # Step 3: zas_score
    zone_map = {"Urban": 3, "Metro": 4, "Rural": 1, "Semi-Urban": 2}
    income_map = {
        "<10L": 1, "10L - 15L": 2, "16L - 25L": 3,
        "26L - 35L": 4, "> 35L": 5, "Not Reported": 0
    }
    df['zas_score'] = zone_map[input_dict['zone']] * income_map[input_dict['income_levels']]

    # Step 4: bsi
    if (input_dict['current_brand'] != "Established" and 
        input_dict['reasons_for_choosing_brands'] in ["Price", "Quality"]):
        df['bsi'] = 1
    else:
        df['bsi'] = 0

    # Direct numerical/ordinal features
    df['income_levels'] = income_map[input_dict['income_levels']]
    df['consume_frequency(weekly)'] = fs
    size_map = {'Small (250 ml)': 1, 'Medium (500 ml)': 2, 'Large (1 L)': 3}
    df['preferable_consumption_size'] = size_map[input_dict['preferable_consumption_size']]
    df['awareness_of_other_brands'] = as_
    health_map = {
        "Low (Not very concerned)": 1,
        "Medium (Moderately health-conscious)": 2,
        "High (Very health-conscious)": 3
    }
    df['health_concerns'] = health_map[input_dict['health_concerns']]

    # One-hot encodings
    if input_dict['gender'] == "Male":
        df['gender_M'] = 1
    if input_dict['zone'] == "Rural":
        df['zone_Rural'] = 1
    elif input_dict['zone'] == "Semi-Urban":
        df['zone_Semi-Urban'] = 1
    elif input_dict['zone'] == "Urban":
        df['zone_Urban'] = 1

    if input_dict['occupation'] == "Retired":
        df['occupation_Retired'] = 1
    elif input_dict['occupation'] == "Student":
        df['occupation_Student'] = 1
    elif input_dict['occupation'] == "Working Professional":
        df['occupation_Working Professional'] = 1
    # Entrepreneur left without encoding if not in training

    if input_dict['current_brand'] == "Newcomer":
        df['current_brand_Newcomer'] = 1

    if input_dict['reasons_for_choosing_brands'] == "Brand Reputation":
        df['reasons_for_choosing_brands_Brand Reputation'] = 1
    elif input_dict['reasons_for_choosing_brands'] == "Price":
        df['reasons_for_choosing_brands_Price'] = 1
    elif input_dict['reasons_for_choosing_brands'] == "Quality":
        df['reasons_for_choosing_brands_Quality'] = 1

    if input_dict['flavor_preference'] == "Traditional":
        df['flavor_preference_Traditional'] = 1

    if input_dict['purchase_channel'] == "Retail Store":
        df['purchase_channel_Retail Store'] = 1

    if input_dict['packaging_preference'] == "Premium":
        df['packaging_preference_Premium'] = 1
    elif input_dict['packaging_preference'] == "Simple":
        df['packaging_preference_Simple'] = 1

    if input_dict['typical_consumption_situations'] == "Casual (eg. At home)":
        df['typical_consumption_situations_Casual (eg. At home)'] = 1
    elif input_dict['typical_consumption_situations'] == "Social (eg. Parties)":
        df['typical_consumption_situations_Social (eg. Parties)'] = 1

    return df


def predict(input_dict):
    label_map = {
    0: '50-100',
    1: '100-150',
    2: '150-200',
    3: '200-250'
    }
    input_df = preprocess_input(input_dict)
    prediction = model.predict(input_df)
    return label_map[int(prediction[0])]