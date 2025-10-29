import streamlit as st
import matplotlib.pyplot as plt
from main import main as analyze_video  # importing main function from main.py

st.set_page_config(page_title="YouTube Comment Sentiment Analyzer", layout="wide")
st.title("🎬 YouTube Comment Sentiment Analyzer")

# --- Input section ---
video_url = st.text_input("Enter YouTube Video URL:")
max_comments = st.number_input("Number of comments to analyze:", min_value=10, max_value=1000, value=100, step=10)

if st.button("Analyze Sentiment"):
    if not video_url.strip():
        st.warning("⚠️ Please enter a valid YouTube video URL.")
    else:
        with st.spinner("Fetching and analyzing comments... ⏳"):
            comment_analysis_df = analyze_video(video_url, max_comments=max_comments)

        if comment_analysis_df.empty:
            st.error("No comments found or unable to process this video.")
        else:
            st.success(f"✅ Analysis complete! Processed {len(comment_analysis_df)} comments.")

            # Display table
            st.subheader("📋 Sentiment Analysis Results")
            st.dataframe(comment_analysis_df)

            # Plot sentiment distribution
            st.subheader("📊 Sentiment Distribution")
            sentiment_counts = comment_analysis_df['Sentiment'].value_counts()

            fig, ax = plt.subplots(figsize=(8, 5))
            sentiment_counts.plot(kind='bar', color='skyblue', edgecolor='black', ax=ax)
            ax.set_title("Distribution of Sentiments in YouTube Comments", fontsize=14)
            ax.set_xlabel("Sentiment", fontsize=12)
            ax.set_ylabel("Number of Comments", fontsize=12)
            plt.xticks(rotation=45)
            plt.tight_layout()

            st.pyplot(fig)
