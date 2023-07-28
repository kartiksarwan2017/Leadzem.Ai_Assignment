import requests
from bs4 import BeautifulSoup
import csv
import time

MAX_RETRIES = 3
RETRY_DELAY = 5  # Seconds between retries

# ... (rest of the functions remain unchanged) ...

def retry_request(url):
    retries = 0
    while retries < MAX_RETRIES:
        try:
            response = requests.get(url)
            response.raise_for_status()  # Check for successful response
            return response
        except requests.exceptions.RequestException as e:
            print(f"Failed to retrieve data from {url}. Error: {e}")
            retries += 1
            time.sleep(RETRY_DELAY)

    return None

def scrape_product_listing_page(url):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"
    }

    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()  # Check for successful response
    except requests.exceptions.RequestException as e:
        print(f"Failed to retrieve data from {url}. Error: {e}")
        return []

    soup = BeautifulSoup(response.text, "html.parser")
    products = []

    product_cards = soup.find_all("div", class_="s-include-content-margin")

    for card in product_cards:
        product_url = card.find("a", class_="a-link-normal")
        if product_url:
            product_url = f"https://www.amazon.in{product_url['href']}"
        else:
            continue

        product_name = card.find("span", class_="a-size-medium")
        if product_name:
            product_name = product_name.text.strip()
        else:
            continue

        product_price = card.find("span", class_="a-offscreen")
        if product_price:
            product_price = product_price.text.strip()
        else:
            continue

        product_rating = card.find("span", class_="a-icon-alt")
        if product_rating:
            product_rating = float(product_rating.text.split()[0])
        else:
            product_rating = None

        product_reviews = card.find("span", {"data-component-type": "s-product-rating"})
        if product_reviews:
            product_reviews = int(product_reviews.text.replace(",", ""))
        else:
            product_reviews = 0

        products.append({
            "URL": product_url,
            "Name": product_name,
            "Price": product_price,
            "Rating": product_rating,
            "Number of Reviews": product_reviews
        })

    return products

def scrape_product_details_page(url):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"
    }

    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()  # Check for successful response
    except requests.exceptions.RequestException as e:
        print(f"Failed to retrieve data from {url}. Error: {e}")
        return {}

    soup = BeautifulSoup(response.text, "html.parser")

    description = soup.find("div", {"id": "productDescription"})
    description_text = description.text.strip() if description else ""

    asin_tag = soup.find("th", text="ASIN")
    asin = asin_tag.find_next("td").text.strip() if asin_tag else ""

    product_description = soup.find("meta", {"name": "description"})["content"]

    manufacturer_tag = soup.find("th", text="Manufacturer")
    manufacturer = manufacturer_tag.find_next("td").text.strip() if manufacturer_tag else ""

    return {
        "Description": description_text,
        "ASIN": asin,
        "Product Description": product_description,
        "Manufacturer": manufacturer
    }

def scrape_multiple_pages(base_url, num_pages=20):
    all_products = []
    for page_num in range(1, num_pages + 1):
        url = f"{base_url}&page={page_num}"
        products = scrape_product_listing_page(url)
        all_products.extend(products)
        time.sleep(2)  # Adding a delay of 2 seconds to avoid rate-limiting

    # Fetch additional details for each product
    for product in all_products:
        url = product["URL"]
        additional_details = scrape_product_details_page(url)
        product.update(additional_details)

    return all_products

def export_to_csv(data, filename):
    keys = ["URL", "Name", "Price", "Rating", "Number of Reviews", "Description", "ASIN", "Product Description", "Manufacturer"]
    with open(filename, "w", newline="", encoding="utf-8") as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=keys)
        writer.writeheader()
        writer.writerows(data)

if __name__ == "__main__":
    base_url = "https://www.amazon.in/s?k=bags&crid=2M096C61O4MLT&qid=1653308124&sprefix=ba%2Caps%2C283&ref=sr_pg_"
    num_pages = 20

    scraped_data = scrape_multiple_pages(base_url, num_pages)

    # Export data to CSV
    export_to_csv(scraped_data, "amazon_bags_data.csv")