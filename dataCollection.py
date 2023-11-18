import requests
import os
# Replace 'your_api_key' with your actual Rainforest API key
api_key = os.environ('RAINFOREST_KEY')

    
def fetch_product_data(url):
    params = {
        'api-key' : api_key,
        'url' : url,
    }
    response = requests.get("https://api.rainforestapi.com/request", params)
    return response.json()


# Function to fetch Q&A using URL
def fetch_questions(url):
    params = {
        'api-key' : api_key,
        'type' : 'questions',
        'url' : url,
        'max_page' : 2,
        'sort_by' : 'most_helpful'
    }
    response = requests.get("https://api.rainforestapi.com/request", params)
    return response.json()


def fetch_all_reviews(url):
    params = {
        'api-key' : api_key,
        'type' : 'reviews',
        'url' : url,
        'output' : 'json',
        'max_page' : 1,
        'sort_by' : 'most_recent'
    }

    response = requests.get("https://api.rainforestapi.com/request", params)
    if response.status_code == 200:
        return response.json()
    else:
        return "Not Found"



# Replace this with the actual URL of the Amazon product page
product_url = 'https://www.amazon.com/dp/product_page_url'

# Fetch and print Q&A
qa_data = fetch_questions(product_url)
print("Questions & Answers:")
print(qa_data)

# Fetch and print reviews
review_data = fetch_reviews(product_url)
print("\nRecent Reviews:")
print(review_data)
