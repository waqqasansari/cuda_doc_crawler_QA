# WebCrawler

A Python web crawler that extracts text and links from a given URL and saves them to files.

## Getting Started

### Prerequisites

- Python 3.8 or later
- `requests` and `beautifulsoup4` libraries installed

### Installation

1. Clone the repository: `git clone https://github.com/your-username/webcrawler.git`
2. Install the required libraries: `pip install -r requirements.txt`

## Usage

### Running the Crawler

1. Run the crawler using: `python main.py`
2. Provide the URL to crawl as an argument: `python main.py https://docs.nvidia.com/cuda/`
3. Optionally, specify the output filename and maximum number of sublinks to crawl: `python main.py https://docs.nvidia.com/cuda/ output.txt 5`

### Configuration

The crawler can be configured using the following environment variables:

- `BASE_URL`: The base URL to use for relative links (default: `https://docs.nvidia.com/cuda/`)
- `MAX_SUBLINKS`: The maximum number of sublinks to crawl (default: 5)

### Output

The crawler saves the extracted text and links to files in the `data` directory. The filename is generated based on the URL and the sublink number.

## License

This project is licensed under the MIT License. See [LICENSE](LICENSE) for details.

## Contributing

Contributions are welcome Please open an issue or submit a pull request to contribute to this project.

## Acknowledgments

- This project uses the `requests` and `beautifulsoup4` libraries.

## Contact

Waqqas Khusraw Ansari - waqmid@gmail.com
