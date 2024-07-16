import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import os

import re

class WebCrawler:
    def fetch_content(self, url):
        self.base_url = "https://docs.nvidia.com/cuda/"
        try:
            print(f"Fetching {url}...")
            response = requests.get(url)
            response.raise_for_status()
            print(f"Fetched {url} successfully.")
            return response.content
        except requests.RequestException as e:
            print(f"Failed to fetch {url}: {e}")
            return None

    def extract_text_and_links(self, html_content, base_url):
        print("Extracting text and links...")
        soup = BeautifulSoup(html_content, 'html.parser')
        text_content = soup.get_text()
        links = [urljoin(self.base_url, link['href']) for link in soup.find_all('a', href=True) if not link['href'].startswith('http')]
        print(f"Extracted {len(links)} links.")
        return text_content, links

    def preprocess_text(self, text):
        # Remove leading and trailing whitespace
        text = text.strip()
        # Replace multiple whitespace characters with a single space
        text = re.sub(r'\s+', ' ', text)
        # Remove extra newline characters
        text = text.replace('\n', ' ')
        return text

    def save_to_file(self, filename, parent_url, text_content, links):
        # Ensure 'data' folder exists
        if not os.path.exists('data'):
            os.makedirs('data')
        
        # Construct the file path within the 'data' folder
        filepath = os.path.join('data', filename)
        
        print(f"Saving to {filepath}...")
        with open(filepath, 'w', encoding='utf-8') as file:
            file.write(text_content)
        print(f"Saved to {filepath}.")

    def crawl(self, url, filename, max_sublinks=5):
        print(f"Initiating crawl for {url}...")
        # Fetch and process the main URL
        html_content = self.fetch_content(url)
        if html_content is None:
            return
        
        text_content, links = self.extract_text_and_links(html_content, url)
        text_content = self.preprocess_text(text_content)  # Preprocess the text
        
        # Save the parent page content
        self.save_to_file(filename, url, text_content, links)
        
        # Process each sub-link, limit to max_sublinks
        count = 0
        for link in links:
            print(f"Processing sublink: {link}")
            if count >= max_sublinks:
                break
            sub_html_content = self.fetch_content(link)
            if sub_html_content is not None:
                sub_text_content, sub_links = self.extract_text_and_links(sub_html_content, link)
                sub_text_content = self.preprocess_text(sub_text_content)  # Preprocess the text
                self.save_to_file(f"{filename}_{link.split('/')[4]}.txt", link, sub_text_content, sub_links)
                count += 1