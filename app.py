import streamlit as st
import requests

# =========================
# BACKEND URL (CHANGE THIS)
# =========================
BACKEND_URL = "https://weather-be-2.onrender.com"

st.set_page_config(page_title="AI Travel Planner", layout="wide")

# =========================
# TITLE
# =========================
st.title("🌍 AI Travel Planner ✈️")

# =========================
# SIDEBAR INPUTS
# =========================
st.sidebar.header("🧳 Plan Your Trip")

city = st.sidebar.text_input("📍 Destination", "Goa")
days = st.sidebar.number_input("📅 Number of Days", min_value=1, value=5)
budget = st.sidebar.number_input("💰 Budget Per Day (INR)", min_value=500, value=2000)

generate = st.sidebar.button("🚀 Generate Plan")

# =========================
# MAIN UI
# =========================
if generate:

    with st.spinner("Generating your AI travel plan..."):

        # API CALL
        res = requests.get(
            f"{BACKEND_URL}/plan-trip",
            params={
                "city": city,
                "days": days,
                "budget_per_day": budget
            }
        )

        if res.status_code != 200:
            st.error("❌ Failed to fetch data from backend")
            st.stop()

        data = res.json()

    # =========================
    # HEADER SECTION
    # =========================
    st.subheader(f"📍 Destination: {city}")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric("📅 Trip Duration", f"{days} Days")

    with col2:
        st.metric("💰 Total Budget", f"₹{budget * days}")

    with col3:
    weather = data["weather"]
    if "temperature" in weather:
        st.metric("🌦 Temp", f"{weather['temperature']}°C")

st.divider()

# =========================
# WEATHER SECTION
# =========================
st.subheader("🌦 Weather Overview")

if "temperature" in data["weather"]:
    st.success(
        f"{data['weather']['weather']} | "
        f"{data['weather']['temperature']}°C | "
        f"Humidity {data['weather']['humidity']}%"
    )
else:
    st.warning("Weather data not available")

st.divider()

    # =========================
    # RECOMMENDATIONS
    # =========================
    st.subheader("🔎 Travel Recommendations")

    for item in data["recommendations"]["results"]:
        st.write("👉", item)

    st.divider()

    # =========================
    # BUDGET BREAKDOWN
    # =========================
    st.subheader("💰 Budget Breakdown")

    total = data["budget"]["total_budget"]

    col1, col2 = st.columns(2)

    with col1:
        st.info(f"Per Day Cost: ₹{budget}")
        st.info(f"Total Days: {days}")

    with col2:
        st.success(f"Total Estimated Budget: ₹{total}")

    st.divider()

    # =========================
    # FINAL MESSAGE
    # =========================
    st.success("✈️ Your AI Travel Plan is Ready!")
