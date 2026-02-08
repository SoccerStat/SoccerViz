from typing import Callable


def team_search_function(all_teams: list[str], teamA=None) -> Callable[[str], list[str]]:
    teams = [(team, team.lower()) for team in all_teams]
    if teamA:
        teams.remove(teamA)

    def search(term: str) -> list[str]:
        if not term:
            return []
        t = term.lower()
        return [team for team, l_team in teams if t in l_team]

    return search


def player_search_function(all_players: list[str]) -> Callable[[str], list[str]]:
    players = [(player, player.lower()) for player in all_players]

    def search(term: str) -> list[str]:
        if not term:
            return []
        t = term.lower()
        return [player for player, l_player in players if t in l_player]

    return search
