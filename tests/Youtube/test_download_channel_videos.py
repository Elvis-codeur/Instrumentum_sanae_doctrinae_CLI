from pytube import Channel



def test1():    
    # Replace with the channel URL
    channel_url = "https://www.youtube.com/@ahavajerusalem"

    # Initialize the channel
    channel = Channel(channel_url)

    print(channel.video_urls)
    # Print or store video IDs
    for url in channel.video_urls:
        video_id = url.split("v=")[-1]
        print(video_id)
        

def test2():

    channel = Channel("https://www.youtube.com/@ligonier")

    print(f"Channel title: {channel.channel_name}")
    print(f"Found {len(channel.video_urls)} videos.")

if __name__ == "__main__":
    test2()
