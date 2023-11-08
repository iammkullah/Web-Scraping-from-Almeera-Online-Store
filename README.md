
"""
Created on Wed Nov  8 06:05:46 2023

@author: Muhammad Kaleem Ullah
"""

# Project: Almeera Online Store Web Scraping

## Overview

This project focuses on scraping data from the Almeera Online Store. The data includes multi-level category and product details. The extracted data is then organized and saved in a structured JSON format.

## Libraries Used

- `requests`: Used for sending HTTP requests to the website.
- `BeautifulSoup (bs4)`: Used for parsing HTML content and extracting data from it.
- `json`: Used for working with JSON data.

## Project Structure

The project consists of the following components:

1. **Code File** (`Aleemra_Scraping_Using_Request.py`):
   - This Python script contains the code for scraping data from the Almeera Online Store. It utilizes the `requests` library to send HTTP requests, and `BeautifulSoup` for parsing HTML content.

2. **Output Data File** (`output.json`):
   - This JSON file contains the structured data extracted from the website. It includes information about categories, subcategories, and products.

3. **Images Folders** (`category_images/`, `sub_category_images/`, `product_images/`):
   - These folders contain the downloaded images related to categories, subcategories, and products.

## How to Run the Script

1. Ensure you have Python installed on your system.
2. Install the required libraries using the following command:

```
pip install requests beautifulsoup4
```

Execute the `Aleemra_Scraping_Using_Request.py` script using a Python interpreter. This can be done via the command line:
```
python Aleemra_Scraping_Using_Request.py
```

## Data Format

The extracted data is structured in JSON format as follows:

```json
{
 "WebsiteName": "almeera.online",
 "Categories": [
     {
         "CategoryName": "string",
         "CategoryLink": "string",
         "ImageLink": "string",
         "Subcategories": [
             {
                 "SubCategoryName": "string",
                 "SubCategoryLink": "string",
                 "ImageLink": "string",
                 "Products": [
                     {
                         "ProductTitle": "string",
                         "ProductPrice": "string",
                         "ProductSKU": "string",
                         "ProductImageURL": "string"
                     },
                     // Additional products...
                 ]
             },
             // Additional subcategories...
         ]
     },
     // Additional categories...
 ]
}

```
## Note
- Ensured the extraction of data adheres to legal and ethical standards.
- The scraping process complies with the website's robots.txt guidelines.
- Adequate waiting time is implemented between requests to avoid burdening the website’s server.
- The extracted data is validated and cleaned where necessary.
- Pagination is managed to navigate through multiple pages of products within each category/subcategory.
- Error handling is implemented to manage potential issues that might arise during the scraping process.
