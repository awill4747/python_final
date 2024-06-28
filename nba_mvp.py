import argparse
import requests
from bs4 import BeautifulSoup
import re


def get_player_stats():
    """
    Fetches player stats from the ESPN website.

    Returns:
        A list of dictionaries, each containing the player's name and stats.
    """
    url = 'https://www.espn.com/nba/stats/player/_/season/2023/seasontype/2'
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')

    names_table = soup.find('table', class_='Table Table--align-right Table--fixed Table--fixed-left')
    name_rows = names_table.find_all('tr')[1:]

    stats_table = soup.find('table', class_='Table Table--align-right')
    stat_rows = stats_table.find_all('tr')

    player_stats = []

    for name_row, stat_row in zip(name_rows, stat_rows[1:]):
        player_name_column = name_row.find('a', class_='AnchorLink')
        player_name = player_name_column.text.strip() if player_name_column else "N/A"

        columns = stat_row.find_all('td')

        if len(columns) < 9:
            print("Invalid row, skipping...")
            continue

        points = columns[3].text.strip()
        field_goal_percentage = columns[6].text.strip()
        three_point_percentage = columns[9].text.strip()
        rebounds = columns[13].text.strip()
        assists = columns[14].text.strip()

        player_stats.append({
            'Player': player_name,
            'Points': points,
            'Field Goal Percentage': field_goal_percentage,
            'Three Point Percentage': three_point_percentage,
            'Rebounds': rebounds,
            'Assists': assists
        })

    return player_stats


def calculate_mvp(player_stats, top_count):
    """
    Calculates the MVP based on player stats.

    Args:
        player_stats: A list of dictionaries containing player stats.
        top_count: The number of top players to consider.

    Returns:
        A tuple containing three lists:
        - The top players based on points scored.
        - The player with the best overall stats.
        - The second and third place players based on overall stats.
    """
    sorted_players_by_points = sorted(player_stats, key=lambda p: float(p['Points']), reverse=True)
    top_players = sorted_players_by_points[:top_count]

    sorted_players_by_overall = sorted(player_stats, key=lambda p: sum(float(p[key]) for key in p.keys() if key != 'Player'), reverse=True)
    best_player = sorted_players_by_overall[0]
    second_place = sorted_players_by_overall[1]
    third_place = sorted_players_by_overall[2]

    return top_players, best_player, second_place, third_place


def filter_players(player_stats, regex_pattern):
    """
    Filters the player stats based on a regular expression pattern.

    Args:
        player_stats: A list of dictionaries containing player stats.
        regex_pattern: The regular expression pattern to match player names.

    Returns:
        A filtered list of player stats matching the given pattern.
    """
    filtered_stats = []

    for player in player_stats:
        if re.search(regex_pattern, player['Player'], re.IGNORECASE):
            filtered_stats.append(player)

    return filtered_stats


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='NBA MVP Calculator')
    parser.add_argument('--top', type=int, default=5, help='number of top players to consider')
    parser.add_argument('--pattern', type=str, default='', help='regular expression pattern to filter player names')
    args = parser.parse_args()

    stats = get_player_stats()

    if args.pattern:
        stats = filter_players(stats, args.pattern)

    top_players, best_player, second_place, third_place = calculate_mvp(stats, args.top)

    print("Top Players:")
    for player in top_players:
        print(f"Player: {player['Player']}")
        print(f"Points: {player['Points']}")
        print(f"Field Goal Percentage: {player['Field Goal Percentage']}")
        print(f"Three Point Percentage: {player['Three Point Percentage']}")
        print(f"Rebounds: {player['Rebounds']}")
        print(f"Assists: {player['Assists']}")
        print("------------------------")

    print("Player with the Best Overall Stats:")
    print(f"Player: {best_player['Player']}")
    print(f"Points: {best_player['Points']}")
    print(f"Field Goal Percentage: {best_player['Field Goal Percentage']}")
    print(f"Three Point Percentage: {best_player['Three Point Percentage']}")
    print(f"Rebounds: {best_player['Rebounds']}")
    print(f"Assists: {best_player['Assists']}")
    print("------------------------")

    print("Second Place:")
    print(f"Player: {second_place['Player']}")
    print(f"Points: {second_place['Points']}")
    print(f"Field Goal Percentage: {second_place['Field Goal Percentage']}")
    print(f"Three Point Percentage: {second_place['Three Point Percentage']}")
    print(f"Rebounds: {second_place['Rebounds']}")
    print(f"Assists: {second_place['Assists']}")
    print("------------------------")

    print("Third Place:")
    print(f"Player: {third_place['Player']}")
    print(f"Points: {third_place['Points']}")
    print(f"Field Goal Percentage: {third_place['Field Goal Percentage']}")
    print(f"Three Point Percentage: {third_place['Three Point Percentage']}")
    print(f"Rebounds: {third_place['Rebounds']}")
    print(f"Assists: {third_place['Assists']}")
    print("------------------------")

    print(f"The NBA MVP should be: {best_player['Player']}")
