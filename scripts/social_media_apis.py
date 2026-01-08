import requests
import json
import os
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Union
import base64


class TwitterAPI:
    def __init__(self):
        self.api_key = os.getenv("TWITTER_API_KEY") or ""
        self.api_secret = os.getenv("TWITTER_API_SECRET") or ""
        self.access_token = os.getenv("TWITTER_ACCESS_TOKEN") or ""
        self.access_token_secret = os.getenv("TWITTER_ACCESS_TOKEN_SECRET") or ""
        self.bearer_token = os.getenv("TWITTER_BEARER_TOKEN") or ""
        self.base_url = "https://api.twitter.com/2"

    def post_tweet(
        self,
        content: str,
        media_ids: Optional[List[str]] = None,
        schedule_time: Optional[str] = None,
    ) -> Dict:
        """Post a tweet with optional media and scheduling"""
        url = f"{self.base_url}/tweets"

        payload: Dict[str, Union[str, List[str], Dict[str, List[str]]]] = {
            "text": content
        }

        if media_ids:
            payload["media"] = {"media_ids": media_ids}

        headers = {
            "Authorization": f"Bearer {self.bearer_token}",
            "Content-Type": "application/json",
        }

        response = requests.post(url, headers=headers, json=payload)
        return response.json()

    def upload_media(self, file_path: str) -> Dict:
        """Upload media to Twitter"""
        url = "https://upload.twitter.com/1.1/media/upload.json"

        with open(file_path, "rb") as file:
            files = {"media": file}
            data = {
                "media_category": "tweet_image",
                "additional_owners": "1446144350646640640",
            }

            if self.api_key and self.api_secret:
                auth = (self.api_key, self.api_secret)
                response = requests.post(url, files=files, data=data, auth=auth)
            else:
                response = requests.post(url, files=files, data=data)
            return response.json()

    def get_user_tweets(self, username: str, max_results: int = 10) -> Dict:
        """Get recent tweets from a user"""
        url = f"{self.base_url}/tweets/search/recent"

        query = f"from:{username}"
        params = {
            "query": query,
            "max_results": max_results,
            "tweet.fields": "created_at,public_metrics",
        }

        headers = {"Authorization": f"Bearer {self.bearer_token}"}

        response = requests.get(url, headers=headers, params=params)
        return response.json()

    def schedule_tweet(
        self,
        content: str,
        publish_time: datetime,
        media_ids: Optional[List[str]] = None,
    ) -> Dict:
        """Schedule a tweet for future publication"""
        # Note: Twitter scheduling requires Premium API
        url = f"{self.base_url}/tweets"

        payload: Dict[str, Union[str, List[str], Dict[str, List[str]]]] = {
            "text": content,
            "scheduled_for": publish_time.isoformat(),
        }

        if media_ids:
            payload["media"] = {"media_ids": media_ids}

        headers = {
            "Authorization": f"Bearer {self.bearer_token}",
            "Content-Type": "application/json",
        }

        response = requests.post(url, headers=headers, json=payload)
        return response.json()


class InstagramAPI:
    def __init__(self):
        self.access_token = os.getenv("INSTAGRAM_ACCESS_TOKEN") or ""
        self.business_account_id = os.getenv("INSTAGRAM_BUSINESS_ID") or ""
        self.base_url = "https://graph.facebook.com/v18.0"

    def post_photo(self, image_url: str, caption: str) -> Dict:
        """Post a photo to Instagram"""
        url = f"{self.base_url}/{self.business_account_id}/media"

        params = {
            "image_url": image_url,
            "caption": caption,
            "access_token": self.access_token,
        }

        response = requests.post(url, params=params)
        creation_id = response.json().get("id")

        # Publish the media
        if creation_id:
            publish_url = f"{self.base_url}/{self.business_account_id}/media_publish"
            publish_params = {
                "creation_id": creation_id,
                "access_token": self.access_token,
            }
            publish_response = requests.post(publish_url, params=publish_params)
            return publish_response.json()

        return response.json()

    def post_reel(self, video_url: str, caption: str) -> Dict:
        """Post a reel to Instagram"""
        url = f"{self.base_url}/{self.business_account_id}/media"

        params = {
            "media_type": "REELS",
            "video_url": video_url,
            "caption": caption,
            "access_token": self.access_token,
        }

        response = requests.post(url, params=params)
        creation_id = response.json().get("id")

        # Publish the reel
        if creation_id:
            publish_url = f"{self.base_url}/{self.business_account_id}/media_publish"
            publish_params = {
                "creation_id": creation_id,
                "access_token": self.access_token,
            }
            publish_response = requests.post(publish_url, params=publish_params)
            return publish_response.json()

        return response.json()

    def get_insights(self, metric_type: str = "engagement") -> Dict:
        """Get Instagram insights and analytics"""
        url = f"{self.base_url}/{self.business_account_id}/insights"

        params = {
            "metric": metric_type,
            "period": "day",
            "access_token": self.access_token,
        }

        response = requests.get(url, params=params)
        return response.json()


class TikTokAPI:
    def __init__(self):
        self.client_key = os.getenv("TIKTOK_CLIENT_KEY") or ""
        self.client_secret = os.getenv("TIKTOK_CLIENT_SECRET") or ""
        self.access_token = os.getenv("TIKTOK_ACCESS_TOKEN") or ""
        self.base_url = "https://open-api.tiktok.com"

    def post_video(
        self, video_path: str, caption: str, hashtags: Optional[List[str]] = None
    ) -> Dict:
        """Post a video to TikTok"""
        url = f"{self.base_url}/share/video/upload/"

        # Upload video
        with open(video_path, "rb") as video_file:
            files = {"video": video_file}
            data = {"access_token": self.access_token, "caption": caption}

            if hashtags:
                data["hashtags"] = ",".join(hashtags)

            response = requests.post(url, files=files, data=data)
            return response.json()

    def get_user_info(self) -> Dict:
        """Get TikTok user information"""
        url = f"{self.base_url}/user/info/"

        params = {
            "access_token": self.access_token,
            "fields": "open_id,union_id,display_name,avatar_url,profile_deep_link",
        }

        response = requests.get(url, params=params)
        return response.json()

    def get_video_analytics(self, video_id: str) -> Dict:
        """Get analytics for a specific video"""
        url = f"{self.base_url}/video/query/"

        params = {
            "access_token": self.access_token,
            "item_id": video_id,
            "fields": "id,create_time,video_description,video_cover_image_url,like_count,comment_count,share_count",
        }

        response = requests.get(url, params=params)
        return response.json()


class YouTubeAPI:
    def __init__(self):
        self.api_key = os.getenv("YOUTUBE_API_KEY") or ""
        self.client_id = os.getenv("YOUTUBE_CLIENT_ID") or ""
        self.client_secret = os.getenv("YOUTUBE_CLIENT_SECRET") or ""
        self.refresh_token = os.getenv("YOUTUBE_REFRESH_TOKEN") or ""
        self.base_url = "https://www.googleapis.com/youtube/v3"

    def get_access_token(self) -> str:
        """Refresh access token using refresh token"""
        url = "https://oauth2.googleapis.com/token"

        data = {
            "client_id": self.client_id,
            "client_secret": self.client_secret,
            "refresh_token": self.refresh_token,
            "grant_type": "refresh_token",
        }

        response = requests.post(url, data=data)
        return response.json().get("access_token", "")

    def upload_video(
        self,
        file_path: str,
        title: str,
        description: str,
        tags: Optional[List[str]] = None,
    ) -> Dict:
        """Upload a video to YouTube"""
        access_token = self.get_access_token()

        # Step 1: Initiate upload
        upload_url = "https://www.googleapis.com/upload/youtube/v3/videos?uploadType=resumable&part=snippet,status"

        metadata = {
            "snippet": {
                "title": title,
                "description": description,
                "tags": tags or [],
                "categoryId": "22",  # People & Blogs
            },
            "status": {"privacyStatus": "public", "selfDeclaredMadeForKids": False},
        }

        headers = {
            "Authorization": f"Bearer {access_token}",
            "Content-Type": "application/json",
        }

        response = requests.post(upload_url, headers=headers, json=metadata)

        if response.status_code == 200:
            upload_url = response.headers["Location"]

            # Step 2: Upload actual video file
            with open(file_path, "rb") as video_file:
                video_headers = {
                    "Authorization": f"Bearer {access_token}",
                    "Content-Type": "video/*",
                }

                video_response = requests.put(
                    upload_url, headers=video_headers, data=video_file.read()
                )
                return video_response.json()

        return response.json()

    def schedule_video(
        self,
        file_path: str,
        title: str,
        description: str,
        publish_time: datetime,
        tags: Optional[List[str]] = None,
    ) -> Dict:
        """Upload and schedule a YouTube video"""
        access_token = self.get_access_token()

        upload_url = "https://www.googleapis.com/upload/youtube/v3/videos?uploadType=resumable&part=snippet,status"

        metadata = {
            "snippet": {
                "title": title,
                "description": description,
                "tags": tags or [],
                "categoryId": "22",
            },
            "status": {
                "privacyStatus": "private",
                "publishAt": publish_time.isoformat(),
                "selfDeclaredMadeForKids": False,
            },
        }

        headers = {
            "Authorization": f"Bearer {access_token}",
            "Content-Type": "application/json",
        }

        response = requests.post(upload_url, headers=headers, json=metadata)

        if response.status_code == 200:
            upload_url = response.headers["Location"]

            with open(file_path, "rb") as video_file:
                video_headers = {
                    "Authorization": f"Bearer {access_token}",
                    "Content-Type": "video/*",
                }

                video_response = requests.put(
                    upload_url, headers=video_headers, data=video_file.read()
                )
                return video_response.json()

        return response.json()

    def get_analytics(
        self,
        video_id: Optional[str] = None,
        start_date: Optional[str] = None,
        end_date: Optional[str] = None,
    ) -> Dict:
        """Get YouTube analytics data"""
        access_token = self.get_access_token()

        if video_id:
            url = f"{self.base_url}/videos"
            params = {"part": "statistics,snippet", "id": video_id, "key": self.api_key}
        else:
            url = f"{self.base_url}/reports"
            params = {
                "key": self.api_key,
                "startDate": start_date
                or (datetime.now() - timedelta(days=30)).strftime("%Y-%m-%d"),
                "endDate": end_date or datetime.now().strftime("%Y-%m-%d"),
                "metrics": "views,estimatedMinutesWatched,averageViewDuration,subscribersGained",
            }

        headers = {"Authorization": f"Bearer {access_token}"}

        response = requests.get(url, headers=headers, params=params)
        return response.json()


class LinkedInAPI:
    def __init__(self):
        self.client_id = os.getenv("LINKEDIN_CLIENT_ID") or ""
        self.client_secret = os.getenv("LINKEDIN_CLIENT_SECRET") or ""
        self.access_token = os.getenv("LINKEDIN_ACCESS_TOKEN") or ""
        self.base_url = "https://api.linkedin.com/v2"

    def post_text(self, content: str) -> Dict:
        """Post a text update to LinkedIn"""
        url = f"{self.base_url}/ugcPosts"

        # First register the post
        register_url = f"{self.base_url}/ugcPosts?action=create"

        headers = {
            "Authorization": f"Bearer {self.access_token}",
            "Content-Type": "application/json",
        }

        post_data = {
            "author": f"urn:li:person:{self.get_person_id()}",
            "lifecycleState": "PUBLISHED",
            "specificContent": {
                "com.linkedin.ugc.ShareContent": {
                    "shareCommentary": {"text": content},
                    "shareMediaCategory": "NONE",
                }
            },
            "visibility": {"com.linkedin.ugc.MemberNetworkVisibility": "PUBLIC"},
        }

        response = requests.post(register_url, headers=headers, json=post_data)
        return response.json()

    def post_image(self, content: str, image_path: str) -> Dict:
        """Post an image update to LinkedIn"""
        # Upload image first
        upload_url = f"{self.base_url}/images?action=upload"

        with open(image_path, "rb") as image_file:
            files = {"file": image_file}
            headers = {"Authorization": f"Bearer {self.access_token}"}

            upload_response = requests.post(upload_url, headers=headers, files=files)
            image_urn = upload_response.json().get("image")

        # Create post with image
        post_url = f"{self.base_url}/ugcPosts?action=create"

        headers = {
            "Authorization": f"Bearer {self.access_token}",
            "Content-Type": "application/json",
        }

        post_data = {
            "author": f"urn:li:person:{self.get_person_id()}",
            "lifecycleState": "PUBLISHED",
            "specificContent": {
                "com.linkedin.ugc.ShareContent": {
                    "shareCommentary": {"text": content},
                    "shareMediaCategory": "IMAGE",
                    "media": [
                        {
                            "status": "READY",
                            "description": {"text": "Image"},
                            "media": image_urn,
                            "title": {"text": "Post Image"},
                        }
                    ],
                }
            },
            "visibility": {"com.linkedin.ugc.MemberNetworkVisibility": "PUBLIC"},
        }

        response = requests.post(post_url, headers=headers, json=post_data)
        return response.json()

    def get_person_id(self) -> str:
        """Get LinkedIn person ID"""
        url = f"{self.base_url}/people/~:(id)"
        headers = {"Authorization": f"Bearer {self.access_token}"}

        response = requests.get(url, headers=headers)
        return response.json().get("id", "")


class SocialMediaManager:
    """Unified social media management class"""

    def __init__(self):
        self.twitter = TwitterAPI()
        self.instagram = InstagramAPI()
        self.tiktok = TikTokAPI()
        self.youtube = YouTubeAPI()
        self.linkedin = LinkedInAPI()

    def cross_post(
        self, content: str, platforms: List[str], media_path: Optional[str] = None
    ) -> Dict[str, Dict]:
        """Post content across multiple platforms"""
        results = {}

        if "twitter" in platforms:
            media_ids = []
            if media_path:
                upload_result = self.twitter.upload_media(media_path)
                media_ids.append(upload_result.get("media_id_string", ""))

            results["twitter"] = self.twitter.post_tweet(content, media_ids)

        if "instagram" in platforms and media_path:
            results["instagram"] = self.instagram.post_photo(media_path, content)

        if "tiktok" in platforms and media_path:
            results["tiktok"] = self.tiktok.post_video(media_path, content)

        if "linkedin" in platforms:
            if media_path:
                results["linkedin"] = self.linkedin.post_image(content, media_path)
            else:
                results["linkedin"] = self.linkedin.post_text(content)

        return results

    def schedule_cross_post(
        self,
        content: str,
        platforms: List[str],
        publish_time: datetime,
        media_path: Optional[str] = None,
    ) -> Dict[str, Dict]:
        """Schedule content across multiple platforms"""
        results = {}

        if "twitter" in platforms:
            media_ids = []
            if media_path:
                upload_result = self.twitter.upload_media(media_path)
                media_ids.append(upload_result.get("media_id_string", ""))

            results["twitter"] = self.twitter.schedule_tweet(
                content, publish_time, media_ids
            )

        if "youtube" in platforms and media_path:
            results["youtube"] = self.youtube.schedule_video(
                media_path, content[:100], content, publish_time
            )

        return results

    def get_analytics_summary(
        self,
        platforms: List[str],
        start_date: Optional[str] = None,
        end_date: Optional[str] = None,
    ) -> Dict:
        """Get analytics summary from multiple platforms"""
        summary = {}

        if "youtube" in platforms:
            summary["youtube"] = self.youtube.get_analytics(None, start_date, end_date)

        if "instagram" in platforms:
            summary["instagram"] = self.instagram.get_insights("engagement")

        # Add more platform analytics as needed

        return summary
