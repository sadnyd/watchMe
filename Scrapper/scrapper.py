from selenium import webdriver
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import time
import os

BRANDS = [
    'rolex', 'audemarspiguet', 'breitling', 'iwc', 'jaegerlecoultre',
    'omega', 'panerai', 'patekphilippe', 'cartier', 'gucci', 'seiko', 'movado', 'zenith'
]


options = webdriver.ChromeOptions()
#options.add_argument('--headless') 
browser = webdriver.Chrome(options=options)

os.makedirs("data", exist_ok=True)

for brand in BRANDS:
    urls = [
        f"http://chrono24.com/{brand}/index.htm",
        f"http://chrono24.com/{brand}/index-2.htm",
        f"http://chrono24.com/{brand}/index-3.htm",
        f"http://chrono24.com/{brand}/index-4.htm",
        f"http://chrono24.com/{brand}/index-5.htm"
    ]

    for url in urls:
        # Navigate to the page
        browser.get(url)
        time.sleep(2)  # Wait for page to load

        # Scroll down to load more content
        for _ in range(15):
            browser.execute_script("window.scrollBy(0, 500)")
            time.sleep(2)

        soup = BeautifulSoup(browser.page_source, 'html.parser')

        # Find all article divs
        article_divs = soup.select(".article-item-container")
        data_file = f"data/{brand}.txt"

        with open(data_file, "a+") as f:
            for article_div in article_divs:
                # Find image URL
                image_div = article_div.select_one(".article-image-container .content img")
                if image_div is None:
                    continue

                image_url = image_div.get('src')
                if not image_url:
                    continue

                # Find price
                price_div = article_div.select_one(".article-price strong")
                if price_div is None:
                    continue

                price_text = price_div.get_text()
                price = ''.join(filter(str.isdigit, price_text))  # Extract numeric value from price

                if not price:
                    continue


                f.write(f"{image_url},{price}\n")


browser.quit()

