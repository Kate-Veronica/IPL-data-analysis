import pandas as pd
import matplotlib.pyplot as plt

matches = pd.read_csv("matches.csv")
deliveries = pd.read_csv("deliveries.csv")

print(matches.head())
print(deliveries.head())

#----- top score -----

top_score = deliveries.groupby('batter')['batsman_runs'].sum()

top_score = top_score.sort_values(ascending=False)

print('Top 10 Run Scorers in IPL:')
print(top_score.head(10))
print('\n')

# ----- top stries rate -----

total_runs = deliveries.groupby('batter')['batsman_runs'].sum()
total_balls = deliveries.groupby('batter')['ball'].count()

strike_rate = (total_runs / total_balls) * 100

# ----- removing players with few balls ------

balls_filter = total_balls[total_balls > 200].index
strike_rate = strike_rate.loc[balls_filter]

strike_rate = strike_rate.sort_values(ascending=False)

print("Top 10 Strike Rates (Min 200 Balls Faced):")
print(strike_rate.head(10))
print("\n")

# ----- team win rate -----

team1_matches = matches["team1"].value_counts()
team2_matches = matches["team2"].value_counts()

total_matches = team1_matches + team2_matches

total_wins = matches["winner"].value_counts()

win_rate = (total_wins / total_matches) * 100
win_rate = win_rate.sort_values(ascending=False)

print("Team Win Rate (%):")
print(win_rate)
print("\n")

# ----- matches per season ------

season_matches = matches["season"].value_counts().sort_index()

plt.figure()
season_matches.plot(kind="line", marker="o")
plt.title("Number of Matches per Season")
plt.xlabel("Season")
plt.ylabel("Matches Played")
plt.grid(True)
plt.savefig("Matches_Per_Season.png")  
plt.show()

# ------ player performance ------

merged = deliveries.merge(
    matches[["id", "season"]],
    left_on="match_id",
    right_on="id"
)

players = ["V Kohli", "RG Sharma"]

for player in players:
    player_data = merged[merged["batter"] == player]
    runs_per_season = player_data.groupby("season")["batsman_runs"].sum()
    
    plt.figure()
    runs_per_season.plot(kind="line", marker="o")
    plt.title(f"{player} Runs per Season")
    plt.xlabel("Season")
    plt.ylabel("Runs")
    plt.grid(True)
    plt.savefig(f"{player}_Runs_Per_Season.png")
    plt.show()

# ----- visualize results -----

top_score.head(10).to_csv("Top_10_Score.csv")
strike_rate.head(10).to_csv("Top_10_Strike_Rate.csv")
win_rate.to_csv("Team_Win_Rate.csv")

print("CSV Files Exported Successfully!")

# ----- short insights ------

print("\n----- PROJECT INSIGHTS -----")

print(f"Highest Run Scorer: {top_score.idxmax()} "
      f"({top_score.max()} runs)")

print(f"Best Strike Rate: {strike_rate.idxmax()} "
      f"({round(strike_rate.max(),2)})")

print(f"Best Team by Win Rate: {win_rate.idxmax()} "
      f"({round(win_rate.max(),2)}%)")

print("\nProject Completed Successfully!")