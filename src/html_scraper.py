import aiohttp
from bs4 import BeautifulSoup
import asyncio
import ssl
from typing import Dict, List, Tuple

async def fetch_html(session: aiohttp.ClientSession, url: str) -> str:
    """
    Fetch HTML content asynchronously
    Args:
        session (aiohttp.ClientSession): The session object to handle requests.
        url (str): The URL to fetch.

    Returns:
        str: The HTML content of the response.
    """
    ssl_context = ssl.create_default_context()
    ssl_context.check_hostname = False
    ssl_context.verify_mode = ssl.CERT_NONE

    async with session.get(url, ssl=ssl_context) as response:
        return await response.text()

async def scrape_pages(base_url: str, pages: int) -> Tuple[Dict[str, str], List[Dict]]:
    """
    Fetch HTML pages concurrently and parse their content.

    Args:
        base_url (str): The base URL of the site.
        pages (int): The number of pages to scrape.

    Returns:
        Tuple[Dict[str, str], List[Dict]]:
            - A dictionary of filenames to HTML content.
            - A list of parsed data dictionaries.
    """
    html_files = {}
    data_rows = []

    async with aiohttp.ClientSession() as session:
        # Create tasks for all page requests
        tasks = [
            asyncio.create_task(fetch_html(session, f"{base_url}?page_num={i}"))
            for i in range(1, pages + 1)
        ]
        # Await all tasks to fetch HTML pages concurrently
        html_pages = await asyncio.gather(*tasks)

    # Process HTML pages
    html_files = {f"{i + 1}.html": html for i, html in enumerate(html_pages)}
    data_rows = [row for html in html_pages for row in parse_html(html)]
    return html_files, data_rows

def parse_html(html: str) -> List[Dict]:
    """
    Parses the HTML content to extract data from the hockey stats table.

    Args:
        html (str): The HTML content.

    Returns:
        List[Dict]: A list of dictionaries containing table data.
    """
    soup = BeautifulSoup(html, "html.parser")
    table = soup.find("table", {"class": "table"})
    if not table:
        return []

    rows = table.find_all("tr")[1:]  # Skip the header row
    data = []
    for row in rows:
        cols = [col.text.strip() for col in row.find_all("td")]
        if cols:
            data.append({
                "team_name": cols[0],
                "year": cols[1],
                "wins": int(cols[2]) if cols[2].isdigit() else 0,
                "losses": int(cols[3]) if cols[3].isdigit() else 0,
                "ot_losses": int(cols[4]) if cols[4].isdigit() else 0,
                "win_pct": float(cols[5]) if cols[5].replace('.', '', 1).isdigit() else 0.0,
                "goals_for": int(cols[6]) if cols[6].isdigit() else 0,
                "goals_against": int(cols[7]) if cols[7].isdigit() else 0,
                "goal_difference": int(cols[8]) if cols[8].isdigit() else 0
            })
    return data
