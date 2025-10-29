from youtube_scrapper import get_comments
from transformers import pipeline
import pandas as pd
import matplotlib.pyplot as plt


# Initialize the sentiment model
sentiment_model = pipeline(
    "text-classification",
    model="j-hartmann/emotion-english-distilroberta-base",
    return_all_scores=False,
    truncation=True,         # ensures text is auto-truncated
    max_length=512           # max token length for distilroberta
)

def analyze_sentiment_transformer(comment):
    """Returns sentiment label and confidence score using a Transformer model."""
    result = sentiment_model(comment[:512])[0]   # limit to 512 tokens for safety
    label = result['label']
    score = result['score']
    return label, round(score, 3)

def main(video_url, max_comments=100):

    comments = get_comments(video_url, max_comments)
    data = []

    for comment in comments:
        label, score = analyze_sentiment_transformer(comment)
        data.append({"Comment": comment, "Sentiment": label, "Confidence": score})

    df = pd.DataFrame(data)

    return df


if __name__ == "__main__":

    video_url = "https://www.youtube.com/watch?v=q2aENKR59w4"
    comment_analysis_df = main(video_url, max_comments=1000)
    # Plot sentiment distribution
    plt.figure(figsize=(8, 5))
    comment_analysis_df['Sentiment'].value_counts().plot(
        kind='bar', 
        color='skyblue',
        edgecolor='black'
    )
    plt.title("Distribution of Sentiments in YouTube Comments", fontsize=14)
    plt.xlabel("Sentiment", fontsize=12)
    plt.ylabel("Number of Comments", fontsize=12)
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()
