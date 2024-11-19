import requests
from bs4 import BeautifulSoup
import json
import base64
import yt_dlp
import re
from concurrent.futures import ThreadPoolExecutor, as_completed


def generate_yt_video_download_link(video_id):
    video_link = f'https://www.youtube.com/watch?v={str(video_id)}'
    ydl_opts = {
        'format': 'best',
        'quiet': True,
    }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info_dict = ydl.extract_info(video_link, download=False)
        # duration = info_dict.get('duration', 0)
        video_url = info_dict.get('url', None)
    return video_url


def generate_video_download_link(vd, video_dn_urls):
    """
    Generates the download link for a YouTube video and appends it to the list if successful.

    Args:
        vd (str): The video code (e.g., video ID).
        video_dn_urls (list): List to append successful download URLs.

    Returns:
        None
    """
    try:
        vd_url = generate_yt_video_download_link(vd)
        if vd_url:
            video_dn_urls.append(vd_url)
    except Exception as e:
        print(f"Error generating download link for video {vd}: {e}")


def generate_video_links_concurrently(video_codes, max_workers=5):
    """
    Generates download links for a list of video codes using concurrency.

    Args:
        video_codes (list): List of video codes to process.
        max_workers (int): Maximum number of threads for concurrent processing.

    Returns:
        list: List of video download URLs.
    """
    video_dn_urls = []

    # Use ThreadPoolExecutor for concurrent processing
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        # Submit tasks for all video codes
        futures = [executor.submit(generate_video_download_link, vd, video_dn_urls) for vd in video_codes]

        # Wait for all futures to complete
        for future in as_completed(futures):
            try:
                future.result()  # This will raise exceptions if any occurred in the threads
            except Exception as e:
                print(f"Error in concurrent processing: {e}")

    return video_dn_urls




def get_youtube_video_links(query):
    # Format the query for YouTube search URL
    query = query.replace(' ', '+')
    url = f"https://www.youtube.com/results?search_query={query}"

    # Send GET request to YouTube
    try:
        response = requests.get(url)
        response.raise_for_status()  # Raise an error for bad responses
    except requests.RequestException as e:
        print(f"Failed to retrieve search results: {e}")
        return None

    # Parse the response content
    soup = BeautifulSoup(response.content, 'html.parser')

    # Extract JSON data from the script tags
    json_data = None
    for script in soup.find_all('script'):
        if 'ytInitialData' in script.text:
            try:
                # Extract JSON from the script text
                json_data = script.text.strip().replace('var ytInitialData = ', '').rstrip(';')
                json_data = json.loads(json_data)
                break
            except json.JSONDecodeError:
                print("Error decoding YouTube JSON data")
                return None

    if not json_data:
        print("No YouTube JSON data found")
        return None

    # Extract video IDs from the parsed JSON data
    try:
        video_list = json_data['contents']['twoColumnSearchResultsRenderer']['primaryContents']\
            ['sectionListRenderer']['contents'][0]['itemSectionRenderer']['contents']

        video_codes = [
            item['videoRenderer']['videoId']
            for item in video_list if 'videoRenderer' in item
        ]

        video_dn_urls = []
        # for vd in video_codes:
        #     try:
        #         vd_url = generate_yt_video_download_link(vd)
        #         if vd_url:
        #             video_dn_urls.append(vd_url)
        #     except Exception as e:
        #         print(f"Error generating download link for video {vd}: {e}")
        video_dn_urls = generate_video_links_concurrently(video_codes, max_workers=5)

        return video_dn_urls

    except KeyError:
        print("Error extracting video data from YouTube response")
        return None


def get_base64_from_imagelink(image_link):
    response = requests.get(image_link)
    if response.status_code == 200:
        return base64.b64encode(response.content).decode('utf-8')
    else:
        raise Exception(f"Failed to download image from {image_link}")
        return None


def get_alibaba_video_links(keyword):
    video_links = []
    headers = {
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
        'accept-language': 'en-US,en;q=0.9',
        'priority': 'u=0, i',
        'referer': 'https://www.alibaba.com/trade/search?spm=a2700.galleryofferlist.the-new-header_fy23_pc_search_bar.keydown__Enter&tab=all&SearchText=ROJECO+LED+Laser+Cat+Toy+interactive+automatic+toy',
        'sec-ch-ua': '"Google Chrome";v="129", "Not=A?Brand";v="8", "Chromium";v="129"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'document',
        'sec-fetch-mode': 'navigate',
        'sec-fetch-site': 'same-origin',
        'sec-fetch-user': '?1',
        'upgrade-insecure-requests': '1',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36',
    }

    params = {
        'spm': 'a2700.galleryofferlist.the-new-header_fy23_pc_search_bar.searchButton',
        'tab': 'all',
        'SearchText': f'{keyword}',
    }

    response = requests.get('https://www.alibaba.com/trade/search', params=params, headers=headers)
    soup = BeautifulSoup(response.content, 'lxml')
    js = soup.find_all('script')
    for jsd in js:
        if 'pc_similar_sse' in jsd.text:
            r_data = jsd.text.replace('window.__page__data_sse10._offer_list = ', '')
            lst = json.loads(r_data)
            break
    products = lst['offerResultData']['offers']
    pdp_links = [pdp['productUrl'] for pdp in products]

    for pdp in pdp_links:
        try:
            pdp = pdp.replace('//', 'https://')
            response = requests.get(pdp)
            pdp_soup = BeautifulSoup(response.text, 'lxml')
            fjs = pdp_soup.find_all('script')
            for pdpjs in fjs:
                if 'icbuPcDetailAll' in pdpjs.text:
                    pattern = r"(?<=window.detailData =)(.*?)(?=}};)"

                    matches = re.findall(pattern, pdpjs.text)[0]
                    if matches:
                        break
            matches = matches + "}}"
            pdp_data = json.loads(matches)
            try:
                pdp_js_data = pdp_data['globalData']['product']['mediaItems'][0]['videoUrl']
                if pdp_js_data.get('hd'):
                    v_link = pdp_js_data.get('hd').get('videoUrl', '')
                else:
                    v_link = pdp_js_data.get('sd').get('videoUrl', '')

                video_links.append(v_link)
            except:
                pass
        except:
            pass
    return video_links
