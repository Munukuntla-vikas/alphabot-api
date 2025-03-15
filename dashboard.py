import streamlit as st
import requests
import pandas as pd

API_URL = "http://127.0.0.1:10000/process-message"  # Change this if deployed online

st.title("📊 Alphabot Sentiment Dashboard")

group_id = st.text_input("Enter Group ID", "123")

message = st.text_area("Enter a test message:")
if st.button("Analyze Message"):
    if message.strip():
        response = requests.post(API_URL, json={"group_id": group_id, "message": message})
        if response.status_code == 200:
            data = response.json()
            st.success("✅ Analysis Complete!")

            # Sentiment Analysis
            st.subheader("📈 Sentiment Analysis")
            st.write(f"**Sentiment:** {data.get('sentiment', 'N/A')}")

            # Trending Topics
            st.subheader("🔥 Trending Topics")
            if data.get("trending_topics"):
                st.write(pd.DataFrame(data["trending_topics"].items(), columns=["Topic", "Keywords"]))

            # Influencer Mentions
            st.subheader("🔍 Influencer Mentions")
            influencers = data.get("influencer_mentions", [])
            if influencers:
                st.write(", ".join(influencers))
            else:
                st.write("No influencers mentioned.")
        else:
            st.error("❌ API Error. Check logs.")
    else:
        st.warning("⚠️ Please enter a message.")

st.markdown("---")
st.caption("Alphabot Dashboard - Real-time sentiment and trend tracking.")
