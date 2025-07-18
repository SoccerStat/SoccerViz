def make_search_function(all_teams: list[str], teamA = None) -> list[str]:
    teams = all_teams.copy()
    if teamA:
        teams.remove(teamA)

    def search(term: str) -> list[str]:
        if not term:
            return []
        return [team for team in teams if term.lower() in team.lower()]
    return search