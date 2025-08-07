import streamlit as st
from prediction_helper import predict

# ---------------------------
# Page Config
# ---------------------------
st.set_page_config(
    page_title="CodeX Beverage: Price Prediction",
    page_icon="🥤",
    layout="wide"
)

# ---------------------------
# Custom CSS for Card & Styling
# ---------------------------
st.markdown("""
    <style>
        .title-card {
            background: linear-gradient(135deg, #ffecd2 0%, #fcb69f 100%);
            padding: 25px;
            border-radius: 15px;
            text-align: center;
            box-shadow: 2px 2px 15px rgba(0,0,0,0.1);
        }
        .title-card h1 {
            color: #1B263B;
            font-size: 38px;
            font-weight: bold;
        }
        .stButton>button {
            background-color: #2E86C1;
            color: white;
            border-radius: 10px;
            height: 50px;
            font-size: 16px;
        }
        .stButton>button:hover {
            background-color: #1A5276;
        }
    </style>
""", unsafe_allow_html=True)

# ---------------------------
# Title Card
# ---------------------------
st.markdown("""
<div class="title-card">
    <h1>🥤 CodeX Beverage Price Prediction</h1>
</div>
""", unsafe_allow_html=True)

# Gap and Header
st.markdown("<div style='margin-top:25px;'></div>", unsafe_allow_html=True)
st.markdown("## 📋 Enter customer details below:")
st.markdown("---")

# ---------------------------
# Inputs Layout
# ---------------------------
with st.container():
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        age = st.number_input('🎂 Age', min_value=18, step=1, max_value=100, value=28,
                              help="Enter the customer's age in years (must be 18 or above).")
    with col2:
        gender = st.selectbox('⚧️ Gender', ['Male', 'Female'],
                              help="Select the customer's gender.")
    with col3:
        zone = st.selectbox('🌍 Zone', ['Urban', 'Rural', 'Metro', 'Semi-Urban'],
                            help="Choose the location type where the customer resides.")
    with col4:
        occupation = st.selectbox('💼 Occupation', ['Working Professional', 'Student', 'Entrepreneur', 'Retired'],
                                  help="Select the customer's primary occupation.")

    col1, col2, col3, col4 = st.columns(4)
    with col1:
        income_levels = st.selectbox('💸 Income Levels', 
                                     ['<10L', '10L - 15L', '16L - 25L', '26L - 35L', '> 35L'],
                                     help="Customer's annual income range (in lakhs INR).")
    with col2:
        consume_frequency = st.selectbox('📆 Consume Frequency (Weekly)',
                                         ['0-2 times', '3-4 times', '5-7 times'],
                                         help="How many times the customer consumes the beverage per week.")
    with col3:
        current_brand = st.selectbox('🏷️ Current Brand', ['Established', 'Newcomer'],
                                     help="The brand type the customer currently prefers.")
    with col4:
        preferable_consumption_size = st.selectbox('📦 Preferable Consumption Size',
                                                   ['Small (250 ml)', 'Medium (500 ml)', 'Large (1 L)'],
                                                   help="The most preferred beverage pack size.")

    col1, col2, col3, col4 = st.columns(4)
    with col1:
        awareness_of_other_brands = st.selectbox('🔍 Awareness of Other Brands',
                                                 ['0 to 1', '2 to 4', 'above 4'],
                                                 help="Number of alternative beverage brands the customer is aware of.")
    with col2:
        reasons_for_choosing_brands = st.selectbox('📊 Reasons for Choosing Brands',
                                                   ['Price', 'Quality', 'Availability', 'Brand Reputation'],
                                                   help="Main reason behind the customer's brand choice.")
    with col3:
        flavor_preference = st.selectbox('🍊 Flavor Preference', ['Traditional', 'Exotic'],
                                         help="Preferred flavor profile of the beverage.")
    with col4:
        purchase_channel = st.selectbox('🛒 Purchase Channel', ['Online', 'Retail Store'],
                                        help="The channel where the customer usually buys the beverage.")

    col1, col2, col3, col4 = st.columns(4)
    with col1:
        packaging_preference = st.selectbox('📦 Packaging Preference',
                                            ['Simple', 'Premium', 'Eco-Friendly'],
                                            help="Type of beverage packaging preferred by the customer.")
    with col2:
        health_concerns = st.selectbox('💚 Health Concerns',
                                       ['Low (Not very concerned)', 'Medium (Moderately health-conscious)', 'High (Very health-conscious)'],
                                       help="Level of concern about health and nutrition.")
    with col3:
        typical_consumption_situations = st.selectbox('🕒 Typical Consumption Situations',
                                                      ['Active (eg. Sports, gym)', 'Social (eg. Parties)', 'Casual (eg. At home)'],
                                                      help="The most common situation where the beverage is consumed.")

# ---------------------------
# Input Dictionary
# ---------------------------
input_dict = {
    'age': age,
    'gender': gender,
    'zone': zone,
    'occupation': occupation,
    'income_levels': income_levels,
    'consume_frequency(weekly)': consume_frequency,
    'current_brand': current_brand,
    'preferable_consumption_size': preferable_consumption_size,
    'awareness_of_other_brands': awareness_of_other_brands,
    'reasons_for_choosing_brands': reasons_for_choosing_brands,
    'flavor_preference': flavor_preference,
    'purchase_channel': purchase_channel,
    'packaging_preference': packaging_preference,
    'health_concerns': health_concerns,
    'typical_consumption_situations': typical_consumption_situations
}

# ---------------------------
# Prediction Button - Left Aligned
# ---------------------------
st.markdown("---")
if st.button("💰 Calculate Price Range", use_container_width=False):
    prediction = predict(input_dict)
    st.markdown(f"""
    <div style="
        background-color: #d4edda;
        color: #155724;
        padding: 15px;
        border-radius: 10px;
        text-align: left;
        font-size: 18px;
        font-weight: bold;
        max-width: 340px;
        margin-top: 15px;
        ">
        💵 Estimated Price Range: ₹ {prediction}
    </div>
    """, unsafe_allow_html=True)
