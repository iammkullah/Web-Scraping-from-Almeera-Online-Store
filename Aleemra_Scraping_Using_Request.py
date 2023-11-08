# -*- coding: utf-8 -*-
"""
Created on Tue Nov  7 05:57:13 2023

@author: Muhammad Kaleem Ullah
"""

import json
import requests
from bs4 import BeautifulSoup as bs

# Define the base URL
base_url = 'https://almeera.online/'

# Define headers if necessary (user-agent, etc.)
headers = {'User-Agent': 'Mozilla/5.0'}

# Send a GET request to the website
response = requests.get(base_url, headers=headers)

category_names = []
category_urls = []
category_image_urls = []

# Define lists to store the data
category_data = []

# Check if the request was successful
if response.status_code == 200:
    # Parse the HTML content with BeautifulSoup
    soup = bs(response.content, 'html.parser')

    # Find all category elements
    category_elements = soup.select('div.block-subcategories ul li')

    for category_element in category_elements:
        # Get category name
        category_name = category_element.select_one('.subcategory-name').text.strip()

        # Get category link
        category_link = category_element.select_one('a')['href']
        category_link = 'https://almeera.online/' + category_link

        # Get image link
        image_link = category_element.select_one('img')['src']
        
        image_link = 'https:' + image_link
        try:
            # Download image
            image_response = requests.get(image_link)
            if image_response.status_code == 200:
                with open(f'category_images/{category_name}.jpg', 'wb') as img_file:
                    img_file.write(image_response.content)
        except requests.HTTPError as http_err:
            print(f'HTTP error occurred: {http_err}')
        except Exception as err:
            print(f'An error occurred: {err}')
            
        # Save information in a list
        category_names.append(category_name)
        category_urls.append(category_link)
        category_image_urls.append(image_link)

        # Print information
        print(f'Category Name: {category_name}')
        print(f'Category Link: {category_link}')
        print(f'Image Link: {image_link}')
        print(f'Image saved as: category_images/{category_name}.jpg')
        
        category_info = {
            "CategoryName": category_name,
            "CategoryLink": category_link,
            "ImageLink": image_link,
            "Subcategories": []
        }
        
        # Send a GET request to the category page
        category_response = requests.get(category_link, headers=headers)
        
        category_soup = bs(category_response.content, 'html.parser')
        
        subcategory_elements = category_soup.select('div.block.block-block.block-subcategories > div > ul > li')
        
        sub_category_names = []
        sub_category_urls = []
        sub_category_image_urls = []
        
        for subcategory_element in subcategory_elements:
            # Get category name
            sub_category_name = subcategory_element.select_one('.subcategory-name').text.strip()
            
            # Get sub category link
            sub_category_link = subcategory_element.select_one('a')['href']
            sub_category_link = 'https://almeera.online/' + sub_category_link
            
            # Get image link
            image_link = subcategory_element.select_one('img')['src']
            
            image_link = 'https:' + image_link
            # Download image
            
            try:
                # Download image
                image_response = requests.get(image_link)
                image_response.raise_for_status()  # This will raise an HTTPError if the HTTP request returned an unsuccessful status code
            
                with open(f'sub_category_images/{sub_category_name}.jpg', 'wb') as img_file:
                    img_file.write(image_response.content)
                    
                print(f'Image saved as: sub_category_images/{sub_category_name}.jpg')
            
            except requests.HTTPError as http_err:
                print(f'HTTP error occurred: {http_err}')
            except Exception as err:
                print(f'An error occurred: {err}')

            # Save information in a list
            sub_category_names.append(sub_category_name)
            sub_category_urls.append(sub_category_link)
            sub_category_image_urls.append(image_link)

            # Print information
            print(f'Sub Category Name: {sub_category_name}')
            print(f'Sub Category Link: {sub_category_link}')
            print(f'Image Link: {image_link}')
            print(f'Image saved as: sub_category_images/{sub_category_name}.jpg')
            
            subcategory_info = {
                "SubCategoryName": sub_category_name,
                "SubCategoryLink": sub_category_link,
                "ImageLink": image_link,
                "Products": []
            }
            
            
            # Send a GET request to the category page
            sub_category_response = requests.get(sub_category_link, headers=headers)
            
            sub_category_soup = bs(sub_category_response.content, 'html.parser')
            
        
            # Find all product elements
            product_elements = sub_category_soup.find_all('li', class_='product-cell box-product')
    
            # Iterate through the product elements
            for product_element in product_elements[:5]:  # Limit to 5 products per page
                # Get product title
                title = product_element.find('h5', class_='product-name').text.strip()
                # Remove invalid characters from title
                title = title.replace('?', '').replace('/', '').replace('\\', '').replace(':', '')
                
                # Get product price
                price = product_element.find('span', class_='price product-price').text.strip()

                # Get product SKU if available
                sku_element = product_element.find('div', class_='segment-product-data')
                sku_data = json.loads(sku_element['data-segment-data']) if sku_element else None
                sku = sku_data['sku'] if sku_data and 'sku' in sku_data else None

                # Get product image URL
                image_url = product_element.find('img', class_='photo')['src']

                # Check if the URL starts with "//", add a scheme if needed
                if image_url.startswith('//'):
                    image_url = 'https:' + image_url

                # Download image
                try:
                    image_response = requests.get(image_url)
                    if image_response.status_code == 200:
                        with open(f'product_images/{title}.jpg', 'wb') as img_file:
                            img_file.write(image_response.content)
                except requests.HTTPError as http_err:
                    print(f'HTTP error occurred: {http_err}')
                except Exception as err:
                    print(f'An error occurred: {err}')
                    
                # Print information
                print(f'Product Title: {title}')
                print(f'Product Price: {price}')
                print(f'Product SKU: {sku}')
                print(f'Image URL: {image_url}')
                print(f'Image saved as: product_images/{title}.jpg')
                
                product_info = {
                    "ProductTitle": title,
                    "ProductPrice": price,
                    "ProductSKU": sku,
                    "ProductImageURL": image_url
                }
                
                subcategory_info["Products"].append(product_info)
                
            # Find all pagination links
            pagination_links = sub_category_soup.find_all("div", class_="list-pager list-pager-bottom")
            
            if len(pagination_links) > 0:
                # Extract all page links
                page_links = pagination_links[0].select('.pagination.grid-list a')
                
                # Define the range of pages you want to scrape (e.g., from page 2 to page 4)
                start_page = 1
                end_page = 1
                
                # Filter out links that correspond to pages
                #page_links = [link for link in page_links if link.has_attr('href') and link['href'].startswith('deals/?pageId=')]
                
                # Iterate through the filtered links
                for page_link in page_links[start_page-1:end_page]:
                    page_url = page_link['href']
                    page_url = 'https://almeera.online/' + page_url
                    # Add your code here to scrape the products on each page
                    print(f'Scraping products on page {page_url}')
                    
                    # Send a GET request to the category page
                    sub_category_response = requests.get(page_url, headers=headers)
                    
                    sub_category_soup = bs(sub_category_response.content, 'html.parser')
                    
                
                    # Find all product elements
                    product_elements = sub_category_soup.find_all('li', class_='product-cell box-product')
            
                    # Iterate through the product elements
                    for product_element in product_elements[:5]:  # Limit to 5 products per page
                        # Get product title
                        title = product_element.find('h5', class_='product-name').text.strip()
                        # Remove invalid characters from title
                        title = title.replace('?', '').replace('/', '').replace('\\', '').replace(':', '')
                        
                        # Get product price
                        price = product_element.find('span', class_='price product-price').text.strip()
    
                        # Get product SKU if available
                        sku_element = product_element.find('div', class_='segment-product-data')
                        sku_data = json.loads(sku_element['data-segment-data']) if sku_element else None
                        sku = sku_data['sku'] if sku_data and 'sku' in sku_data else None
    
                        # Get product image URL
                        image_url = product_element.find('img', class_='photo')['src']
    
                        # Check if the URL starts with "//", add a scheme if needed
                        if image_url.startswith('//'):
                            image_url = 'https:' + image_url
                        
                        try:
                            # Download image
                            image_response = requests.get(image_url)
                            if image_response.status_code == 200:
                                with open(f'product_images/{title}.jpg', 'wb') as img_file:
                                    img_file.write(image_response.content)
                        except requests.HTTPError as http_err:
                            print(f'HTTP error occurred: {http_err}')
                        except Exception as err:
                            print(f'An error occurred: {err}')
                        
                        # Print information
                        print(f'Product Title: {title}')
                        print(f'Product Price: {price}')
                        print(f'Product SKU: {sku}')
                        print(f'Image URL: {image_url}')
                        print(f'Image saved as: product_images/{title}.jpg')
                        
                        product_info = {
                                "ProductTitle": title,
                                "ProductPrice": price,
                                "ProductSKU": sku,
                                "ProductImageURL": image_url
                            }
                        subcategory_info["Products"].append(product_info)
                                    
            category_info["Subcategories"].append(subcategory_info)
        category_data.append(category_info)
                          
else:
    print(f'Error: Unable to retrieve page. Status code: {response.status_code}')

# Define the output structure
output_data = {
    "WebsiteName": "almeera.online",
    "Categories": category_data
}

# Save the data to a JSON file
with open('output.json', 'w') as json_file:
    json.dump(output_data, json_file, indent=4)

print("Done with scraping Aleemra ...")

