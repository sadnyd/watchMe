import csv
import requests
import os

BRANDS = [
    'rolex', 'audemarspiguet', 'breitling', 'iwc', 'jaegerlecoultre',
    'omega', 'panerai', 'patekphilippe', 'cartier', 'gucci',
    'seiko', 'movado', 'zenith'
]


os.makedirs("images", exist_ok=True)

for brand in BRANDS:
    with open(f"data/{brand}.txt", newline='') as csvfile:
        data = csv.reader(csvfile)

        for index, item in enumerate(data):
            image_url = item[0]
            image_name = item[1]

            try:
                response = requests.get(image_url, stream=True)
                response.raise_for_status()  # Check if request was successful

        
                with open(f"images/{brand}-{index+1}-{image_name}.jpg", "wb") as file:
                    file.write(response.content)

                print(f"Downloaded {brand}-{index+1}-{image_name}.jpg")

            except requests.RequestException as e:
                print(f"Error downloading {image_url}: {e}")
