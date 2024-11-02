import csv
import requests
import os

BRANDS = [
    'rolex', 'audemarspiguet', 'breitling', 'iwc', 'jaegerlecoultre',
    'omega', 'panerai', 'patekphilippe', 'cartier', 'gucci',
    'seiko', 'movado', 'zenith'
]

# Headers to mimic a browser request
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8",
    "Accept-Language": "en-US,en;q=0.5",
    "Connection": "keep-alive"
}

session = requests.Session()
session.headers.update(headers)

# Ensure the images directory exists
os.makedirs("images", exist_ok=True)

for brand in BRANDS:
    with open(f"data/{brand}.txt", newline='') as csvfile:
        data = csv.reader(csvfile)

        for index, item in enumerate(data):
            image_url = item[0]
            image_name = item[1]

            try:
                # Send request with headers
                response = requests.get(image_url, headers=headers, stream=True)
                response.raise_for_status()  # Check if request was successful

                # Write the image to a file
                with open(f"images/{brand}-{index+1}-{image_name}.jpg", "wb") as file:
                    file.write(response.content)

                print(f"Downloaded {brand}-{index+1}-{image_name}.jpg")
                break

            except requests.RequestException as e:
                print(f"Error downloading {image_url}: {e}")
                break
