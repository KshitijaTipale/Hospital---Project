import streamlit as st
import pandas as pd
import numpy as np
import time

# --- Page Configuration ---
st.set_page_config(
    page_title="Sugarcane Yield Prediction",
    page_icon="🌾",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- Custom Styling ---
st.markdown("""
    <style>
    .main {
        background-color: #f8f9fa;
    }
    .stButton>button {
        width: 100%;
        background-color: #4CAF50;
        color: white;
        font-weight: bold;
        border-radius: 8px;
        padding: 0.5rem 1rem;
        border: none;
    }
    .stButton>button:hover {
        background-color: #45a049;
    }
    .metric-card {
        background-color: white;
        padding: 20px;
        border-radius: 10px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        text-align: center;
    }
    h1 {
        color: #2E7D32;
        font-family: 'Helvetica Neue', sans-serif;
    }
    .sidebar-text {
        font-size: 14px;
        color: #555;
    }
    </style>
    """, unsafe_allow_html=True)

# --- Sidebar ---
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/2674/2674486.png", width=100) # Optional: Add a local image if available
    st.title("Project Overview")
    st.markdown("""
    **AI Driven Sugarcane Yield Prediction**
    
    This system predicts sugarcane yield based on environmental and satellite parameters using Machine Learning.
    """)
    
    st.subheader("🛠 Technologies Used")
    st.markdown("""
    - **Python** (Logic)
    - **Streamlit** (UI)
    - **Machine Learning** (Prediction)
    - **Satellite Data** (NDVI)
    - **Weather Data** (Rainfall, Temp)
    """)
    
    st.divider()
    st.caption("Designed for Final Year Engineering Project")

# --- Main Content ---
st.title("🌾 AI Driven Sugarcane Yield Prediction")
st.markdown("### Predict sugarcane yield for A.Nagar district taluks with precision.")

st.divider()

col1, col2 = st.columns([1, 1], gap="large")

with col1:
    st.subheader("📝 Input Parameters")
    
    # Input Form
    with st.form("prediction_form"):
        taluk = st.selectbox(
            "Select Taluk (A.Nagar District)",
            ["Ahmednagar", "Rahata", "Rahuri", "Sangamner", "Shrigonda", "Pathardi", "Parner"]
        )
        
        c1, c2 = st.columns(2)
        with c1:
            rainfall = st.number_input("Rainfall (mm)", min_value=0.0, max_value=2000.0, value=500.0, step=10.0)
            temperature = st.number_input("Temperature (°C)", min_value=10.0, max_value=50.0, value=30.0, step=1.0)
        
        with c2:
            humidity = st.number_input("Humidity (%)", min_value=0.0, max_value=100.0, value=65.0, step=1.0)
            ndvi = st.slider("NDVI Value (Vegetation Index)", 0.0, 1.0, 0.65)
        
        submit_btn = st.form_submit_button("Predict Yield 🚀")

# --- Mock Prediction Logic & Display ---
if submit_btn:
    with col2:
        st.subheader("📊 Prediction Results")
        
        # Simulate processing time
        with st.spinner("Analyzing parameters and predicting yield..."):
            time.sleep(1.5)
            
            # MOCK PREDICTION LOGIC (Replace this with actual model loading and inference)
            # Simple heuristic for demo: 
            # Base yield ~80. Higher rainfall/NDVI increases it slightly, extreme temp decreases it.
            base_yield = 80.0
            weather_factor = (rainfall / 1000.0) * 5.0
            ndvi_factor = ndvi * 20.0
            temp_penalty = abs(30 - temperature) * 0.5
            
            predicted_yield = base_yield + weather_factor + ndvi_factor - temp_penalty
            # Add some randomness for realism in demo
            predicted_yield += np.random.uniform(-5, 5)
            
            # Ensure valid range
            predicted_yield = max(10, min(150, predicted_yield))
        
        # Display Result
        st.markdown(f"""
            <div class='metric-card'>
                <h3 style='margin:0; color:#555;'>Estimated Yield</h3>
                <h1 style='font-size: 48px; color: #4CAF50; margin: 10px 0;'>
                    {predicted_yield:.2f} <span style='font-size: 24px;'>tons/ha</span>
                </h1>
                <p style='color: #888;'>For {taluk} Taluk</p>
            </div>
        """, unsafe_allow_html=True)
        
        st.write("") # Spacer
        
        # Visualization (Simple Bar Chart comparison)
        chart_data = pd.DataFrame({
            "Category": ["Average Yield", "Predicted Yield"],
            "Values (Tons/Ha)": [90, predicted_yield]
        })
        
        st.bar_chart(chart_data, x="Category", y="Values (Tons/Ha)", color=["#e0e0e0", "#4CAF50"])
        
        st.success("Prediction completed successfully!")

else:
    with col2:
        # Placeholder when no prediction is made yet
        st.info("👈 Enter parameters in the form and click 'Predict Yield' to see results here.")
        st.image("https://cdn-icons-png.flaticon.com/512/3135/3135679.png", width=150, caption="Waiting for input...")

