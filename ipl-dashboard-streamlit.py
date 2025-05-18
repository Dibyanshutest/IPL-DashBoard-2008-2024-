import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import streamlit as st
from datetime import datetime

# Set the style for seaborn plots
sns.set_style("whitegrid")
plt.rcParams["figure.figsize"] = (12, 8)

# Set page config
st.set_page_config(
    page_title="IPL Dashboard (2008-2024)",
    page_icon="🏏",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS to enhance the appearance
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem !important;
        font-weight: 700 !important;
        color: #0066cc !important;
        text-align: center !important;
        margin-bottom: 1rem !important;
        padding-bottom: 1rem !important;
        border-bottom: 2px solid #f0f2f6 !important;
    }
    .sub-header {
        font-size: 1.5rem !important;
        font-weight: 600 !important;
        color: #0066cc !important;
        margin-top: 1rem !important;
        margin-bottom: 1rem !important;
    }
    .card {
        border-radius: 5px !important;
        background-color: #ffffff !important;
        box-shadow: rgba(0, 0, 0, 0.1) 0px 1px 3px 0px, rgba(0, 0, 0, 0.06) 0px 1px 2px 0px !important;
        padding: 1.5rem !important;
        margin-bottom: 1rem !important;
    }
    .metric-card {
        background-color: #f8f9fa !important;
        border-radius: 8px !important;
        box-shadow: rgba(0, 0, 0, 0.05) 0px 1px 3px 0px !important;
        padding: 1rem !important;
        text-align: center !important;
    }
    .metric-value {
        font-size: 2rem !important;
        font-weight: 700 !important;
        color: #0066cc !important;
    }
    .metric-label {
        font-size: 0.9rem !important;
        color: #6c757d !important;
        font-weight: 500 !important;
    }
    .team-csk { color: #FDB913 !important; }
    .team-mi { color: #004BA0 !important; }
    .team-rcb { color: #EC1C24 !important; }
    .team-kkr { color: #3A225D !important; }
    .team-srh { color: #F7A721 !important; }
    .stPlotlyChart {
        background-color: white !important;
        border-radius: 8px !important;
        padding: 1rem !important;
        box-shadow: rgba(0, 0, 0, 0.05) 0px 1px 3px 0px !important;
    }
    .dataframe {
        font-size: 0.9rem !important;
    }
    .sidebar .sidebar-content {
        background-color: #f8f9fa !important;
    }
    .css-1d391kg {
        padding-top: 3.5rem !important;
    }
    .stMetric {
        background-color: white !important;
        padding: 15px !important;
        border-radius: 10px !important;
        box-shadow: 0 2px 5px rgba(0,0,0,0.1) !important;
    }
    .banned-notice {
        background-color: #ffe0e0 !important;
        border-left: 5px solid #ff0000 !important;
        padding: 15px !important;
        margin: 20px 0 !important;
        border-radius: 5px !important;
        font-weight: bold !important;
        color: #d32f2f !important;
        text-align: center !important;
        font-size: 1.2rem !important;
    }
</style>
""", unsafe_allow_html=True)

# Function to load and prepare data
@st.cache_data
def load_data():
    # For demo purposes, I'll create mock data
    # In a real app, you would use:
    # matches = pd.read_csv(r"matches.csv")
    # deliveries = pd.read_csv(r"deliveries.csv")
    
    # Create mock matches dataframe
    years = list(range(2008, 2025))
    teams = ['Chennai Super Kings', 'Mumbai Indians', 'Royal Challengers Bangalore', 
             'Kolkata Knight Riders', 'Rajasthan Royals', 'Delhi Capitals', 
             'Kings XI Punjab', 'Sunrisers Hyderabad', 'Gujarat Titans', 
             'Lucknow Super Giants']
    
    team_codes = {
        'Chennai Super Kings': 'CSK',
        'Mumbai Indians': 'MI',
        'Royal Challengers Bangalore': 'RCB',
        'Kolkata Knight Riders': 'KKR',
        'Rajasthan Royals': 'RR',
        'Delhi Capitals': 'DC',
        'Kings XI Punjab': 'PBKS',
        'Sunrisers Hyderabad': 'SRH',
        'Gujarat Titans': 'GT',
        'Lucknow Super Giants': 'LSG'
    }
    
    team_colors = {
        'Chennai Super Kings': '#FDB913',
        'Mumbai Indians': '#004BA0',
        'Royal Challengers Bangalore': '#EC1C24',
        'Kolkata Knight Riders': '#3A225D',
        'Rajasthan Royals': '#FF1493',
        'Delhi Capitals': '#0078BC',
        'Kings XI Punjab': '#ED1C24',
        'Sunrisers Hyderabad': '#F7A721',
        'Gujarat Titans': '#1D3160',
        'Lucknow Super Giants': '#A72056'
    }
    
    # Define banned teams by year
    banned_teams = {
        2016: ['Chennai Super Kings', 'Rajasthan Royals'],
        2017: ['Chennai Super Kings', 'Rajasthan Royals']
    }
    
    # Mock matches data
    matches_data = []
    match_id = 1
    
    for year in years:
        # Skip generating matches for banned teams in certain years
        active_teams = [team for team in teams if team not in banned_teams.get(year, [])]
        
        num_matches = 60  # Approximate number of matches per season
        for i in range(num_matches):
            if len(active_teams) < 2:
                continue
                
            team1_idx = np.random.randint(0, len(active_teams))
            team2_idx = np.random.randint(0, len(active_teams))
            while team2_idx == team1_idx:
                team2_idx = np.random.randint(0, len(active_teams))
                
            team1 = active_teams[team1_idx]
            team2 = active_teams[team2_idx]
            
            # Randomly select winner
            winner_idx = np.random.choice([team1_idx, team2_idx])
            winner = active_teams[winner_idx]
            
            # Create random date within IPL season months (April-May)
            month = np.random.choice([4, 5])
            day = np.random.randint(1, 28)
            date = f"{year}-{month:02d}-{day:02d}"
            
            # Create match entry
            match_entry = {
                'id': match_id,
                'season': year,
                'date': date,
                'team1': team1,
                'team2': team2,
                'team1_code': team_codes[team1],
                'team2_code': team_codes[team2],
                'winner': winner,
                'winner_code': team_codes[winner] if winner else None,
                'win_by_runs': np.random.randint(0, 100) if np.random.random() > 0.5 else 0,
                'win_by_wickets': np.random.randint(1, 10) if np.random.random() <= 0.5 else 0,
                'city': np.random.choice(['Mumbai', 'Chennai', 'Bangalore', 'Kolkata', 'Delhi', 'Hyderabad']),
                'venue': np.random.choice(['Wankhede Stadium', 'Eden Gardens', 'Chinnaswamy Stadium', 'Chepauk']),
                'toss_winner': np.random.choice([team1, team2]),
                'toss_decision': np.random.choice(['bat', 'field'])
            }
            
            matches_data.append(match_entry)
            match_id += 1
    
    matches_df = pd.DataFrame(matches_data)
    
    # Create mock players data
    all_players = []
    player_id = 1
    
    for team in teams:
        # Each team has about 20 players
        for i in range(20):  
            # Create player stats for each year
            for year in years:
                # Skip banned teams in certain years
                if year in banned_teams and team in banned_teams[year]:
                    continue
                    
                # Not all players play all years
                if np.random.random() > 0.3:  
                    matches_played = np.random.randint(5, 15)
                    
                    # For batsmen (player_id % 3 != 0)
                    if player_id % 3 != 0:
                        player_entry = {
                            'player_id': player_id,
                            'player_name': f"Player_{player_id}",
                            'team': team,
                            'team_code': team_codes[team],
                            'season': year,
                            'matches': matches_played,
                            'runs': np.random.randint(100, 700),
                            'avg': np.random.uniform(20, 50),
                            'strike_rate': np.random.uniform(120, 170),
                            'fifties': np.random.randint(0, 5),
                            'hundreds': np.random.randint(0, 2),
                            'wickets': np.random.randint(0, 3),
                            'economy': np.random.uniform(7, 12),
                            'player_type': 'Batsman'
                        }
                    # For bowlers
                    else:
                        player_entry = {
                            'player_id': player_id,
                            'player_name': f"Player_{player_id}",
                            'team': team,
                            'team_code': team_codes[team],
                            'season': year,
                            'matches': matches_played,
                            'runs': np.random.randint(20, 150),
                            'avg': np.random.uniform(10, 25),
                            'strike_rate': np.random.uniform(100, 140),
                            'fifties': 0,
                            'hundreds': 0,
                            'wickets': np.random.randint(5, 25),
                            'economy': np.random.uniform(6, 10),
                            'player_type': 'Bowler'
                        }
                    
                    all_players.append(player_entry)
            
            player_id += 1
    
    players_df = pd.DataFrame(all_players)
    
    # Create mock team performance data
    team_performance = []
    
    for team in teams:
        for year in years:
            # Some teams might not exist in certain years
            if (team == 'Gujarat Titans' and year < 2022) or \
               (team == 'Lucknow Super Giants' and year < 2022) or \
               (team == 'Sunrisers Hyderabad' and year < 2013):
                continue
                
            # Mark banned teams
            if year in banned_teams and team in banned_teams[year]:
                team_entry = {
                    'team': team,
                    'team_code': team_codes[team],
                    'team_color': team_colors[team],
                    'season': year,
                    'matches_played': 0,
                    'wins': 0,
                    'losses': 0,
                    'points': 0,
                    'nrr': 0,
                    'title_winner': False,
                    'banned': True
                }
            else:
                matches_played = np.random.randint(14, 17)
                wins = np.random.randint(4, matches_played)
                
                team_entry = {
                    'team': team,
                    'team_code': team_codes[team],
                    'team_color': team_colors[team],
                    'season': year,
                    'matches_played': matches_played,
                    'wins': wins,
                    'losses': matches_played - wins,
                    'points': wins * 2,
                    'nrr': np.random.uniform(-2, 2),
                    'title_winner': False,
                    'banned': False
                }
            
            team_performance.append(team_entry)
    
    # Set title winners
    # Actual IPL winners by year
    winners_by_year = {
        2008: 'Rajasthan Royals',
        2009: 'Deccan Chargers',  # Now Sunrisers Hyderabad
        2010: 'Chennai Super Kings',
        2011: 'Chennai Super Kings',
        2012: 'Kolkata Knight Riders',
        2013: 'Mumbai Indians',
        2014: 'Kolkata Knight Riders',
        2015: 'Mumbai Indians',
        2016: 'Sunrisers Hyderabad',
        2017: 'Mumbai Indians',
        2018: 'Chennai Super Kings',
        2019: 'Mumbai Indians',
        2020: 'Mumbai Indians',
        2021: 'Chennai Super Kings',
        2022: 'Gujarat Titans',
        2023: 'Chennai Super Kings',
        2024: 'Kolkata Knight Riders'  # Latest winner
    }
    
    # Set the actual winners
    for entry in team_performance:
        year = entry['season']
        if year in winners_by_year and entry['team'] == winners_by_year[year]:
            entry['title_winner'] = True
    
    team_perf_df = pd.DataFrame(team_performance)
    
    return matches_df, players_df, team_perf_df, team_codes, team_colors, banned_teams

# Load the data
matches_df, players_df, team_perf_df, team_codes, team_colors, banned_teams = load_data()

# Create title with custom HTML
st.markdown('<h1 class="main-header">🏏 IPL Dashboard (2008-2024)</h1>', unsafe_allow_html=True)
st.markdown('<p style="text-align: center; margin-bottom: 30px;">Comprehensive analysis of Indian Premier League cricket tournament data</p>', unsafe_allow_html=True)

# Sidebar for filtering
st.sidebar.header("Filters")

# Year selection
years = sorted(matches_df['season'].unique())
selected_year = st.sidebar.selectbox("Select Year", years, index=len(years)-1)

# Get teams for the selected year (including banned teams)
all_teams_in_year = sorted(team_perf_df[team_perf_df['season'] == selected_year]['team'].unique())
selected_team = st.sidebar.selectbox("Select Team", ["All Teams"] + list(all_teams_in_year))

# Extra tabs for advanced features
analysis_type = st.sidebar.radio(
    "Analysis Type",
    ["Season Overview", "Team Analysis", "Player Stats", "Historical Trends"]
)

# Check if the selected team is banned for the selected year
is_team_banned = False
if selected_year in banned_teams and selected_team in banned_teams[selected_year]:
    is_team_banned = True

# Apply filters
filtered_matches = matches_df[matches_df['season'] == selected_year]
if selected_team != "All Teams":
    filtered_matches = filtered_matches[(filtered_matches['team1'] == selected_team) | 
                                       (filtered_matches['team2'] == selected_team)]

filtered_players = players_df[players_df['season'] == selected_year]
if selected_team != "All Teams":
    filtered_players = filtered_players[filtered_players['team'] == selected_team]

filtered_team_perf = team_perf_df[team_perf_df['season'] == selected_year]
if selected_team != "All Teams":
    filtered_team_perf = filtered_team_perf[filtered_team_perf['team'] == selected_team]

# Get active teams (not banned) for the selected year
active_teams_in_year = [team for team in all_teams_in_year if team not in banned_teams.get(selected_year, [])]

# Determine champion for the selected year
champion_team = team_perf_df[(team_perf_df['season'] == selected_year) & 
                            (team_perf_df['title_winner'] == True)]
champion = champion_team['team_code'].values[0] if not champion_team.empty else "N/A"

# Determine team with most wins (only from active teams)
active_team_perf = filtered_team_perf[~filtered_team_perf['banned']]
most_wins_team = active_team_perf.loc[active_team_perf['wins'].idxmax()] if not active_team_perf.empty else None
most_wins = f"{most_wins_team['team_code']} ({most_wins_team['wins']})" if most_wins_team is not None else "N/A"

# Show banned notice if the selected team is banned for the selected year
if is_team_banned:
    st.markdown(f"""
    <div class="banned-notice">
        {selected_team} (CSK) was banned from IPL in {selected_year} due to spot-fixing scandal
    </div>
    """, unsafe_allow_html=True)

# Display different content based on analysis type
if analysis_type == "Season Overview":
    # Key metrics in a row
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-value">{len(filtered_matches)}</div>
            <div class="metric-label">Matches</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-value">{len(active_teams_in_year)}</div>
            <div class="metric-label">Teams</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-value">{champion}</div>
            <div class="metric-label">Champion</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-value">{most_wins}</div>
            <div class="metric-label">Most Wins</div>
        </div>
        """, unsafe_allow_html=True)
    
    # Team Performance Charts
    st.markdown(f"<h2 class='sub-header'>Team Performance in {selected_year}</h2>", unsafe_allow_html=True)
    
    # Only show active teams in charts
    active_team_perf = filtered_team_perf[~filtered_team_perf['banned']]
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Team Wins Chart
        fig_wins = px.bar(
            active_team_perf,
            x='team_code',
            y='wins',
            color='team',
            color_discrete_map={team: color for team, color in zip(active_team_perf['team'], active_team_perf['team_color'])},
            title=f"Team Wins in {selected_year}",
            labels={'team_code': 'Team', 'wins': 'Number of Wins'}
        )
        fig_wins.update_layout(showlegend=False, height=400)
        st.plotly_chart(fig_wins, use_container_width=True)
    
    with col2:
        # Net Run Rate Chart
        fig_nrr = px.bar(
            active_team_perf,
            x='team_code',
            y='nrr',
            color='nrr',
            color_continuous_scale=['red', 'yellow', 'green'],
            title=f"Net Run Rate in {selected_year}",
            labels={'team_code': 'Team', 'nrr': 'Net Run Rate'}
        )
        fig_nrr.update_layout(showlegend=False, height=400)
        st.plotly_chart(fig_nrr, use_container_width=True)
    
    # Match Analysis Charts - only if there are matches
    if not filtered_matches.empty:
        st.markdown(f"<h2 class='sub-header'>Match Analysis</h2>", unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        
        with col1:
            # Toss Impact Chart
            toss_win_match_win = filtered_matches[filtered_matches['toss_winner'] == filtered_matches['winner']].shape[0]
            toss_win_match_lose = filtered_matches.shape[0] - toss_win_match_win
            
            toss_data = pd.DataFrame({
                'Result': ['Won Toss & Match', 'Won Toss, Lost Match'],
                'Count': [toss_win_match_win, toss_win_match_lose]
            })
            
            fig_toss = px.pie(
                toss_data,
                values='Count',
                names='Result',
                title='Toss Impact on Match Outcome',
                color_discrete_sequence=['#36a2eb', '#ffce56']
            )
            fig_toss.update_traces(textposition='inside', textinfo='percent+label')
            st.plotly_chart(fig_toss, use_container_width=True)
        
        with col2:
            # Win Type Chart
            win_by_runs = filtered_matches[filtered_matches['win_by_runs'] > 0].shape[0]
            win_by_wickets = filtered_matches[filtered_matches['win_by_wickets'] > 0].shape[0]
            
            win_type_data = pd.DataFrame({
                'Win Type': ['Win by Runs (Batting 1st)', 'Win by Wickets (Batting 2nd)'],
                'Count': [win_by_runs, win_by_wickets]
            })
            
            fig_win_type = px.pie(
                win_type_data,
                values='Count',
                names='Win Type',
                title='Win Type Distribution',
                color_discrete_sequence=['#4bc0c0', '#9966ff']
            )
            fig_win_type.update_traces(textposition='inside', textinfo='percent+label')
            st.plotly_chart(fig_win_type, use_container_width=True)
    
    # Points Table
    st.markdown(f"<h2 class='sub-header'>Points Table - {selected_year}</h2>", unsafe_allow_html=True)
    
    # Sort teams by points then NRR (for active teams)
    active_points_table = active_team_perf.sort_values(by=['points', 'nrr'], ascending=[False, False])
    
    # Format the table
    points_table_display = active_points_table[['team', 'matches_played', 'wins', 'losses', 'points', 'nrr']]
    points_table_display = points_table_display.rename(columns={
        'team': 'Team',
        'matches_played': 'P',
        'wins': 'W',
        'losses': 'L',
        'points': 'Points',
        'nrr': 'NRR'
    })
    
    # Format NRR to 2 decimal places
    points_table_display['NRR'] = points_table_display['NRR'].round(2)
    
    # Display the table with styling
    st.dataframe(
        points_table_display,
        column_config={
            "Team": st.column_config.TextColumn("Team", width="medium"),
            "P": st.column_config.NumberColumn("P", width="small"),
            "W": st.column_config.NumberColumn("W", width="small"),
            "L": st.column_config.NumberColumn("L", width="small"),
            "Points": st.column_config.NumberColumn("Points", width="small", format="%d"),
            "NRR": st.column_config.NumberColumn("NRR", width="small", format="%0.2f")
        },
        use_container_width=True,
        hide_index=True
    )
    
    # Display banned teams if any
    banned_teams_in_year = [team for team in all_teams_in_year if team in banned_teams.get(selected_year, [])]
    if banned_teams_in_year:
        banned_teams_str = ", ".join(banned_teams_in_year)
        st.markdown(f"""
        <div class="banned-notice" style="margin-top: 20px;">
            Teams banned in {selected_year}: {banned_teams_str}
        </div>
        """, unsafe_allow_html=True)

elif analysis_type == "Team Analysis":
    if selected_team == "All Teams":
        st.markdown("<h2 class='sub-header'>Please select a specific team for detailed analysis</h2>", unsafe_allow_html=True)
    elif is_team_banned:
        st.markdown(f"<h2 class='sub-header'>{selected_team} Analysis ({selected_year})</h2>", unsafe_allow_html=True)
        
        st.markdown(f"""
        <div class="banned-notice">
            {selected_team} was banned from IPL in {selected_year} due to spot-fixing scandal.
            No matches or player statistics are available for this period.
        </div>
        
        <div style="padding: 20px; background-color: #f8f9fa; border-radius: 10px; margin-top: 20px;">
            <h3 style="color: #0066cb;">Ban Details:</h3>
            <p> Chennai Super Kings (CSK) and Rajasthan Royals (RR) were suspended from the IPL for two years (2016-2017) 
            following the IPL betting scandal. The suspension was imposed by the Supreme Court-appointed Justice Lodha Committee. </p>
            
            <p> During this period, some of the players from these teams were drafted to other franchises through a special player draft, 
            while two new teams, Rising Pune Supergiant and Gujarat Lions, were introduced as temporary replacements for the duration of the ban. </p>
            
            <p> CSK returned to IPL in 2018 and went on to win the tournament that year, demonstrating their resilience and strength as a franchise. </p>
        </div>
        """, unsafe_allow_html=True)
        
        # Display a historical overview
        st.markdown("<h3 style='margin-top: 30px;'>Historical Performance Overview</h3>", unsafe_allow_html=True)
        
        # Get team performance across all years except banned years
        team_history = team_perf_df[(team_perf_df['team'] == selected_team) & (~team_perf_df['banned'])]
        
        if not team_history.empty:
            # Wins per year
            fig_wins_history = px.line(
                team_history,
                x='season',
                y='wins',
                markers=True,
                title=f"{selected_team} - Wins Over the Years",
                labels={'season': 'Year', 'wins': 'Number of Wins'}
            )
            fig_wins_history.update_traces(line_color=team_history.iloc[0]['team_color'])
            
            # Add vertical lines for banned years
            for year in banned_teams:
                if selected_team in banned_teams[year]:
                    fig_wins_history.add_vline(x=year, line_width=2, line_dash="dash", line_color="red")
            
            st.plotly_chart(fig_wins_history, use_container_width=True)
            
    else:
        st.markdown(f"<h2 class='sub-header'>{selected_team} Analysis ({selected_year})</h2>", unsafe_allow_html=True)
        
        # Team performance metrics
        team_perf = filtered_team_perf.iloc[0] if not filtered_team_perf.empty else None
        
        if team_perf is not None:
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                st.markdown(f"""
                <div class="metric-card">
                    <div class="metric-value">{team_perf['matches_played']}</div>
                    <div class="metric-label">Matches Played</div>
                </div>
                """, unsafe_allow_html=True)
            
            with col2:
                st.markdown(f"""
                <div class="metric-card">
                    <div class="metric-value">{team_perf['wins']}</div>
                    <div class="metric-label">Wins</div>
                </div>
                """, unsafe_allow_html=True)
            
            with col3:
                st.markdown(f"""
                <div class="metric-card">
                    <div class="metric-value">{team_perf['losses']}</div>
                    <div class="metric-label">Losses</div>
                </div>
                """, unsafe_allow_html=True)
            
            with col4:
                st.markdown(f"""
                <div class="metric-card">
                    <div class="metric-value">{team_perf['nrr']:.2f}</div>
                    <div class="metric-label">Net Run Rate</div>
                </div>
                """, unsafe_allow_html=True)
        
        # Team matches
        st.markdown(f"<h3 class='sub-header'>Matches</h3>", unsafe_allow_html=True)
        
        team_matches = filtered_matches[(filtered_matches['team1'] == selected_team) | 
                                       (filtered_matches['team2'] == selected_team)]
        
        match_results = []
        
        for _, match in team_matches.iterrows():
            if match['winner'] == selected_team:
                result = 'Won'
                opponent = match['team1'] if match['team2'] == selected_team else match['team2']
                if match['win_by_runs'] > 0:
                    details = f"Won by {match['win_by_runs']} runs"
                else:
                    details = f"Won by {match['win_by_wickets']} wickets"
            else:
                result = 'Lost'
                opponent = match['winner']
                if match['win_by_runs'] > 0 and match['team1'] == selected_team:
                    details = f"Lost by {match['win_by_runs']} runs"
                elif match['win_by_wickets'] > 0 and match['team2'] == selected_team:
                    details = f"Lost by {match['win_by_wickets']} wickets"
                else:
                    details = "Lost"
            
            match_results.append({
                'Date': match['date'],
                'Opponent': opponent,
                'Result': result,
                'Details': details,
                'Venue': match['venue']
            })
        
        match_results_df = pd.DataFrame(match_results)
        
        if not match_results_df.empty:
            st.dataframe(
                match_results_df,
                use_container_width=True,
                hide_index=True
            )
        else:
            st.info(f"No matches found for {selected_team} in {selected_year}")
        
        # Top Players
        st.markdown(f"<h3 class='sub-header'>Top Players</h3>", unsafe_allow_html=True)
        
        # Top batsmen
        team_batsmen = filtered_players[filtered_players['player_type'] == 'Batsman'].sort_values(by='runs', ascending=False).head(5)
        
        if not team_batsmen.empty:
            st.markdown("<h4>Top Batsmen</h4>", unsafe_allow_html=True)
            
            batsmen_cols = st.columns(len(team_batsmen))
            
            for i, (_, batsman) in enumerate(team_batsmen.iterrows()):
                with batsmen_cols[i]:
                    st.markdown(f"""
                    <div class="metric-card">
                        <div style="font-weight: 600; margin-bottom: 10px;">{batsman['player_name']}</div>
                        <div class="metric-value">{batsman['runs']}</div>
                        <div class="metric-label">Runs</div>
                        <div style="margin-top: 10px; font-size: 0.9rem;">
                            <span style="display: block;">Avg: {batsman['avg']:.2f}</span>
                            <span style="display: block;">SR: {batsman['strike_rate']:.2f}</span>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
        
        # Top bowlers
        team_bowlers = filtered_players[filtered_players['player_type'] == 'Bowler'].sort_values(by='wickets', ascending=False).head(5)
        
        if not team_bowlers.empty:
            st.markdown("<h4>Top Bowlers</h4>", unsafe_allow_html=True)
            
            bowlers_cols = st.columns(len(team_bowlers))
            
            for i, (_, bowler) in enumerate(team_bowlers.iterrows()):
                with bowlers_cols[i]:
                    st.markdown(f"""
                    <div class="metric-card">
                        <div style="font-weight: 600; margin-bottom: 10px;">{bowler['player_name']}</div>
                        <div class="metric-value">{bowler['wickets']}</div>
                        <div class="metric-label">Wickets</div>
                        <div style="margin-top: 10px; font-size: 0.9rem;">
                            <span style="display: block;">Economy: {bowler['economy']:.2f}</span>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)

elif analysis_type == "Player Stats":
    st.markdown("<h2 class='sub-header'>Player Statistics</h2>", unsafe_allow_html=True)
    
    # Filter options
    player_type = st.radio("Player Type", ["All", "Batsman", "Bowler"], horizontal=True)
    
    # Apply filter
    if player_type != "All":
        filtered_players = filtered_players[filtered_players['player_type'] == player_type]
    
    # Sort options
    if player_type == "Bowler":
        sort_by = st.selectbox("Sort By", ["wickets", "economy"])
        ascending = st.checkbox("Ascending Order", False)
        sorted_players = filtered_players.sort_values(by=sort_by, ascending=ascending)
    else:
        sort_by = st.selectbox("Sort By", ["runs", "avg", "strike_rate"])
        ascending = st.checkbox("Ascending Order", False)
        sorted_players = filtered_players.sort_values(by=sort_by, ascending=ascending)
    
    # Display top players table
    if not sorted_players.empty:
        if player_type == "Bowler":
            display_cols = ['player_name', 'team_code', 'matches', 'wickets', 'economy']
            renamed_cols = {
                'player_name': 'Player',
                'team_code': 'Team',
                'matches': 'Matches',
                'wickets': 'Wickets',
                'economy': 'Economy'
            }
        else:
            display_cols = ['player_name', 'team_code', 'matches', 'runs', 'avg', 'strike_rate', 'fifties', 'hundreds']
            renamed_cols = {
                'player_name': 'Player',
                'team_code': 'Team',
                'matches': 'Matches',
                'runs': 'Runs',
                'avg': 'Average',
                'strike_rate': 'Strike Rate',
                'fifties': '50s',
                'hundreds': '100s'
            }
        
        # Format floating point numbers
        for col in ['avg', 'strike_rate', 'economy']:
            if col in sorted_players.columns:
                sorted_players[col] = sorted_players[col].round(2)
        
        display_df = sorted_players[display_cols].rename(columns=renamed_cols)
        
        st.dataframe(
            display_df,
            use_container_width=True,
            hide_index=True
        )
        
        # Visualize top players
        top_n = min(10, len(sorted_players))
        top_players = sorted_players.head(top_n)
        
        if player_type == "Bowler":
            fig = px.bar(
                top_players,
                x='player_name',
                y='wickets',
                color='team_code',
                title=f"Top {top_n} Bowlers by Wickets",
                labels={'player_name': 'Player', 'wickets': 'Wickets', 'team_code': 'Team'}
            )
            st.plotly_chart(fig, use_container_width=True)
            
            # Economy rate comparison
            fig_economy = px.scatter(
                top_players,
                x='wickets',
                y='economy',
                color='team_code',
                size='matches',
                hover_name='player_name',
                title=f"Wickets vs Economy Rate",
                labels={'wickets': 'Wickets', 'economy': 'Economy Rate', 'matches': 'Matches Played'}
            )
            st.plotly_chart(fig_economy, use_container_width=True)
        else:
            fig = px.bar(
                top_players,
                x='player_name',
                y='runs',
                color='team_code',
                title=f"Top {top_n} Batsmen by Runs",
                labels={'player_name': 'Player', 'runs': 'Runs', 'team_code': 'Team'}
            )
            st.plotly_chart(fig, use_container_width=True)
            
            # Strike rate vs Average scatter plot
            fig_sr_avg = px.scatter(
                top_players,
                x='avg',
                y='strike_rate',
                color='team_code',
                size='runs',
                hover_name='player_name',
                title=f"Average vs Strike Rate",
                labels={'avg': 'Batting Average', 'strike_rate': 'Strike Rate', 'runs': 'Total Runs'}
            )
            st.plotly_chart(fig_sr_avg, use_container_width=True)
    else:
        st.info("No player data available for the selected filters")

elif analysis_type == "Historical Trends":
    st.markdown("<h2 class='sub-header'>Historical Trends</h2>", unsafe_allow_html=True)
    
    # Select type of historical analysis
    trend_type = st.radio(
        "Select Trend Analysis",
        ["Team Performance Over Years", "Champions Timeline", "Win Type Trends", "Toss Impact Trends"],
        horizontal=True
    )
    
    if trend_type == "Team Performance Over Years":
        if selected_team != "All Teams":
            # Get team performance over years
            team_history = team_perf_df[team_perf_df['team'] == selected_team]
            
            if not team_history.empty:
                st.markdown(f"<h3>Performance of {selected_team} Over the Years</h3>", unsafe_allow_html=True)
                
                # Wins per year
                fig_wins_history = px.line(
                    team_history,
                    x='season',
                    y='wins',
                    markers=True,
                    title=f"{selected_team} - Wins Over the Years",
                    labels={'season': 'Year', 'wins': 'Number of Wins'}
                )
                fig_wins_history.update_traces(line_color=team_history.iloc[0]['team_color'])
                st.plotly_chart(fig_wins_history, use_container_width=True)
                
                # Points per year
                fig_points_history = px.line(
                    team_history,
                    x='season',
                    y='points',
                    markers=True,
                    title=f"{selected_team} - Points Over the Years",
                    labels={'season': 'Year', 'points': 'Points'}
                )
                fig_points_history.update_traces(line_color=team_history.iloc[0]['team_color'])
                st.plotly_chart(fig_points_history, use_container_width=True)
                
                # Win percentage
                team_history['win_percentage'] = (team_history['wins'] / team_history['matches_played'] * 100).round(2)
                
                fig_win_pct = px.bar(
                    team_history,
                    x='season',
                    y='win_percentage',
                    title=f"{selected_team} - Win Percentage Over the Years",
                    labels={'season': 'Year', 'win_percentage': 'Win Percentage (%)'}
                )
                fig_win_pct.update_traces(marker_color=team_history.iloc[0]['team_color'])
                st.plotly_chart(fig_win_pct, use_container_width=True)
                
                # Display years when they were champions
                champion_years = team_history[team_history['title_winner'] == True]['season'].tolist()
                
                if champion_years:
                    champions_text = ", ".join([str(year) for year in champion_years])
                    st.markdown(f"""
                    <div style="background-color: gold; padding: 15px; border-radius: 10px; text-align: center; margin-top: 20px;">
                        <h3 style="margin: 0; color: #333;">{selected_team} were Champions in: {champions_text}</h3>
                    </div>
                    """, unsafe_allow_html=True)
                else:
                    st.markdown(f"""
                    <div style="background-color: #f8f9fa; padding: 15px; border-radius: 10px; text-align: center; margin-top: 20px;">
                        <h3 style="margin: 0; color: #666;">{selected_team} have not won any IPL title yet</h3>
                    </div>
                    """, unsafe_allow_html=True)
            else:
                st.info(f"No historical data available for {selected_team}")
        else:
            # Compare all teams
            # Aggregate team performance by year
            team_yearly_performance = team_perf_df.groupby(['team', 'team_code', 'team_color'])['wins'].mean().reset_index()
            team_yearly_performance['avg_wins'] = team_yearly_performance['wins'].round(2)
            
            # Sort by average wins
            team_yearly_performance = team_yearly_performance.sort_values(by='avg_wins', ascending=False)
            
            # Bar chart of average wins
            fig_avg_wins = px.bar(
                team_yearly_performance,
                x='team_code',
                y='avg_wins',
                color='team',
                color_discrete_map={team: color for team, color in zip(team_yearly_performance['team'], team_yearly_performance['team_color'])},
                title="Average Wins per Season (All Teams)",
                labels={'team_code': 'Team', 'avg_wins': 'Average Wins per Season'}
            )
            fig_avg_wins.update_layout(showlegend=False)
            st.plotly_chart(fig_avg_wins, use_container_width=True)
            
            # Count total championships by team
            champions = team_perf_df[team_perf_df['title_winner'] == True]
            champions_count = champions.groupby(['team', 'team_code', 'team_color']).size().reset_index(name='titles')
            champions_count = champions_count.sort_values(by='titles', ascending=False)
            
            # Bar chart of total championships
            fig_titles = px.bar(
                champions_count,
                x='team_code',
                y='titles',
                color='team',
                color_discrete_map={team: color for team, color in zip(champions_count['team'], champions_count['team_color'])},
                title="Total IPL Titles Won (2008-2024)",
                labels={'team_code': 'Team', 'titles': 'Number of Titles'}
            )
            fig_titles.update_layout(showlegend=False)
            st.plotly_chart(fig_titles, use_container_width=True)
            
            # Win percentage heatmap across years
            team_win_pct = team_perf_df.copy()
            team_win_pct['win_percentage'] = (team_win_pct['wins'] / team_win_pct['matches_played'] * 100).round(2)
            
            # Pivot for heatmap
            win_pct_pivot = team_win_pct.pivot_table(
                index='team_code',
                columns='season',
                values='win_percentage',
                aggfunc='mean'
            ).fillna(0)
            
            # Filter years for better visualization
            selected_years = list(range(2008, 2025, 2))  # Show every other year to avoid crowding
            win_pct_pivot = win_pct_pivot[win_pct_pivot.columns.intersection(selected_years)]
            
            fig_heatmap = px.imshow(
                win_pct_pivot,
                labels=dict(x="Season", y="Team", color="Win %"),
                x=win_pct_pivot.columns,
                y=win_pct_pivot.index,
                color_continuous_scale='RdYlGn',
                title="Team Win Percentage by Season"
            )
            fig_heatmap.update_layout(height=500)
            st.plotly_chart(fig_heatmap, use_container_width=True)
    
    elif trend_type == "Champions Timeline":
        # Champions through the years
        champions = team_perf_df[team_perf_df['title_winner'] == True][['season', 'team', 'team_code', 'team_color']]
        champions = champions.sort_values(by='season')
        
        fig_timeline = px.line(
            champions,
            x='season',
            y=[1] * len(champions),  # Constant value to create a straight line
            markers=True,
            hover_name='team',
            title="IPL Champions Timeline (2008-2024)",
            labels={'season': 'Year'}
        )
        
        # Remove y-axis and its grid lines
        fig_timeline.update_layout(
            yaxis={'visible': False, 'showgrid': False},
            height=400
        )
        
        # Add team names as annotations
        for i, row in champions.iterrows():
            fig_timeline.add_annotation(
                x=row['season'],
                y=1,
                text=row['team_code'],
                showarrow=True,
                arrowhead=0,
                yshift=20,
                font={'color': row['team_color'], 'size': 14, 'weight': 'bold'}
            )
        
        st.plotly_chart(fig_timeline, use_container_width=True)
        
        # Count championships by team
        champions_count = champions.groupby(['team', 'team_code', 'team_color']).size().reset_index(name='titles')
        champions_count = champions_count.sort_values(by='titles', ascending=False)
        
        # Create donut chart
        fig_donut = px.pie(
            champions_count,
            values='titles',
            names='team',
            color='team',
            hole=0.4,
            color_discrete_map={team: color for team, color in zip(champions_count['team'], champions_count['team_color'])},
            title="Distribution of IPL Championships by Team"
        )
        fig_donut.update_traces(textinfo='percent+label')
        
        st.plotly_chart(fig_donut, use_container_width=True)
        
        # Champions stats table
        st.markdown("<h3>IPL Champions Details</h3>", unsafe_allow_html=True)
        
        # Merge with team performance to get more details
        champions_detailed = champions.merge(
            team_perf_df[['season', 'team', 'matches_played', 'wins', 'losses', 'nrr']],
            on=['season', 'team']
        )
        
        # Calculate win percentage
        champions_detailed['win_percentage'] = (champions_detailed['wins'] / champions_detailed['matches_played'] * 100).round(2)
        
        # Format the table for display
        champions_display = champions_detailed[['season', 'team', 'wins', 'losses', 'win_percentage', 'nrr']]
        champions_display = champions_display.rename(columns={
            'season': 'Year',
            'team': 'Champion',
            'wins': 'Wins',
            'losses': 'Losses',
            'win_percentage': 'Win %',
            'nrr': 'NRR'
        })
        
        champions_display['NRR'] = champions_display['NRR'].round(2)
        
        st.dataframe(
            champions_display,
            use_container_width=True,
            hide_index=True
        )
    
    elif trend_type == "Win Type Trends":
        # Analyze win type trends over the years
        
        # Calculate win types by year
        win_types_by_year = []
        
        for year in sorted(matches_df['season'].unique()):
            year_matches = matches_df[matches_df['season'] == year]
            win_by_runs = year_matches[year_matches['win_by_runs'] > 0].shape[0]
            win_by_wickets = year_matches[year_matches['win_by_wickets'] > 0].shape[0]
            
            win_types_by_year.append({
                'season': year,
                'win_by_runs': win_by_runs,
                'win_by_wickets': win_by_wickets,
                'total_matches': len(year_matches)
            })
        
        win_types_df = pd.DataFrame(win_types_by_year)
        
        # Calculate percentages
        win_types_df['pct_win_by_runs'] = (win_types_df['win_by_runs'] / win_types_df['total_matches'] * 100).round(2)
        win_types_df['pct_win_by_wickets'] = (win_types_df['win_by_wickets'] / win_types_df['total_matches'] * 100).round(2)
        
        # Area chart showing win type distribution over years
        fig_win_types = go.Figure()
        
        fig_win_types.add_trace(go.Scatter(
            x=win_types_df['season'],
            y=win_types_df['pct_win_by_runs'],
            mode='lines',
            stackgroup='one',
            name='Win by Runs (Batting 1st)',
            line=dict(color='rgba(75, 192, 192, 0.8)')
        ))
        
        fig_win_types.add_trace(go.Scatter(
            x=win_types_df['season'],
            y=win_types_df['pct_win_by_wickets'],
            mode='lines',
            stackgroup='one',
            name='Win by Wickets (Batting 2nd)',
            line=dict(color='rgba(153, 102, 255, 0.8)')
        ))
        
        fig_win_types.update_layout(
            title="Win Type Distribution Over Years",
            xaxis_title="Season",
            yaxis_title="Percentage of Matches (%)",
            yaxis_range=[0, 100],
            hovermode="x unified",
            height=500
        )
        
        st.plotly_chart(fig_win_types, use_container_width=True)
        
        # Analyze margin of victory trends
        
        # For wins by runs
        runs_victories = matches_df[matches_df['win_by_runs'] > 0]
        
        if not runs_victories.empty:
            runs_by_year = runs_victories.groupby('season')['win_by_runs'].agg(['mean', 'median', 'max']).reset_index()
            runs_by_year['mean'] = runs_by_year['mean'].round(2)
            
            fig_runs_margin = px.line(
                runs_by_year,
                x='season',
                y=['mean', 'median', 'max'],
                markers=True,
                title="Margin of Victory (Runs) Trends",
                labels={
                    'season': 'Year',
                    'value': 'Runs',
                    'variable': 'Statistic'
                }
            )
            
            st.plotly_chart(fig_runs_margin, use_container_width=True)
        
        # For wins by wickets
        wickets_victories = matches_df[matches_df['win_by_wickets'] > 0]
        
        if not wickets_victories.empty:
            wickets_by_year = wickets_victories.groupby('season')['win_by_wickets'].agg(['mean', 'median', 'max']).reset_index()
            wickets_by_year['mean'] = wickets_by_year['mean'].round(2)
            
            fig_wickets_margin = px.line(
                wickets_by_year,
                x='season',
                y=['mean', 'median', 'max'],
                markers=True,
                title="Margin of Victory (Wickets) Trends",
                labels={
                    'season': 'Year',
                    'value': 'Wickets',
                    'variable': 'Statistic'
                }
            )
            
            st.plotly_chart(fig_wickets_margin, use_container_width=True)
    
    elif trend_type == "Toss Impact Trends":
        # Analyze toss impact over the years
        
        toss_impact_by_year = []
        
        for year in sorted(matches_df['season'].unique()):
            year_matches = matches_df[matches_df['season'] == year]
            toss_win_match_win = year_matches[year_matches['toss_winner'] == year_matches['winner']].shape[0]
            toss_win_match_lose = year_matches.shape[0] - toss_win_match_win
            
            toss_impact_by_year.append({
                'season': year,
                'toss_win_match_win': toss_win_match_win,
                'toss_win_match_lose': toss_win_match_lose,
                'total_matches': len(year_matches),
                'toss_win_match_win_pct': round(toss_win_match_win / len(year_matches) * 100, 2)

            })
        
        toss_impact_df = pd.DataFrame(toss_impact_by_year)
        
        # Line chart for toss impact over years
        fig_toss_impact = go.Figure()
        
        fig_toss_impact.add_trace(go.Scatter(
            x=toss_impact_df['season'],
            y=toss_impact_df['toss_win_match_win_pct'],
            mode='lines+markers',
            name='Toss Winners Won Match (%)',
            line=dict(color='rgba(54, 162, 235, 0.8)', width=3)
        ))
        
        # Add a 50% reference line
        fig_toss_impact.add_shape(
            type="line",
            x0=min(toss_impact_df['season']),
            y0=50,
            x1=max(toss_impact_df['season']),
            y1=50,
            line=dict(color="gray", width=1, dash="dash")
        )
        
        fig_toss_impact.update_layout(
            title="Toss Impact on Match Outcome Over the Years",
            xaxis_title="Season",
            yaxis_title="Percentage of Matches (%)",
            yaxis_range=[0, 100],
            height=500,
            hovermode="x"
        )
        
        st.plotly_chart(fig_toss_impact, use_container_width=True)
        
        # Analyze toss decision trends (bat or field)
        toss_decisions = matches_df.groupby(['season', 'toss_decision']).size().reset_index(name='count')
        
        # Pivot for stacked bar chart
        toss_decisions_pivot = toss_decisions.pivot_table(
            index='season',
            columns='toss_decision',
            values='count',
            aggfunc='sum'
        ).fillna(0).reset_index()
        
        # Calculate percentages
        if 'bat' in toss_decisions_pivot.columns and 'field' in toss_decisions_pivot.columns:
            total_by_season = toss_decisions_pivot['bat'] + toss_decisions_pivot['field']
            toss_decisions_pivot['bat_pct'] = (toss_decisions_pivot['bat'] / total_by_season * 100).round(2)
            toss_decisions_pivot['field_pct'] = (toss_decisions_pivot['field'] / total_by_season * 100).round(2)
            
            # Stacked area chart for toss decisions
            fig_toss_decisions = go.Figure()
            
            fig_toss_decisions.add_trace(go.Scatter(
                x=toss_decisions_pivot['season'],
                y=toss_decisions_pivot['bat_pct'],
                mode='lines',
                stackgroup='one',
                name='Chose to Bat',
                line=dict(color='rgba(255, 99, 132, 0.8)')
            ))
            
            fig_toss_decisions.add_trace(go.Scatter(
                x=toss_decisions_pivot['season'],
                y=toss_decisions_pivot['field_pct'],
                mode='lines',
                stackgroup='one',
                name='Chose to Field',
                line=dict(color='rgba(54, 162, 235, 0.8)')
            ))
            
            fig_toss_decisions.update_layout(
                title="Toss Decision Trends Over the Years",
                xaxis_title="Season",
                yaxis_title="Percentage of Decisions (%)",
                yaxis_range=[0, 100],
                hovermode="x unified",
                height=500
            )
            
            st.plotly_chart(fig_toss_decisions, use_container_width=True)
            
            # Analyze which toss decision led to more wins
            toss_decision_outcome = []
            
            for year in sorted(matches_df['season'].unique()):
                year_matches = matches_df[matches_df['season'] == year]
                
                # Toss winner chose to bat
                bat_matches = year_matches[year_matches['toss_decision'] == 'bat']
                bat_win = bat_matches[bat_matches['toss_winner'] == bat_matches['winner']].shape[0]
                bat_total = len(bat_matches)
                bat_win_pct = round(bat_win / bat_total * 100, 2) if bat_total > 0 else 0

                
                # Toss winner chose to field
                field_matches = year_matches[year_matches['toss_decision'] == 'field']
                field_win = field_matches[field_matches['toss_winner'] == field_matches['winner']].shape[0]
                field_total = len(field_matches)
                field_win_pct = round(field_win / field_total * 100,2) if field_total > 0 else 0
                
                toss_decision_outcome.append({
                    'season': year,
                    'bat_win_pct': bat_win_pct,
                    'field_win_pct': field_win_pct
                })
            
            toss_outcome_df = pd.DataFrame(toss_decision_outcome)
            
            # Line chart comparing success rates of toss decisions
            fig_toss_success = go.Figure()
            
            fig_toss_success.add_trace(go.Scatter(
                x=toss_outcome_df['season'],
                y=toss_outcome_df['bat_win_pct'],
                mode='lines+markers',
                name='Success Rate - Chose to Bat',
                line=dict(color='rgba(255, 99, 132, 0.8)', width=2)
            ))
            
            fig_toss_success.add_trace(go.Scatter(
                x=toss_outcome_df['season'],
                y=toss_outcome_df['field_win_pct'],
                mode='lines+markers',
                name='Success Rate - Chose to Field',
                line=dict(color='rgba(54, 162, 235, 0.8)', width=2)
            ))
            
            fig_toss_success.update_layout(
                title="Success Rate of Toss Decisions Over the Years",
                xaxis_title="Season",
                yaxis_title="Win Percentage (%)",
                yaxis_range=[0, 100],
                height=500,
                hovermode="x"
            )
            
            st.plotly_chart(fig_toss_success, use_container_width=True)

# Footer
st.markdown("""
<div style="text-align: center; margin-top: 30px; padding-top: 20px; border-top: 1px solid #f0f2f6;">
    <p>IPL Dashboard (2008-2024) | Created with Streamlit</p>
</div>
""", unsafe_allow_html=True)
