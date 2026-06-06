import streamlit as st
import requests

S_URL = "https://weather-be-2.onrender.com"

st.title("🌤 AI Weather Agent")

city = st.text_input("Enter City")

question = st.text_input(
    "Ask Your Weather Question"
)

if st.button("Ask Agent"):

    try:

        res = requests.post(
            f"{S_URL}/get_weather",
            params={
                "city": city,
                "question": question
            }
        )

        if res.status_code == 200:

            data = res.json()

            st.success("Answer Generated")

            st.write("### City")
            st.write(data["city"])

            st.write("### Question")
            st.write(data["question"])

            st.write("### Answer")
            st.write(data["answer"])

        else:
            st.error(res.text)

    except Exception as e:
        st.error(str(e))
