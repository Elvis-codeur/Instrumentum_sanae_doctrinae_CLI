import os
import sys
import json
import argparse
import pandas as pd
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor
import yt_dlp

def parse_arguments():
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(description='Download metadata of all videos from a YouTube channel using yt-dlp')
    parser.add_argument('channel_url', type=str, help='URL of the YouTube channel')
    parser.add_argument('--output-dir', type=str, default='output', help='Directory to save output files')
    parser.add_argument('--format', type=str, choices=['json', 'csv', 'both'], default='both', help='Output format')
    parser.add_argument('--threads', type=int, default=4, help='Number of threads for parallel processing')
    parser.add_argument('--limit', type=int, default=None, help='Limit the number of videos to process')
    return parser.parse_args()

def get_channel_info(channel_url):
    """Get basic information about the channel."""
    ydl_opts = {
        'skip_download': True,
        'extract_flat': True,
        'quiet': True,
    }
    
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        try:
            info = ydl.extract_info(channel_url, download=False)
            return info
        except yt_dlp.utils.DownloadError as e:
            print(f"Error getting channel info: {e}")
            sys.exit(1)

def get_video_metadata(video_url, index=None, total=None):
    """Get detailed metadata for a single video."""
    ydl_opts = {
        'skip_download': True,
        'quiet': True,
        'no_warnings': True,
    }
    
    if index is not None and total is not None:
        print(f"Processing video {index}/{total}: {video_url}")
    
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        try:
            info = ydl.extract_info(video_url, download=False)
            return info
        except Exception as e:
            print(f"Error processing {video_url}: {e}")
            return None

def process_videos(video_entries, num_threads=4, limit=None):
    """Process videos in parallel using multiple threads."""
    videos_to_process = video_entries[:limit] if limit else video_entries
    total_videos = len(videos_to_process)
    
    print(f"Processing {total_videos} videos using {num_threads} threads...")
    
    all_metadata = []
    
    with ThreadPoolExecutor(max_workers=num_threads) as executor:
        future_to_url = {
            executor.submit(
                get_video_metadata, 
                entry['url'], 
                i+1, 
                total_videos
            ): entry for i, entry in enumerate(videos_to_process)
        }
        
        for future in future_to_url:
            metadata = future.result()
            if metadata:
                all_metadata.append(metadata)
    
    return all_metadata

def extract_useful_metadata(metadata_list):
    """Extract and normalize useful metadata from each video."""
    useful_data = []
    
    for video in metadata_list:
        if not video:
            continue
            
        # Extract the most useful fields
        video_data = {
            'id': video.get('id'),
            'title': video.get('title'),
            'url': video.get('webpage_url'),
            'upload_date': video.get('upload_date'),  # YYYYMMDD format
            'uploader': video.get('uploader'),
            'uploader_id': video.get('uploader_id'),
            'uploader_url': video.get('uploader_url'),
            'channel_id': video.get('channel_id'),
            'channel_url': video.get('channel_url'),
            'duration': video.get('duration'),  # in seconds
            'view_count': video.get('view_count'),
            'like_count': video.get('like_count'),
            'comment_count': video.get('comment_count'),
            'tags': video.get('tags', []),
            'categories': video.get('categories', []),
            'description': video.get('description'),
            'thumbnail': video.get('thumbnail'),
            'age_limit': video.get('age_limit', 0),
            'was_live': video.get('was_live', False),
            'live_status': video.get('live_status'),
            'release_timestamp': video.get('release_timestamp'),
            'availability': video.get('availability'),
            'original_url': video.get('original_url'),
            'webpage_url_basename': video.get('webpage_url_basename'),
            'extractor': video.get('extractor'),
            'extractor_key': video.get('extractor_key'),
        }
        
        # Convert upload_date to a more readable format
        if video_data['upload_date']:
            try:
                date_obj = datetime.strptime(video_data['upload_date'], '%Y%m%d')
                video_data['upload_date_formatted'] = date_obj.strftime('%Y-%m-%d')
            except ValueError:
                video_data['upload_date_formatted'] = video_data['upload_date']
        
        useful_data.append(video_data)
    
    return useful_data

def save_metadata(metadata, output_dir, format_type='both', channel_name=None):
    """Save metadata to JSON and/or CSV files."""
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    # Create a timestamp for the filenames
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    
    # Use channel name in filename if available
    base_filename = f"{channel_name}_{timestamp}" if channel_name else f"youtube_metadata_{timestamp}"
    
    if format_type in ['json', 'both']:
        json_path = os.path.join(output_dir, f"{base_filename}.json")
        with open(json_path, 'w', encoding='utf-8') as f:
            json.dump(metadata, f, ensure_ascii=False, indent=4)
        print(f"Saved JSON metadata to {json_path}")
    
    if format_type in ['csv', 'both']:
        # For CSV, we need to normalize the data (flatten lists)
        flattened_data = []
        for video in metadata:
            video_copy = video.copy()
            
            # Convert lists to strings
            for key, value in video_copy.items():
                if isinstance(value, list):
                    video_copy[key] = '|'.join(str(item) for item in value)
            
            flattened_data.append(video_copy)
        
        # Create DataFrame and save to CSV
        df = pd.DataFrame(flattened_data)
        csv_path = os.path.join(output_dir, f"{base_filename}.csv")
        df.to_csv(csv_path, index=False, encoding='utf-8')
        print(f"Saved CSV metadata to {csv_path}")

def main():
    args = parse_arguments()
    
    print(f"Getting information for channel: {args.channel_url}")
    channel_info = get_channel_info(args.channel_url)
    
    # Extract channel name for the filename
    channel_name = channel_info.get('title', '').replace(' ', '_').lower()
    if not channel_name:
        channel_name = "channel"
    
    # Process videos based on channel type
    if 'entries' in channel_info:
        video_entries = channel_info['entries']
        print(f"Found {len(video_entries)} videos in the channel")
        
        # Process videos and get detailed metadata
        metadata_list = process_videos(video_entries, args.threads, args.limit)
        useful_metadata = extract_useful_metadata(metadata_list)
        
        # Save the results
        save_metadata(useful_metadata, args.output_dir, args.format, channel_name)
        
        print(f"Successfully processed {len(useful_metadata)} videos")
    else:
        print("No videos found in the channel or this might not be a channel URL")
        sys.exit(1)

if __name__ == "__main__":
    main()