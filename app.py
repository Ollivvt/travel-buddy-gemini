import streamlit as st
import datetime
import json
from utils import initialize_gemini, generate_itinerary

# Page configuration
st.set_page_config(
    page_title="Smart Travel Genie",
    page_icon="🧳",
    layout="wide"
)

# Title and introduction
st.title("🧳 Smart Travel Genie: AI-Powered Travel Itinerary Planner")
st.markdown("""
Planning a trip can be stressful, especially when you're trying to balance time, budget, and personal interests.
Let our AI assistant create a customized day-by-day itinerary based on your preferences!
""")

# Initialize Gemini client
try:
    client = initialize_gemini()
    if client:
        st.session_state.api_connected = True
    else:
        st.session_state.api_connected = False
except Exception as e:
    st.session_state.api_connected = False
    st.error(f"Error connecting to Gemini API: {str(e)}")

# Sidebar for user inputs
with st.sidebar:
    st.header("✏️ Your Travel Details")
    
    # Destination input
    destination = st.text_input("Destination", placeholder="e.g. Kyoto, Paris, New York")
    
    # Date selection
    col1, col2 = st.columns(2)
    with col1:
        today = datetime.date.today()
        start_date = st.date_input("Start Date", value=today)
    with col2:
        end_date = st.date_input("End Date", value=today + datetime.timedelta(days=7))
    
    # Budget selection
    budget_options = ["budget", "moderate", "luxury"]
    budget = st.select_slider("Budget Level", options=budget_options, value="moderate")
    
    # Travel interests
    st.write("Select your interests:")
    interests = []
    interest_options = [
        "architecture", "art", "beaches", "culture", "family", "festivals", 
        "food", "hiking", "history", "museums", "nature", "nightlife", 
        "photography", "shopping", "temples", "wildlife"
    ]
    
    # Display interests as multi-select
    selected_interests = st.multiselect("Your Interests", options=interest_options, default=["nature", "food"])
    
    # Generate button
    generate_button = st.button("✨ Generate Itinerary", type="primary", use_container_width=True)
    
    # Display API connection status
    if hasattr(st.session_state, 'api_connected'):
        if st.session_state.api_connected:
            st.success("✅ API Connected")
        else:
            st.error("❌ API Not Connected")
    
    st.markdown("---")
    st.markdown("Made with ❤️ and Streamlit")

# Generate itinerary when button is clicked
if generate_button:
    if not hasattr(st.session_state, 'api_connected') or not st.session_state.api_connected:
        st.error("Cannot generate itinerary: API not connected")
    elif not destination:
        st.error("Please enter a destination")
    elif start_date > end_date:
        st.error("Start date must be before end date")
    elif not selected_interests:
        st.error("Please select at least one interest")
    else:
        user_input = {
            "destination": destination,
            "start_date": start_date.strftime("%Y-%m-%d"),
            "end_date": end_date.strftime("%Y-%m-%d"),
            "budget": budget,
            "interests": selected_interests
        }
        
        # Display loading spinner during generation
        with st.spinner("🧠 Generating your personalized travel itinerary..."):
            try:
                itinerary_days = generate_itinerary(client, user_input)
                if itinerary_days:
                    st.session_state.itinerary = itinerary_days
                else:
                    st.error("Failed to generate itinerary. Please try again.")
            except Exception as e:
                st.error(f"Error generating itinerary: {str(e)}")

# Display the generated itinerary if it exists in session state
if hasattr(st.session_state, 'itinerary') and st.session_state.itinerary:
    st.header(f"🌍 Your Personalized Itinerary for {destination}")
    
    trip_length = len(st.session_state.itinerary)
    st.subheader(f"{trip_length} Day Trip • {budget.capitalize()} Budget • {', '.join(selected_interests)}")
    
    # Create tabs for each day
    day_tabs = st.tabs([f"Day {day['day']}" for day in st.session_state.itinerary])
    
    # Fill each tab with the day's itinerary
    for i, day_tab in enumerate(day_tabs):
        day_data = st.session_state.itinerary[i]
        
        with day_tab:
            st.markdown(f"### {day_data['summary']}")
            
            # Morning, Afternoon, Evening sections
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.markdown("#### ☀️ Morning")
                st.markdown(day_data['morning'])
            
            with col2:
                st.markdown("#### 🌤️ Afternoon")
                st.markdown(day_data['afternoon'])
            
            with col3:
                st.markdown("#### 🌙 Evening")
                st.markdown(day_data['evening'])
