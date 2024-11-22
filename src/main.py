import asyncio
import time
from html_scraper import scrape_pages
from data_transformer import aggregate_data
from file_writer import write_zip, write_excel

BASE_URL = "https://www.scrapethissite.com/pages/forms/"
OUTPUT_ZIP = "hockey_stats.zip"
OUTPUT_EXCEL = "hockey_stats.xlsx"

async def main():
    start_time = time.time()
    html_files, all_data = await scrape_pages(BASE_URL, pages=24)
    summary_data = aggregate_data(all_data)
    write_zip(html_files, OUTPUT_ZIP)
    write_excel(all_data, summary_data, OUTPUT_EXCEL)
    end_time = time.time()
    print(f"Execution completed in {end_time - start_time:.2f} seconds.")

if __name__ == "__main__":
    asyncio.run(main())
