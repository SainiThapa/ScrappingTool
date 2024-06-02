import re
import pandas as pd
import requests
from bs4 import BeautifulSoup

from scrappingtool.models import Newsheadline, Webportal

# Function to preprocess Nepali text
def preprocess_nepali_text(text):
    # Remove non-Nepali characters
    text = re.sub(r'[^\u0900-\u097F\s]', '', text)
    # Remove extra whitespaces and unnecessary characters
    text = re.sub(r'\s+', ' ', text)
    # Normalize text
    text = text.strip()
    return text


# def scrape_news():
#     final_data = []
#     for j in range(1, 11):
#         headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}
#         url = f'https://www.onlinekhabar.com/content/news/rastriya/page/{j}'
#         try:
#             webpage = requests.get(url, headers=headers)
#             webpage.raise_for_status()  # Raise an exception for any HTTP errors
#         except requests.exceptions.RequestException as e:
#             print(f"Failed to retrieve data from page {j}. Error: {e}")
#             continue  # Skip to the next iteration

#         soup = BeautifulSoup(webpage.content, 'html.parser')
#         news_data = soup.find_all('div', class_="teaser offset")

#         for i in news_data:
#             news_title = i.find('h2').find('a')

#             if news_title:  # Check if title is found
#                 title_text = news_title.text.strip()
#                 final_data.append({'title': title_text})

#     final_df = pd.DataFrame(final_data)

#     # Apply preprocessing to title column
#     final_df['title_cleaned'] = final_df['title'].apply(preprocess_nepali_text)
#     # Tokenization (split on whitespace) for title
#     final_df['title_tokens'] = final_df['title_cleaned'].str.split()

#     return final_df[['title', 'title_cleaned', 'title_tokens']]

def scrape_news():
    final_data = []

    # Define websites to scrape
    websites = [
        {
            'name': 'Online Khabar',
            'url': 'https://www.onlinekhabar.com/content/news/rastiya/page/{}',
            'headers': {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'},
            'news_block_class': 'span-4',
            'title_class': 'ok-news-title-txt',
            'post_hour_class': 'ok-news-post-hour'
        },
        {
            'name': 'Setopati',
            'url': 'https://www.setopati.com/exclusive?page={}',
            'headers': {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'},
            'news_block_class': 'items col-md-4',
            'title_class': 'main-title',
            'post_hour_class': 'time-stamp'
        },
        {
            'name': 'Manthali Nagarpalika',
            'url': 'https://manthalimun.gov.np/ne/node?page={}',
            'headers': {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'},
            'news_block_class': 'region',
            'title_class': 'views-field-title',
            'post_hour_class': 'field-content'
        }
    ]

    for website in websites:
        try:
            webportal_instance = Webportal.objects.get(page_title=website['name'])
        except Webportal.DoesNotExist:
            print(f"Webportal instance for {website['name']} does not exist.")
            continue
        for j in range(1, 3):
            try:
                webpage = requests.get(website['url'].format(j), headers=website['headers'])
                webpage.raise_for_status()
            except requests.exceptions.RequestException as e:
                print(f"Failed to retrieve data from {website['name']} page {j}. Error: {e}")
                continue

            soup = BeautifulSoup(webpage.content, 'html.parser')
            news_data = soup.find_all('div', class_=website['news_block_class'])

            for i in news_data:
                news_title = i.find('h2', class_=website['title_class'])
                post_hour = i.find('div', class_=website['post_hour_class'])

                if news_title and post_hour:
                    title_text = news_title.text.strip()
                    post_hour_text = post_hour.text.strip()
                    final_data.append({'title': title_text, 'post_hour': post_hour_text})                    
                    
                    if Newsheadline.objects.filter(news_source=webportal_instance,news_title=title_text,news_upload_date=post_hour).first():
                        print("News already exists")
                        pass
                    else:
                        newsheadline=Newsheadline.objects.create(news_source=webportal_instance,news_title=title_text, news_upload_date=post_hour_text)
                        newsheadline.save()
    final_df = pd.DataFrame(final_data)
    final_df['title_cleaned'] = final_df['title'].apply(preprocess_nepali_text)
    final_df['title_tokens'] = final_df['title_cleaned'].str.split()

    return final_df


# Search function
def search_news(df, query):
    query_cleaned = preprocess_nepali_text(query)
    results = df[df['title_cleaned'].str.contains(query_cleaned, case=False, na=False)]
    return results

# Main function to scrape, search, and display results
def main(searchquery):
    try:
        # Scrape news and preprocess data
        processed_df = scrape_news()
        print("Scraping completed successfully.")
        print(processed_df)

        # Sample search query
        query =  searchquery # Replace with your search query

        # Search news based on query
        search_results = search_news(processed_df, query)

        # Display search results
        if not search_results.empty:
            print("Search Results:")
            print(search_results[['title']])
        else:
            print("No matching news found.")
        news_title= search_results[['title']]
        return news_title
    
    except Exception as e:
        print(f"An error occurred during data processing: {e}")
        return 0

