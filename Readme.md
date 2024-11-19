# **Product Video Matching Script**

This script retrieves product-related videos from YouTube and Alibaba, compares their frames with a product image, and outputs URLs of matching videos. It uses AI-based embedding techniques and OpenAI-powered prompts for product matching.

---

## **Features**
- **Product Video Retrieval**: Fetches video links from YouTube and Alibaba based on product title and description.
- **Frame Extraction**: Extracts frames from videos at evenly spaced intervals for comparison.
- **Image-Video Matching**: Matches a product image with video frames using AI-based embeddings.
- **Concurrent Processing**: Efficiently handles multiple video links using multithreading for faster execution.
- **Output Matching URLs**: Returns a list of video URLs that match the product image.

---

## **Installation**

1. **Clone the Repository**
   ```bash
   git clone <repository_url>
   cd <repository_folder>

2. **Install Dependencies Install the required Python packages**
   ```bash
   pip install -r requirements.txt

# Product Video Matching Script

## **Usage**

### **Script Execution**
1. **Modify the `input_json` with your product details**:
    - `title`: Product title.
    - `description`: Product description.
    - `image_url`: URL to the product image.

2. **Run the script**:
    ```bash
    python main.py
    ```

3. **The script outputs**:
    - Matched video URLs in the console.
    - Total processing time for debugging and performance analysis.

---
# **Modules**

### **`get_matched_urls`**
- **Description**: Main function for video retrieval and matching.
- **Features**:
  - Combines video links from YouTube and Alibaba.
  - Matches product images with video frames.

---

### **`get_youtube_video_links`**
- **Description**: Fetches video links from YouTube based on a generated search query.

---

### **`get_alibaba_video_links`**
- **Description**: Retrieves video links from Alibaba product pages.

---

### **`match_product_using_frames`**
- **Description**: Compares product images with video frames to find matches.

---

### **`get_search_query`**
- **Description**: Generates a search query using the product title and description.

---

## **Performance Considerations**

### **Concurrency**
- Uses `ThreadPoolExecutor` to parallelize video processing.

### **Efficiency**
- Processes only 10 frames per video for faster comparison.

---

## **Output**
- A list of matched video URLs is printed in the console.

---

### **Example Output**
```
['https://www.youtube.com/watch?v=abc123', 'https://www.alibaba.com/video_link'].
```
---

### **Example Input**
```json
{
    "website_url": "https://tophandystore.com/products/rojeco-automatic-cat-toys",
    "product": {
        "title": "LED Laser Cat Toy",
        "description": "Brand Name: ROJECO, Toys Type: Laser Toys, Is Smart Device: YES, Origin: Mainland China...",
        "image_url": "https://tophandystore.com/cdn/shop/files/S5655d1a2031e49d882d2e60b0deb3cfdR.webp?v=1700746011"
    }
}



