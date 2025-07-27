import streamlit as st
import pandas as pd
import numpy as np
from scipy.stats import bernoulli


def simulate_by_side(teams: pd.DataFrame, played_home: bool, n_sim: int):
    xgs = teams.loc[teams["played_home"] == played_home, 'xg_shot']
    if not (xgs.empty | xgs.isna().any()):
        simulations = np.array([bernoulli(xg).rvs(n_sim) for xg in xgs])
        return simulations.sum(axis=0)
    return teams[(teams["played_home"] == played_home) & (teams["outcome"] == "goal")].shape[0]

# Average number of points per simulation
def mean_and_round(xp, r):
    return round(np.mean(xp), r)

def simulate_matches(
        teams_shots: pd.DataFrame,
        partition: str,
        n_sim: int,
        r: int
) -> pd.DataFrame:
    both_teams_shots = teams_shots.copy()

    home_theoretical_goals = simulate_by_side(both_teams_shots, True, n_sim)
    away_theoretical_goals = simulate_by_side(both_teams_shots, False, n_sim)

    home_xp_by_simulation = np.where(
        home_theoretical_goals > away_theoretical_goals,
        3,
        np.where(
            home_theoretical_goals == away_theoretical_goals,
            1,
            0
        )
    )
    away_xp_by_simulation = np.where(home_xp_by_simulation == 1, 1, 3 - home_xp_by_simulation)

    home_xp = mean_and_round(home_xp_by_simulation, r)
    away_xp = mean_and_round(away_xp_by_simulation, r)

    home_subset = both_teams_shots.loc[both_teams_shots['played_home'], 'Club']
    away_subset = both_teams_shots.loc[~both_teams_shots['played_home'], 'Club']

    return pd.DataFrame({
        'Club': [home_subset.iloc[0] if not home_subset.empty else None, away_subset.iloc[0] if not away_subset.empty else None],
        'played_home': [True, False],
        'Partition': [partition, partition],
        'xP': [home_xp, away_xp]
    })

@st.cache_data(show_spinner=False)
def build_expected_performance_ranking(
        expected_team_stats: pd.DataFrame,
        side: str = 'both',
        n_sim: int = 1000000,
        r: int = 2
) -> pd.DataFrame:
    if side == 'home':
        side_filter = 'played_home'
    elif side == 'away':
        side_filter = 'not played_home'
    else:
        side_filter = 'played_home | not played_home'

    if not expected_team_stats.empty:
        matches_and_partitions = expected_team_stats[['match', 'Partition']].drop_duplicates()

        return \
            pd.concat(
                [
                    simulate_matches(
                        expected_team_stats.loc[expected_team_stats['match'] == id_match].copy(),
                        partition,
                        n_sim,
                        r
                    )
                    for (id_match, partition) in matches_and_partitions.itertuples(index=False)
                ]
            ).query(side_filter)[['Club', 'Partition', 'xP']].groupby(['Club', 'Partition']).sum().reset_index()

    return pd.DataFrame(columns=['Club', 'Partition', 'xP'])

def merge_rankings(
    teams_ranking: pd.DataFrame,
    expected_performance_ranking: pd.DataFrame,
    r: int = 2
) -> pd.DataFrame:

    merged_ranking = pd.merge(
        teams_ranking,
        expected_performance_ranking,
        how='left',
        left_on=['Club', 'Week'],
        right_on=['Club', 'Partition']
    )

    merged_ranking['xP/Match'] = \
        round(merged_ranking['xP'] / merged_ranking['Partition'], r)

    merged_ranking['Diff Points'] = \
        merged_ranking['Points'] - merged_ranking['xP']

    return merged_ranking