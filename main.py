import json
import datetime
from openai import get_search_query
from scraping import get_youtube_video_links, get_alibaba_video_links
from utils import match_product_using_frames

# Optimized get_matched_urls function
def get_matched_urls(input_json, match_urls):
    if isinstance(input_json, str):
        input_json = json.loads(input_json)

    input_img_url = input_json['product'].get('image_url')
    title = input_json['product'].get('title')
    description = input_json['product'].get('description')

    # Generate search query only once
    search_query = get_search_query(title=title, description=description)

    # Fetch YouTube and Alibaba video links concurrently if possible
    yt_dn_urls = get_youtube_video_links(search_query)
    alibaba_dn_urls = get_alibaba_video_links(search_query)

    # Match products using frames from both sources
    match_products = match_product_using_frames(input_img_url, yt_dn_urls + alibaba_dn_urls, match_urls)

    # Output the matched URLs for debug purposes

    return match_urls

if __name__ == "__main__":
    st = datetime.datetime.now()

    input_json = {
        "website_url": "https://tophandystore.com/products/rojeco-automatic-cat-toys-interactive-smart-teasing-pet-led-laser-indoor-cat-toy-accessories-handheld-electronic-cat-toy-for-dog?srsltid=AfmBOoq4TcK4gkyp5Z-Lh8aVEW_7vZnMBZs1PXbfe5kbYzoQP3ZnC054",
        "product": {
            "title": "LED Laser Cat Toy",
            "description": "Brand Name: ROJECO, Toys Type: Laser Toys, Is Smart Device: YES, Origin: Mainland China, CN: Guangdong, Material: Plastic, Type: cats, Product: Little Devil Automatic LED laser Cat Toys, Color: White, Size: 175X65mm, 3 Gears Mode: I Gear / II Gear / M Gear (Handheld Mode), Power Supply: DC Power & 4*AA Battery Supply (Not Include), Material: Environmental Friendly ABS Material, Suitable For: All Cats / Dogs, Feature1: cat accessories / cat toy / Toys for cats / cat toys / cat toys interactive / Interactive cat toy, Feature2: jouer pour chat / indoor cat toy / cat laser / Interactive toys / laser chat / cat toys for cat, Feature3: Interactive dog toy / cat interactive toy / automatic cat toy / laser for cat / laser pour chat, Feature4: Electronic toys / Cat auto toy / Interactive toys for cats / interactive cat toys, Feature5: cat toy automatic / cat toy interactive / interactive toy for cat / interactive moving cat toy, Friendly Tips: It needs 4*AA battery (Not Include). Please kindly note. thanks",
            "image_url": "https://tophandystore.com/cdn/shop/files/S5655d1a2031e49d882d2e60b0deb3cfdR.webp?v=1700746011"
        }
    }

    match_urls = get_matched_urls(input_json, [])
    print(match_urls)

    end = datetime.datetime.now()
    print(f"Start time: {st}, End time: {end}")
    print(f"Total time: {end - st}")
