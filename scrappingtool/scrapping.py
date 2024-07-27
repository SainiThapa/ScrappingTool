import re

import pandas as pd
import requests
from bs4 import BeautifulSoup

from .models import Newsheadline, Webportal


# Function to preprocess Nepali text
def preprocess_nepali_text(text):
    subject=text
    # Remove non-Nepali characters
    text = re.sub(r'[^\u0900-\u097F\s]', '', text)
    # Remove extra whitespaces and unnecessary characters
    text = re.sub(r'\s+', ' ', text)
    # Normalize text
    text = text.strip()
    if text:
        return text
    else:
        return subject

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
            'name': 'Hajurko Khabar',
            'url': 'https://hajurkokhabar.com/category/समाचार?page={}',
            'headers': {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'},
            'news_block_class': 'listing__news',
            'title_class': 'news__title',
            'post_hour_class': 'time_date'
        },
           {
            'name': 'Modi Municipality',
            'url': 'https://modimun.gov.np/news-notices?page={}',
            'headers': {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'},
            'news_block_class': 'node node-article node-teaser clearfix',
            'title_class': '',
            'post_hour_class': ''
        },
          {
            'name': 'Gorkhapatra',
            'url': 'https://gorkhapatraonline.com/categories/national?page={}',
            'headers': {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'},
            'news_block_class': 'item-content d-flex flex-column align-items-start justify-content-center',
            'title_class': 'item-title mb-2',
            'post_hour_class': 'entry-meta meta-color-dark mb-2'
        },
          {
            'name': 'Gorkhapatra',
            'url': 'https://gorkhapatraonline.com/categories/politics?page={}',
            'headers': {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'},
            'news_block_class': 'item-content d-flex flex-column align-items-start justify-content-center',
            'title_class': 'item-title mb-2',
            'post_hour_class': 'entry-meta meta-color-dark mb-2'
        },
          {
            'name': 'Gorkhapatra',
            'url': 'https://gorkhapatraonline.com/categories/sports?page={}',
            'headers': {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'},
            'news_block_class': 'item-content d-flex flex-column align-items-start justify-content-center',
            'title_class': 'item-title mb-2',
            'post_hour_class': 'entry-meta meta-color-dark mb-2'
        },
           {
            'name': 'Gorkhapatra',
            'url': 'https://gorkhapatraonline.com/categories/province?page={}',
            'headers': {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'},
            'news_block_class': 'item-content d-flex flex-column align-items-start justify-content-center',
            'title_class': 'item-title mb-2',
            'post_hour_class': 'entry-meta meta-color-dark mb-2'
        },
    ]

    for website in websites:
     
        for j in range(1, 11):
            try:
                webpage = requests.get(website['url'].format(j), headers=website['headers'])
                webpage.raise_for_status()
                webportal_exists, created = Webportal.objects.get_or_create(page_title=website['name'], page_url=website['url'].format(j))

                if created:
                    print(f"Created new web portal instance for {website['name']}")
                webportal_instance = Webportal.objects.get(page_title=website['name'],page_url=website['url'].format(j))
                
            except requests.exceptions.RequestException as e:
                print(f"Failed to retrieve data from {website['name']} page {j}. Error: {e}")
                continue
            try:
                soup = BeautifulSoup(webpage.content, 'html.parser')
            except:
                soup=BeautifulSoup(webpage.content,'lxml')
            news_data = soup.find_all('div', class_=website['news_block_class'])

            for i in news_data:
                title_block=['h2','span','div']
                try:
                    for block in title_block: 
                        news_title = i.find(title_block, class_=website['title_class'])
                        if news_title is not None:
                            break
                except:
                    raise ValueError("News title not found")

                newsblock=['div','span','ul']
                try:
                    for block in newsblock:
                        post_hour = i.find(block, class_=website['post_hour_class'])
                        if post_hour is not None:
                            break
                except:
                        raise ValueError("Post hour not found")
                        
                if news_title and post_hour:
                    title_text = news_title.text.strip()
                    post_hour_text = post_hour.text.strip()
                    final_data.append({'title': title_text, 'post_hour': post_hour_text})                    
                    try:
                        newsheadline, created=Newsheadline.objects.get_or_create(
                            news_title=title_text,  
                            news_source=webportal_instance,
                            news_upload_date=post_hour_text)
                        
                        if created:
                            print(f"News Created : {title_text}")
                        else:
                            print(f"News already exists : {title_text}")

                    except Exception as e:
                        print(f"An error occured : {e}")
    final_df = pd.DataFrame(final_data) 
    final_df['title_cleaned'] = final_df['title'].apply(preprocess_nepali_text)
    final_df['title_tokens'] = final_df['title_cleaned'].str.split()
    
    return final_df


# Search function
def search_news(newsheadlines, query):
    query_cleaned = preprocess_nepali_text(query)
    results = [newsheadline for newsheadline in newsheadlines 
               if query_cleaned in preprocess_nepali_text(newsheadline.news_title)]
    return results

# Main function to scrape, search, and display results
def search_and_display(searchquery):
    try:
        # Scrape news and preprocess data
        processed_df = scrape_news()
        print("Scraping completed successfully.")

        # Sample search query
        newsheadlines=Newsheadline.objects.all()
        matching_newsheadlines = search_news(newsheadlines, searchquery)
        return matching_newsheadlines
    
    except Exception as e:
        print(f"An error occurred during data processing: {e}")
        return Newsheadline.objects.none()