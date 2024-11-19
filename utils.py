from concurrent.futures import ThreadPoolExecutor
import cv2
import requests
import base64
from prompts import GENERATE_VIDEO_SUMMARY_PROMPT, GENERATE_IMAGE_SUMMARY_PROMPT, GENERATE_IMAGE_VIDEO_COMPARISION_PROMPT
from openai import generate_content, get_text_embedding
from scraping import get_base64_from_imagelink
import numpy as np


def download_image(image_url):
    response = requests.get(image_url)
    if response.status_code == 200:
        image_array = np.asarray(bytearray(response.content), dtype=np.uint8)
        img = cv2.imdecode(image_array, cv2.IMREAD_COLOR)
        return img
    else:
        print(f"Error downloading image: {response.status_code}")
        return None

def extract_frames(vd_url):
    frames = []
    cap = cv2.VideoCapture(vd_url)

    # Get total frame count
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))

    if total_frames == 0:
        print("Error: Unable to get total frame count from video.")
        return frames

    # Calculate frame positions for 10% intervals
    frame_intervals = [int(total_frames * (i / 15)) for i in range(1, 11)]  # 10%, 20%, ..., 100%

    for frame_pos in frame_intervals:
        cap.set(cv2.CAP_PROP_POS_FRAMES, frame_pos)  # Move to the specific frame position
        ret, frame = cap.read()

        if not ret:
            print(f"Error: Unable to read frame at position {frame_pos}")
            break

        frames.append(frame)  # Store the extracted frame

    cap.release()
    return frames


def frames_to_base64(frames):
    try:
        return [
            base64.b64encode(cv2.imencode(".jpg", cv2.cvtColor(frame, cv2.COLOR_RGB2BGR))[1]).decode("utf-8")
            for frame in frames
        ]
    except Exception as e:
        print(f"Error in frames_to_base64: {str(e)}")
        return []


def calculate_similarity(embedding1, embedding2):
    return np.dot(embedding1, embedding2) / (np.linalg.norm(embedding1) * np.linalg.norm(embedding2))

def match_product_using_summary(input_img_url, yt_dn_urls):
    m_img_base64 = [get_base64_from_imagelink(input_img_url)]
    messages = GENERATE_IMAGE_SUMMARY_PROMPT
    m_img_summary = generate_content(messages, m_img_base64)
    print(f"Image Summary : {m_img_summary}")
    embedding1 = get_text_embedding(m_img_summary)
    for vd_url in yt_dn_urls:
        frames = extract_frames(vd_url)
        base64_frames = frames_to_base64(frames)
        messages = GENERATE_VIDEO_SUMMARY_PROMPT
        vd_summaries = generate_content(messages, base64_frames)
        print(f"Video Summary : {vd_summaries}")
        for vd_summary in vd_summaries:
            embedding2 = get_text_embedding(vd_summary)
            similarity_score = calculate_similarity(embedding1, embedding2)
            print(similarity_score)


# def match_product_using_frames(image_url, vd_urls, match_urls):
#     base64_image = get_base64_from_imagelink(image_link=image_url)
#     for vd_url in vd_urls:
#         frames = extract_frames(vd_url)
#         base64_frames = frames_to_base64(frames)
#         message = GENERATE_IMAGE_VIDEO_COMPARISION_PROMPT
#         frames = [base64_image] + base64_frames
#         match_prduct = generate_content(message, frames)
#         if match_prduct == 'Yes':
#             print(match_prduct)
#             match_urls.append(vd_url)
#         else:
#             print("No")
#
#     return match_urls


def process_video(vd_url, base64_image):
    try:
        frames = extract_frames(vd_url)
        base64_frames = frames_to_base64(frames)
        frames_to_compare = [base64_image] + base64_frames
        message = GENERATE_IMAGE_VIDEO_COMPARISION_PROMPT
        return vd_url if generate_content(message, frames_to_compare) == 'Yes' else None
    except Exception as e:
        print(f"Error processing video {vd_url}: {e}")
        return None

def match_product_using_frames(image_url, vd_urls, match_urls):
    base64_image = get_base64_from_imagelink(image_link=image_url)
    with ThreadPoolExecutor(max_workers=5) as executor:
        results = executor.map(lambda url: process_video(url, base64_image), vd_urls)
    match_urls.extend(filter(None, results))
    return  match_urls