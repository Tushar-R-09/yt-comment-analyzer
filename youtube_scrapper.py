from urllib.parse import urlparse, parse_qs
from googleapiclient.discovery import build
import os
from dotenv import load_dotenv

load_dotenv()
API_KEY = os.getenv("YOUTUBE_API_KEY")

def extract_video_id(url: str) -> str:
    """Extracts the YouTube video ID from a given URL."""
    parsed_url = urlparse(url)
    if parsed_url.hostname == 'youtu.be':
        return parsed_url.path[1:]
    elif parsed_url.hostname in ('www.youtube.com', 'youtube.com'):
        if parsed_url.path == '/watch':
            return parse_qs(parsed_url.query)['v'][0]
        elif parsed_url.path.startswith('/embed/'):
            return parsed_url.path.split('/')[2]
    raise ValueError("Invalid YouTube URL")




def get_youtube_comments(video_id: str, api_key: str, max_comments: int = 100):
    """Fetches comments from a YouTube video using the YouTube Data API."""
    youtube = build('youtube', 'v3', developerKey=api_key)
    comments = []
    
    request = youtube.commentThreads().list(
        part="snippet",
        videoId=video_id,
        maxResults=100,
        textFormat="plainText"
    )
    response = request.execute()

    while response:
        for item in response['items']:
            comment = item['snippet']['topLevelComment']['snippet']['textDisplay']
            comments.append(comment)

        # Check if there’s a next page of comments
        if 'nextPageToken' in response and len(comments) < max_comments:
            request = youtube.commentThreads().list(
                part="snippet",
                videoId=video_id,
                pageToken=response['nextPageToken'],
                maxResults=100,
                textFormat="plainText"
            )
            response = request.execute()
        else:
            break
    
    return comments[:max_comments]

def get_comments(video_url: str, max_comments: int = 100):
    video_id = extract_video_id(video_url)
    return get_youtube_comments(video_id, API_KEY, max_comments)


if __name__ == "__main__":
    video_url = "https://www.youtube.com/watch?v=q2aENKR59w4"
    comments = get_comments(video_url, max_comments=10)
    for idx, comment in enumerate(comments):
        print(f"{idx + 1}: {comment}\n")
