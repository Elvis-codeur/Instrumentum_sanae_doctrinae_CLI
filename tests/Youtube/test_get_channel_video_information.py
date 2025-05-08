import os
import google_auth_oauthlib.flow
import googleapiclient.discovery
import googleapiclient.errors
import pandas as pd
import json
from datetime import datetime

def get_authenticated_service():
    """
    Create a YouTube API service instance using API key.
    Returns: An authenticated YouTube API service instance.
    """
    api_service_name = "youtube"
    api_version = "v3"
    
    # Replace with your actual API key
    API_KEY = "YOUR_API_KEY"  
    
    youtube = googleapiclient.discovery.build(
        api_service_name, api_version, developerKey=API_KEY)
    
    return youtube

def get_channel_id_from_username(youtube, username):
    """
    Get channel ID from a username.
    Args:
        youtube: Authenticated YouTube API service instance
        username: YouTube channel username
    Returns:
        Channel ID as string
    """
    request = youtube.channels().list(
        part="id",
        forUsername=username
    )
    response = request.execute()
    
    if response['items']:
        return response['items'][0]['id']
    else:
        print(f"No channel found for username: {username}")
        return None

def get_all_channel_videos(youtube, channel_id):
    """
    Get all videos from a channel.
    Args:
        youtube: Authenticated YouTube API service instance
        channel_id: YouTube channel ID
    Returns:
        List of video information dictionaries
    """
    all_videos = []
    next_page_token = None
    
    # First, get all playlist IDs for the channel
    request = youtube.channels().list(
        part="contentDetails",
        id=channel_id
    )
    response = request.execute()
    
    if not response['items']:
        print(f"No channel found for ID: {channel_id}")
        return all_videos
    
    # Get the uploads playlist ID
    uploads_playlist_id = response['items'][0]['contentDetails']['relatedPlaylists']['uploads']
    
    # Now get all videos from the uploads playlist
    while True:
        request = youtube.playlistItems().list(
            part="snippet,contentDetails",
            playlistId=uploads_playlist_id,
            maxResults=50,  # Maximum allowed by API
            pageToken=next_page_token
        )
        response = request.execute()
        
        # Add each video to our list
        for item in response['items']:
            video_id = item['contentDetails']['videoId']
            
            # Get more detailed video information
            video_request = youtube.videos().list(
                part="snippet,contentDetails,statistics",
                id=video_id
            )
            video_response = video_request.execute()
            
            if video_response['items']:
                video_info = video_response['items'][0]
                
                # Extract the information we want
                video_data = {
                    'video_id': video_id,
                    'title': video_info['snippet']['title'],
                    'description': video_info['snippet']['description'],
                    'published_at': video_info['snippet']['publishedAt'],
                    'channel_id': video_info['snippet']['channelId'],
                    'channel_title': video_info['snippet']['channelTitle'],
                    'duration': video_info['contentDetails']['duration'],
                    'view_count': video_info['statistics'].get('viewCount', 0),
                    'like_count': video_info['statistics'].get('likeCount', 0),
                    'comment_count': video_info['statistics'].get('commentCount', 0),
                    'tags': video_info['snippet'].get('tags', []),
                    'thumbnail_url': video_info['snippet']['thumbnails']['high']['url']
                }
                
                all_videos.append(video_data)
                print(f"Added video: {video_data['title']}")
        
        # Check if there are more pages
        next_page_token = response.get('nextPageToken')
        if not next_page_token:
            break
    
    return all_videos

def save_to_csv(videos, filename="youtube_videos.csv"):
    """
    Save video information to a CSV file.
    Args:
        videos: List of video information dictionaries
        filename: Output CSV filename
    """
    df = pd.DataFrame(videos)
    df.to_csv(filename, index=False)
    print(f"Saved {len(videos)} videos to {filename}")

def save_to_json(videos, filename="youtube_videos.json"):
    """
    Save video information to a JSON file.
    Args:
        videos: List of video information dictionaries
        filename: Output JSON filename
    """
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(videos, f, ensure_ascii=False, indent=4)
    print(f"Saved {len(videos)} videos to {filename}")

def main():
    # Get authenticated YouTube service
    youtube = get_authenticated_service()
    
    # Ask user for channel information
    print("Enter YouTube channel information:")
    print("1. Channel ID")
    print("2. Username")
    choice = input("Choose an option (1/2): ")
    
    channel_id = None
    
    if choice == "1":
        channel_id = input("Enter the channel ID: ")
    elif choice == "2":
        username = input("Enter the username: ")
        channel_id = get_channel_id_from_username(youtube, username)
    else:
        print("Invalid choice. Exiting.")
        return
    
    if not channel_id:
        print("Could not find channel. Exiting.")
        return
    
    # Get all videos
    print(f"Fetching videos for channel ID: {channel_id}")
    videos = get_all_channel_videos(youtube, channel_id)
    
    if not videos:
        print("No videos found.")
        return
    
    # Save the data
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    save_to_csv(videos, f"youtube_videos_{timestamp}.csv")
    save_to_json(videos, f"youtube_videos_{timestamp}.json")

if __name__ == "__main__":
    main()