import cv2
from PIL import Image
import time
import requests
import os
from moviepy.editor import VideoFileClip
import json
from urllib.parse import urlencode

class InstaUpload:
    def __init__(self, cookies):
        self.cookies = cookies
    def wait(self, duration, message):
        for remaining in range(duration, 0, -1):
            minutes, seconds = divmod(remaining, 60)
            print(f"{message} {minutes:02d}:{seconds:02d}", end='\r')
            time.sleep(1)

    def saveThumbnail(self, video_path):
        print("Extracting thumbnail...")
        # Open the video file
        cap = cv2.VideoCapture(video_path)
        # Read the first frame
        ret, frame = cap.read()
        # Check if the frame was successfully read
        if ret:
            # Convert the frame from BGR (OpenCV format) to RGB (Pillow format)
            frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            # Convert to a PIL Image
            image = Image.fromarray(frame_rgb)
            # Save the image as JPEG
            image.save("thumbnail.jpg", "JPEG")
            print("Thumbnail extracted successfully")
        else:
            print("Failed to read the video frame")
        # Release the video capture object
        cap.release()

    def getVideoProps(self, video_path):
        clip = VideoFileClip(video_path)
        duration_ms = int(clip.duration * 1000)  # Duration in milliseconds
        width, height = clip.size  # Width and height in pixels
        clip.close()
        return duration_ms, width, height
    def getCaption(self):
        captions = [
            "The Tesla Cybertruck is an all-electric, battery-powered light-duty truck unveiled by Tesla, Inc.\n\nHere’s a comprehensive overview of its key features and specifications:\n\nTesla Cybertruck Overview\n\nDesign and Structure\n\n• Exterior: The Cybertruck has a distinctive, angular, stainless steel exoskeleton design for durability and passenger protection. It features ultra-hard 30X cold-rolled stainless steel and armored glass.\n• Dimensions: Approximately 231.7 inches long, 79.8 inches wide, and 75 inches tall, with a 6.5-foot cargo bed.\n\nPerformance and Variants\n\n• Single Motor RWD:\n◦ 0-60 mph: ~6.5 seconds\n◦ Range: ~250 miles\n◦ Towing Capacity: 7,500 pounds\n• Dual Motor AWD:\n◦ 0-60 mph: ~4.5 seconds\n◦ Range: ~300 miles\n◦ Towing Capacity: 10,000 pounds\n• Tri-Motor AWD:\n◦ 0-60 mph: ~2.9 seconds\n◦ Range: ~500 miles\n◦ Towing Capacity: 14,000 pounds"
        ]
        return captions[0]


    def uploadVideo(self, video_path, timestamp):
        print("Starting Video upload...")
        duration_ms, width, height = self.getVideoProps(video_path)
        file_size = os.path.getsize(video_path)
        x_instagram_rupload_params = {
            "client-passthrough": "1",
            "is_clips_video": "1",  # Set to "0" if it's not a Clips video
            "is_sidecar": "0",  # Set to "1" if this is part of a sidecar
            "media_type": 2,  # 2 represents a video
            "for_album": False,  # Set to True if this video is part of an album
            "video_format": "",  # Specify the video format, e.g., "mp4"
            "upload_id": timestamp,
            "upload_media_duration_ms": duration_ms,
            "upload_media_height": height,
            "upload_media_width": width,
            "video_transform": None,  # Set transformation parameters if applicable
            "video_edit_params": {
                "crop_height": height,  # Height after cropping
                "crop_width": width,  # Width after cropping
                "crop_x1": 0,  # X coordinate of the crop start
                "crop_y1": 0,  # Y coordinate of the crop start
                "mute": False,  # Whether the video is muted
                "trim_end":
                duration_ms / 1000.0,  # End time in seconds for trimming
                "trim_start": 0  # Start time in seconds for trimming
            }
        }
        headers = {
            'accept': '*/*',
            'accept-language': 'en-US,en;q=0.9',
            'offset': '0',
            'origin': 'https://www.instagram.com',
            'priority': 'u=1, i',
            'referer': 'https://www.instagram.com/',
            'sec-ch-ua':
            '"Chromium";v="128", "Not;A=Brand";v="24", "Google Chrome";v="128"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'same-site',
            'user-agent':
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36',
            'x-asbd-id': '129477',
            'x-entity-length': str(file_size),
            'x-entity-name': 'fb_uploader_' + timestamp,
            'x-ig-app-id': '936619743392459',
            'x-instagram-rupload-params': json.dumps(x_instagram_rupload_params),
            'content-type': 'application/x-www-form-urlencoded',
        }
        with open(video_path, 'rb') as f:
            data = f.read()
            response = requests.post(
                f'https://i.instagram.com/rupload_igvideo/fb_uploader_{timestamp}',
                cookies=self.cookies,
                headers=headers,
                data=data,
            )
        if response.status_code == 200:
            print("Video uploaded successfully!")
            return True
        else:
            print(response)
            print(response.text)
            return False
    def uploadPhoto(self, video_path, timestamp):
        self.saveThumbnail(video_path)
        print("Starting Thumbnail upload...")
        duration_ms, width, height = self.getVideoProps(video_path)
        x_instagram_rupload_params = {
            "client-passthrough": "1",
            "is_clips_video": "1",  # Set to "0" if it's not a Clips video
            "is_sidecar": "0",  # Set to "1" if this is part of a sidecar
            "media_type": 2,  # 2 represents a video
            "for_album": False,  # Set to True if this video is part of an album
            "video_format": "",  # Specify the video format, e.g., "mp4"
            "upload_id": timestamp,
            "upload_media_duration_ms": duration_ms,
            "upload_media_height": height,
            "upload_media_width": width,
            "video_transform": None,  # Set transformation parameters if applicable
            "video_edit_params": {
                "crop_height": height,  # Height after cropping
                "crop_width": width,  # Width after cropping
                "crop_x1": 0,  # X coordinate of the crop start
                "crop_y1": 0,  # Y coordinate of the crop start
                "mute": False,  # Whether the video is muted
                "trim_end":
                duration_ms / 1000.0,  # End time in seconds for trimming
                "trim_start": 0  # Start time in seconds for trimming
            }
        }
        file_size = os.path.getsize('thumbnail.jpg')
        headers = {
            'accept': '*/*',
            'accept-language': 'en-US,en;q=0.9',
            'offset': '0',
            'origin': 'https://www.instagram.com',
            'priority': 'u=1, i',
            'referer': 'https://www.instagram.com/',
            'sec-ch-ua':
            '"Chromium";v="128", "Not;A=Brand";v="24", "Google Chrome";v="128"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'same-site',
            'user-agent':
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36',
            'x-asbd-id': '129477',
            'x-entity-length': str(file_size),
            'x-entity-name': 'fb_uploader_' + timestamp,
            'x-ig-app-id': '936619743392459',
            'x-instagram-rupload-params': json.dumps(x_instagram_rupload_params),
            'content-type': 'application/x-www-form-urlencoded',
        }
        with open('thumbnail.jpg', 'rb') as f:
            data = f.read()
            response = requests.post(
                f'https://i.instagram.com/rupload_igphoto/fb_uploader_{timestamp}',
                cookies=self.cookies,
                headers=headers,
                data=data,
            )
        if response.status_code == 200:
            print("Thumbnail uploaded successfully")
            return response.json()['upload_id']
        else:
            print(response.text)
            print(response.status_code)
            return False
    
    def finalizeUpload(self, upload_id):
        print("Posting video...")
        caption = self.getCaption()
        headers = {
            'accept': '*/*',
            'accept-language': 'en-US,en;q=0.9',
            'content-type': 'application/x-www-form-urlencoded',
            'origin': 'https://www.instagram.com',
            'priority': 'u=1, i',
            'referer': 'https://www.instagram.com/funi.ting',
            'sec-ch-prefers-color-scheme': 'dark',
            'sec-ch-ua':
            '"Chromium";v="128", "Not;A=Brand";v="24", "Google Chrome";v="128"',
            'sec-ch-ua-full-version-list':
            '"Chromium";v="128.0.6613.114", "Not;A=Brand";v="24.0.0.0", "Google Chrome";v="128.0.6613.114"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-model': '""',
            'sec-ch-ua-platform': '"Windows"',
            'sec-ch-ua-platform-version': '"10.0.0"',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'same-origin',
            'user-agent':
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36',
            'x-asbd-id': '129477',
            'x-csrftoken': self.cookies['csrftoken'],
            'x-ig-app-id': '936619743392459',
            'x-requested-with': 'XMLHttpRequest',
        }
        data = {
            'archive_only': 'false',
            'caption': caption,
            'clips_share_preview_to_feed': '1',
            'disable_comments': '0',
            'disable_oa_reuse': 'false',
            'igtv_share_preview_to_feed': '1',
            'is_meta_only_post': '0',
            'is_unified_video': '1',
            'like_and_view_counts_disabled': '0',
            'share_to_threads': 'false',
            'source_type': 'library',
            'upload_id': upload_id,
            'video_subtitles_enabled': '0'
        }
        data = urlencode(data)
        response = requests.post('https://www.instagram.com/api/v1/media/configure_to_clips/',
                                    cookies=self.cookies,
                                    headers=headers,
                                    data=data)

        if response.status_code == 200:
            print("Posted successfully")
            return True
        else:
            print('error finalizing upload with status ' + response.json()['status'])
            return False

    def startPosting(self, videos_path, wait_time, stash_path=None):

        while True:
            videos = os.listdir(videos_path)
            videos = [video for video in videos if (video.endswith(".mp4") and "_instagram" not in video)]
            parent_path = videos_path
            if len(videos) == 0:
                if not stash_path:
                    print("No videos to upload. stoping script.")
                    break
                print("No videos to upload. Moving to stash...")
                videos = os.listdir(stash_path)
                videos = [video for video in videos if (video.endswith(".mp4") and "_instagram" not in video)]
                parent_path = stash_path
                if len(videos) == 0:
                    print("No videos in stash. Stoping script.")
                    break
                print(f"Got {len(videos)} from stash.")

            print(f"Starting upload batch for {len(videos)} videos this should take about {((wait_time + 0.5) * len(videos))} minutes")
            for video in videos:
                try:
                    print(f"Posting: {video}")
                    timestamp = str(int(time.time()))
                    video_path = os.path.join(parent_path, video)
                    video_upload_res = self.uploadVideo(video_path, timestamp)
                    if not video_upload_res:
                        os.rename(video_path, os.path.join(parent_path, "error_instagram_" + video))
                        print("Error uploading video: " + video)
                        continue
                    upload_id = self.uploadPhoto(video_path, timestamp)
                    if not upload_id:
                        os.rename(video_path, os.path.join(parent_path, "error_instagram_" + video))
                        print("Error uploading thumbnail for video: " + video)
                        continue
                    upload_finalize_res = self.finalizeUpload(upload_id)
                    if not upload_finalize_res:
                        os.rename(video_path, os.path.join(parent_path, "error_instagram_" + video))
                        print("error posting video: " + video)
                        continue
                    os.rename(video_path, os.path.join(parent_path, "uploaded_instagram_" + video))

                    self.wait((60 * wait_time), "Next video in :")
                except Exception as e:
                    print("Error while uploading video: ", video)
                    os.rename(video_path, os.path.join(parent_path, "error_instagram_" + video))

    
