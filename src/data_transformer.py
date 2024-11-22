from typing import List, Dict

def aggregate_data(data: List[Dict]) -> List[Dict]:
    """
    function to find team with the most wins and the least wins per year
    Args:
        data (List[Dict]): A list of dictionaries with table data.
    Returns:
        List[Dict]: A list of dictionaries with winners and losers by year.
    """
    year_stats = {}
    for row in data:
        year = row["year"]
        if year not in year_stats:
            year_stats[year] = {"winner": row, "loser": row}
        else:
            if row["wins"] > year_stats[year]["winner"]["wins"]:
                year_stats[year]["winner"] = row
            if row["wins"] < year_stats[year]["loser"]["wins"]:
                year_stats[year]["loser"] = row

    return [
        {
            "year": year,
            "winner": stats["winner"]["team_name"],
            "winner_wins": stats["winner"]["wins"],
            "loser": stats["loser"]["team_name"],
            "loser_wins": stats["loser"]["wins"]
        }
        for year, stats in year_stats.items()
    ]
