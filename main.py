from crawler.cuda_crawler import WebCrawler

if __name__ == "__main__":
    crawler = WebCrawler()  # Initialize an instance of WebCrawler
    main_url = "https://docs.nvidia.com/cuda/"
    output_filename = "nvidia_toolkit_clean"
    crawler.crawl(main_url, output_filename, max_sublinks=5)