# Hockey Stats Scraper

This project is designed to scrape hockey team statistics from [Scrape This Site](https://www.scrapethissite.com/pages/forms/), process the data, and produce meaningful outputs. The script handles:
- Extracting data from multiple web pages.
- Transforming the extracted data into structured formats.
- Graceful handling of missing or invalid data.

## **Approach**

1. **Scraping HTML Content**:
   - The program uses `aiohttp` to asynchronously fetch HTML content from the website.
   - SSL verification is bypassed to handle certificate errors.

2. **Parsing HTML**:
   - HTML content is processed using `BeautifulSoup`.
   - Data is extracted from the table present on the webpage.

3. **Data Handling**:
   - Rows of the table are converted into dictionaries.
   - Missing or invalid numeric fields are replaced with default values (e.g., `0`).

4. **Output**:
   - The parsed data is printed to the console and can be extended to save in various formats like Excel or JSON.

## **File Descriptions**

### `html_scraper.py`
This file contains the core logic for fetching, parsing, and processing the data.

- **Functions**:
  1. `fetch_html(session: aiohttp.ClientSession, url: str) -> str`:
     - Fetches HTML content from a given URL asynchronously.
     - Uses `aiohttp` to handle network requests.
     - Bypasses SSL verification to handle certificate issues.

  2. `scrape_pages(base_url: str, pages: int) -> (Dict[str, str], List[Dict])`:
     - Iterates through multiple pages of the site.
     - Fetches HTML content for each page and parses it using `parse_html`.

  3. `parse_html(html: str) -> List[Dict]`:
     - Extracts and processes table data from the provided HTML content.
     - Converts rows into dictionaries with keys: `year`, `team`, `wins`, `losses`, and `ties`.
     - Handles missing or invalid data gracefully.

- **Example Output**:
  ```json
  [
      {
          "year": "1990",
          "team": "Boston Bruins",
          "wins": 44,
          "losses": 24,
          "ties": 0
      },
      {
          "year": "1991",
          "team": "Buffalo Sabres",
          "wins": 31,
          "losses": 30,
          "ties": 5
      }
  ]
