import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

def fetch_content(url):
    try:
        response = requests.get(url)
        response.raise_for_status()
        return response.content
    except requests.RequestException as e:
        print(f"Failed to fetch {url}: {e}")
        return None

def extract_text_and_links(html_content, base_url):
    soup = BeautifulSoup(html_content, 'html.parser')
    text_content = soup.get_text()
    links = [urljoin(base_url, link['href']) for link in soup.find_all('a', href=True)]
    return text_content, links

def save_to_file(filename, parent_url, text_content, links):
    with open(filename, 'w', encoding='utf-8') as file:
        file.write(f"URL: {parent_url}\n\n")
        file.write("Extracted Text Content:\n")
        file.write(text_content)
        file.write("\n\nExtracted Links:\n")
        for link in links:
            file.write(link + "\n")


def crawl(url, filename):
    # Fetch and process the main URL
    html_content = fetch_content(url)
    if html_content is None:
        return
    
    text_content, links = extract_text_and_links(html_content, url)
    
    # Save the parent page content
    save_to_file(filename, url, text_content, links)
    
    # Process each sub-link
    for link in links:
        sub_html_content = fetch_content(link)
        if sub_html_content is not None:
            sub_text_content, sub_links = extract_text_and_links(sub_html_content, link)
            save_to_file(f"{filename}_{link.split('/')[-1]}.txt", link, sub_text_content, sub_links)