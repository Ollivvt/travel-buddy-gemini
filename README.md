# 🧳 Smart Travel Genie

<img src="https://github.com/user-attachments/assets/ef575bb3-d98f-4db7-9c3e-e1c24d63d226" alt="Smart Travel Genie Banner" width="600">

> AI-powered travel itinerary generation - from overwhelming options to perfect personalization in seconds.

## 🚀 Project Overview

**Smart Travel Genie** transforms travel planning by using generative AI to create personalized day-by-day itineraries based on your preferences. This project was developed as my capstone for the **Google x Kaggle Gen AI Intensive 2025**.

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://smart-travel-genie.streamlit.app/)

## 🌍 The Problem: Planning Travel Is Overwhelming

Traveling should be fun, but planning a trip? Not so much. Between blogs, maps, hotel sites, weather forecasts, and food reviews, most of us spend hours researching where to go and what to do. It's time-consuming, fragmented, and exhausting.

I wanted to explore how **Generative AI** could simplify that process.

## 🤖 The Solution: AI as a Personal Travel Assistant

In this project, I built a **Smart Travel Genie**: an AI tool that takes in a few simple inputs (destination, dates, budget, interests) and instantly generates a **personalized, structured, multi-day travel itinerary**.

The project uses three core Gen AI capabilities:
* **Structured Output**: Returns clean JSON itineraries, ready to format or parse
* **Few-Shot Prompting**: Teaches the model to match tone/style using example trips (e.g., "luxury foodie" vs "budget backpacker")
* **Simulated Retrieval**: Instead of a real database, user inputs (like "temples" or "local food") are used to guide itinerary content

## ✨ Features

- **AI-Powered Itinerary Creation**: Generate complete travel plans with a single click
- **Personalization**: Customize by destination, travel dates, budget level, and interests
- **Interest-Based Recommendations**: 16 different interest categories (food, nature, history, etc.)
- **Day-by-Day Structure**: Clear breakdown of activities by day and time period (morning/afternoon/evening)
- **Responsive Design**: Optimized layout that works on both desktop and mobile devices
- **Real-Time Generation**: Watch as your custom itinerary builds before your eyes


## 🛠️ Technologies

- **Frontend**: Streamlit (Python-based web app framework)
- **AI Model**: Google Gemini API
- **Language**: Python 3.11+
- **Deployment**: Streamlit Cloud

## 🔧 Installation

1. Clone this repository:
```bash
git clone https://github.com/username/travel-buddy-gemini.git

cd travel-buddy-gemini
```

2. Create a virtual environment and install dependencies:
```bash
python -m venv venv

source venv/bin/activate  # On Windows: venv\Scripts\activate

pip install -r requirements.txt
```

3. Set up your environment variables:
```bash
# Create .env file with your API key
echo "GEMINI_API_KEY=your_api_key_here" > .env
```

4. Run the application:
```bash
streamlit run app.py
```

## 📐 Architecture
The application follows a simple but effective architecture:

1. User Interface (Streamlit): Collects travel preferences and displays results
2. Prompt Engineering Layer: Transforms user inputs into optimized queries
3. AI Integration (Gemini API): Processes the prompt to generate structured travel content
4. Response Parser: Transforms API responses into formatted itinerary displays

### How It Works:
```
User Input → Prompt Engineering → Gemini API → JSON Response → Formatted Display
```

## 🚀 Future Enhancements

- [ ] Map Integration: Visualize daily activities on an interactive map
- [ ] Image Generation: AI-generated images of recommended locations
- [ ] Local Insights: Add cultural tips and local customs information
- [ ] Weather Integration: Incorporate weather forecasts into planning
- [ ] Itinerary Export: PDF/calendar export functionality
- [ ] Restaurant & Hotel Booking Links: Direct integration with booking platforms

## 🧠 Lessons Learned
Through this capstone project, I've gained valuable insights into:

- Effective prompt engineering for structured outputs
- Balancing user customization with AI simplicity
- Creating intuitive UI/UX for AI-powered applications
- Optimizing LLM responses for factual accuracy in travel recommendations

## 👏 Acknowledgements

- Google x Kaggle Gen AI Intensive 2025 program and mentors
- Streamlit for their amazing framework for rapid AI application development
- Google for access to the Gemini API
- Travel bloggers whose public content helped with prompt examples and validation
