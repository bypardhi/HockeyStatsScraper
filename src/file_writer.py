from typing import List, Dict
from zipfile import ZipFile
from openpyxl import Workbook
from concurrent.futures import ThreadPoolExecutor

def write_zip(html_files: Dict[str, str], zip_filename: str):
    """
    Writes multiple HTML files into a ZIP archive.
    """
    with ZipFile(zip_filename, "w") as zipf:
        for name, content in html_files.items():
            zipf.writestr(name, content)

def write_excel(data1: List[Dict], data2: List[Dict], filename: str):
    """
    Writes the parsed data to an Excel file with two sheets.
    Args:
        data1 (List[Dict]): All scraped data for Sheet 1.
        data2 (List[Dict]): Aggregated winner/loser data for Sheet 2.
        filename (str): The name of the output Excel file.
    Returns:
        excel file with two sheets.
    """
    workbook = Workbook()

    # Sheet 1: All Data
    sheet1 = workbook.active
    sheet1.title = "NHL Stats 1990-2011"
    sheet1.append(["Team Name", "Year", "Wins", "Losses", "OT Losses", "Win %", "Goals For (GF)", "Goals Against (GA)", "+/-"])
    for row in data1:
        sheet1.append([
            row["team_name"],
            row["year"],
            row["wins"],
            row["losses"],
            row["ot_losses"],
            row["win_pct"],
            row["goals_for"],
            row["goals_against"],
            row["goal_difference"]
        ])

    # Sheet 2: Winners and Losers
    sheet2 = workbook.create_sheet(title="Winner and Loser per Year")
    sheet2.append(["Year", "Winner", "Winner Num. of Wins", "Loser", "Loser Num. of Wins"])
    for row in data2:
        sheet2.append([row["year"], row["winner"], row["winner_wins"], row["loser"], row["loser_wins"]])

    workbook.save(filename)

def save_html_files(html_files: Dict[str, str]):
    """
    Save multiple HTML files concurrently.
    """
    def save_file(name, content):
        with open(name, "w", encoding="utf-8") as f:
            f.write(content)

    with ThreadPoolExecutor() as executor:
        executor.map(lambda item: save_file(*item), html_files.items())
