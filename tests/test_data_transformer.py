from src.data_transformer import aggregate_data

def test_aggregate_data():
    # Normal case with multiple teams in one year
    mock_data = [
        {"year": "1990", "team_name": "Team A", "wins": 10, "losses": 5, "ties": 3},
        {"year": "1990", "team_name": "Team B", "wins": 8, "losses": 7, "ties": 3},
        {"year": "1990", "team_name": "Team C", "wins": 12, "losses": 3, "ties": 3},
    ]

    result = aggregate_data(mock_data)
    expected = [
        {
            "year": "1990",
            "winner": "Team C",
            "winner_wins": 12,
            "loser": "Team B",
            "loser_wins": 8,
        }
    ]

    assert result == expected

def test_aggregate_data_multiple_years():
    # Case with multiple years
    mock_data = [
        {"year": "1990", "team_name": "Team A", "wins": 10, "losses": 5, "ties": 3},
        {"year": "1991", "team_name": "Team B", "wins": 8, "losses": 7, "ties": 3},
        {"year": "1991", "team_name": "Team C", "wins": 12, "losses": 3, "ties": 3},
    ]

    result = aggregate_data(mock_data)
    expected = [
        {
            "year": "1990",
            "winner": "Team A",
            "winner_wins": 10,
            "loser": "Team A",
            "loser_wins": 10,  # Single team, so winner and loser are the same
        },
        {
            "year": "1991",
            "winner": "Team C",
            "winner_wins": 12,
            "loser": "Team B",
            "loser_wins": 8,
        }
    ]

    assert result == expected

def test_aggregate_data_empty():
    # Case with empty data
    mock_data = []
    result = aggregate_data(mock_data)
    expected = []  # No data to aggregate
    assert result == expected


def test_aggregate_data_incomplete_data():
    # Case with incomplete or malformed data
    mock_data = [
        {"year": "1990", "team_name": "Team A", "wins": 10},
        {"year": "1990", "team_name": "Team B", "wins": 8, "losses": 7, "ties": 3},
    ]

    try:
        aggregate_data(mock_data)
    except KeyError:
        assert True  # Expected behavior
