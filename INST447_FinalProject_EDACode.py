import pandas as pd
import nflreadpy as nfl

final_dataset = pd.read_csv("nfl_team_tendencies_2023.csv")

pbp_reg = nfl.load_pbp(seasons=[2023]).to_pandas()
pbp_reg = pbp_reg[pbp_reg["season_type"] == "REG"].copy()

#missing values
print(final_dataset.isnull().sum())

#visualization missing values
import matplotlib.pyplot as plt

missing_counts = final_dataset.isnull().sum()

plt.figure(figsize=(10,5))
missing_counts.plot(kind="bar")
plt.title("Missing Values by Column")
plt.xlabel("Column")
plt.ylabel("Missing Values")
plt.xticks(rotation=45)
plt.show()

#team balance check

#amount of teams in the final dataset
print("Number of teams:", final_dataset["posteam"].nunique())

#rows per team in original regular season dataset
team_play_counts = pbp_reg["posteam"].value_counts()

print(team_play_counts)

plt.figure(figsize=(10,5))
team_play_counts.sort_values().plot(kind="barh")
plt.title("Number of Offensive Plays by Team")
plt.xlabel("Play Count")
plt.ylabel("Team")
plt.show()

#relationship between team success and opportunities 

#red zone opportunities with touchdowns 
x = final_dataset["red_zone_plays"]
y = final_dataset["red_zone_td_rate_pct"]

print("Correlation:", x.corr(y))

plt.figure()
plt.scatter(x, y)
plt.xlabel("Red Zone Plays")
plt.ylabel("Red Zone TD Rate")
plt.title("Red Zone Opportunities vs Touchdown Rate")
plt.show()

#distribution of fourth down attempts
#some teams may be more aggressive because they played from behind more often
plt.figure()
final_dataset["fourth_down_attempts"].hist(bins=16)
plt.title("distribution of Fourth Down Attempts")
plt.xlabel("Attempts")
plt.ylabel("Teams")
plt.show()