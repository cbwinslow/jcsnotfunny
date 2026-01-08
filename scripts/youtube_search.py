"""YouTube search utility to find channel and episodes.

Usage:
    python scripts/youtube_search.py --search "Jared's Not Funny"
    python scripts/youtube_search.py --channel-id CHANNEL_ID
"""
import os
import requests
import argparse
import json

API_KEY = os.environ.get('YT_API_KEY')
BASE_URL = 'https://www.googleapis.com/youtube/v3'


def search_channels(query, max_results=10):
    """Search for YouTube channels matching the query."""
    if not API_KEY:
        print("Error: YT_API_KEY not set in environment")
        return None

    url = f"{BASE_URL}/search"
    params = {
        'part': 'snippet',
        'q': query,
        'type': 'channel',
        'maxResults': max_results,
        'key': API_KEY
    }

    try:
        resp = requests.get(url, params=params, timeout=10)
        resp.raise_for_status()
        data = resp.json()

        print(f"\n📺 Channel Search Results for '{query}':\n")
        for item in data.get('items', []):
            channel_id = item['id']['channelId']
            title = item['snippet']['title']
            desc = item['snippet']['description']
            thumb = item['snippet']['thumbnails']['default']['url']
            print(f"  Title: {title}")
            print(f"  Channel ID: {channel_id}")
            print(f"  Description: {desc[:100]}..." if len(desc) > 100 else f"  Description: {desc}")
            print(f"  Thumbnail: {thumb}")
            print("-" * 50)
        return data
    except Exception as e:
        print(f"Error searching channels: {e}")
        return None


def search_videos(query, max_results=20):
    """Search for YouTube videos matching the query."""
    if not API_KEY:
        print("Error: YT_API_KEY not set in environment")
        return None

    url = f"{BASE_URL}/search"
    params = {
        'part': 'snippet',
        'q': query,
        'type': 'video',
        'maxResults': max_results,
        'key': API_KEY
    }

    try:
        resp = requests.get(url, params=params, timeout=10)
        resp.raise_for_status()
        data = resp.json()

        print(f"\n🎬 Video Search Results for '{query}':\n")
        for item in data.get('items', []):
            video_id = item['id']['videoId']
            title = item['snippet']['title']
            channel = item['snippet']['channelTitle']
            desc = item['snippet']['description']
            thumb = item['snippet']['thumbnails']['default']['url']
            print(f"  Title: {title}")
            print(f"  Video ID: {video_id}")
            print(f"  Channel: {channel}")
            print(f"  URL: https://youtu.be/{video_id}")
            print(f"  Description: {desc[:100]}..." if len(desc) > 100 else f"  Description: {desc}")
            print("-" * 50)
        return data
    except Exception as e:
        print(f"Error searching videos: {e}")
        return None


def get_channel_details(channel_id):
    """Get details about a specific channel."""
    if not API_KEY:
        print("Error: YT_API_KEY not set in environment")
        return None

    url = f"{BASE_URL}/channels"
    params = {
        'part': 'snippet,statistics,contentDetails',
        'id': channel_id,
        'key': API_KEY
    }

    try:
        resp = requests.get(url, params=params, timeout=10)
        resp.raise_for_status()
        data = resp.json()

        if data.get('items'):
            item = data['items'][0]
            snippet = item['snippet']
            stats = item.get('statistics', {})
            uploads_playlist = item['contentDetails']['relatedPlaylists']['uploads']

            print(f"\n📊 Channel Details for '{snippet['title']}':\n")
            print(f"  Description: {snippet['description']}")
            print(f"  Custom URL: {snippet.get('customUrl', 'N/A')}")
            print(f"  Subscriber Count: {stats.get('subscriberCount', 'N/A')}")
            print(f"  View Count: {stats.get('viewCount', 'N/A')}")
            print(f"  Video Count: {stats.get('videoCount', 'N/A')}")
            print(f"  Uploads Playlist: {uploads_playlist}")
            print(f"  Channel ID: {channel_id}")
            return data
        else:
            print(f"No channel found with ID: {channel_id}")
            return None
    except Exception as e:
        print(f"Error getting channel details: {e}")
        return None


def get_uploads_playlist(playlist_id, max_results=50):
    """Get videos from a channel's uploads playlist."""
    if not API_KEY:
        print("Error: YT_API_KEY not set in environment")
        return None

    url = f"{BASE_URL}/playlistItems"
    params = {
        'part': 'snippet,contentDetails',
        'playlistId': playlist_id,
        'maxResults': max_results,
        'key': API_KEY
    }

    try:
        resp = requests.get(url, params=params, timeout=10)
        resp.raise_for_status()
        data = resp.json()

        print(f"\n🎥 Latest Uploads ({len(data.get('items', []))} videos):\n")
        for item in data.get('items', []):
            video_id = item['contentDetails']['videoId']
            title = item['snippet']['title']
            published = item['snippet']['publishedAt']
            desc = item['snippet']['description']
            print(f"  Title: {title}")
            print(f"  Video ID: {video_id}")
            print(f"  URL: https://youtu.be/{video_id}")
            print(f"  Published: {published[:10]}")
            print("-" * 50)
        return data
    except Exception as e:
        print(f"Error getting uploads: {e}")
        return None


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='YouTube Search Utility')
    parser.add_argument('--search', '-s', type=str, help='Search query')
    parser.add_argument('--channel-id', '-c', type=str, help='Get channel details by ID')
    parser.add_argument('--uploads', '-u', type=str, help='Get uploads from playlist ID')
    parser.add_argument('--videos', '-v', action='store_true', help='Search for videos instead of channels')
    parser.add_argument('--max-results', '-m', type=int, default=10, help='Max results (default: 10)')

    args = parser.parse_args()

    if not API_KEY:
        print("❌ YT_API_KEY environment variable not set!")
        print("   Set it with: export YT_API_KEY='your_api_key'")
        print("   Or add it to your .env file")
        exit(1)

    if args.channel_id:
        get_channel_details(args.channel_id)
        if args.uploads:
            get_uploads_playlist(args.uploads, args.max_results)
    elif args.uploads:
        get_uploads_playlist(args.uploads, args.max_results)
    elif args.search:
        if args.videos:
            search_videos(args.search, args.max_results)
        else:
            search_channels(args.search, args.max_results)
    else:
        parser.print_help()
