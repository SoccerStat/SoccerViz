from typing import Callable


def search_for_team(all_teams: list[str], teamA=None) -> Callable[[str], list[str]]:
    teams = [(team, team.lower()) for team in all_teams]
    if teamA:
        teams.remove((teamA, teamA.lower()))

    def search(term: str) -> list[str]:
        if not term:
            return []
        t = term.lower()
        return [team for team, l_team in teams if t in l_team]

    return search


def search_for_country(all_countries: list[str]) -> Callable[[str], list[str]]:
    countries = [(country, country.lower()) for country in all_countries]

    def search(term: str) -> list[str]:
        if not term:
            return []
        t = term.lower()
        return [country for country, l_country in countries if t in l_country]

    return search


def search_for_player(all_players: list[str]) -> Callable[[str], list[str]]:
    players = [(player, player.lower()) for player in all_players]

    def search(term: str) -> list[str]:
        if not term:
            return []
        t = term.lower()
        return [player for player, l_player in players if t in l_player]

    return search
