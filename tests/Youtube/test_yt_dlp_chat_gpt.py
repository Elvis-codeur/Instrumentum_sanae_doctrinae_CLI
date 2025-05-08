import yt_dlp
import json

# Replace with the URL of the channel (supports @handle, /channel/UC..., /c/...)
channel_url = "https://www.youtube.com/@Heartcrymissionary"

# Options for yt-dlp (we set 'extract_flat' to True to avoid downloading)
ydl_opts = {
    'extract_flat': True,      # Don't download, just get metadata
    'quiet': True,
    'force_generic_extractor': False,
    'dump_single_json': True   # Return all videos in a single JSON object
}

# Use yt-dlp to extract metadata
with yt_dlp.YoutubeDL(ydl_opts) as ydl:
    info = ydl.extract_info(channel_url, download=False)

# Print the number of videos found
print(f"Found {len(info['entries'])} videos in channel: {info['title']}")

# Save to JSON file
with open("channel_videos_metadata.json", "w", encoding="utf-8") as f:
    json.dump(info['entries'], f, indent=2, ensure_ascii=False)

# Optionally print some of the metadata
for video in info['entries'][:5]:  # Show first 5 videos
    print(f"{video['id']} - {video['title']}")
