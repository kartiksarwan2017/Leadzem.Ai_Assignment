# Amazon Bags Data Scraper

The "Amazon Bags Data Scraper" is a Python script that allows you to scrape product data from Amazon's bags category. The script scrapes product listings from multiple pages, retrieves additional details for each product, and exports the collected data to a CSV file.

## Requirements

Before running the script, ensure you have the following requirements installed:

- Python 3.x
- requests library
- BeautifulSoup4 library
- csv library

You can install the required libraries using `pip`:
pip install requests beautifulsoup4


## Usage

1. Clone or download this repository to your local machine.

2. Open a terminal or command prompt and navigate to the project directory.

3. Run the script:



The script will start scraping product data from Amazon. It will retrieve information such as product URLs, names, prices, ratings, number of reviews, descriptions, ASINs, product descriptions, and manufacturers.

The data will be saved in a CSV file named `amazon_bags_data.csv` in the same directory as the script.

## Notes

- The script includes a delay of 2 seconds between each page request to avoid rate-limiting issues with the Amazon website.

- In case of temporary server errors (e.g., 503 Service Unavailable), the script uses a retry mechanism to attempt the request again after a short delay.

- Web scraping may violate the website's terms of service. Ensure that you are allowed to access and use the data you are scraping from Amazon.

- Always review Amazon's terms of service and robots.txt file before scraping their website.


Happy scraping! 🚀
