predictions = {
  "Liverpool": 1,
  "Chelsea": 2,
  "Manchester City": 3,
  "Arsenal": 4,
  "Aston Villa": 5,
  "Newcastle United": 6,
  "Manchester United": 7,
  "West Ham United": 8,
  "Tottenham Hotspur": 9,
  "Crystal Palace": 10,
  "Nottingham Forest": 11,
  "Brighton": 12,
  "Fulham": 13,
  "Everton": 14,
  "Burnley": 15,
  "Bournemouth": 16,
  "Sunderland": 17,
  "Brentford": 18,
  "Leeds": 19,
  "Wolves": 20
}

from dotenv import load_dotenv
import os

load_dotenv()

API_KEY = os.getenv("FOOTBALL_API_KEY")

#Import requests library
import requests

# Define the API endpoint for the premier league standings
API_URL = "https://api.football-data.org/v4/competitions/PL/standings"

# Add authentication token (API key) to the request headers
headers = {"X-Auth-Token": API_KEY}

# Get respones to API headpoint with headers
response = requests.get(API_URL, headers=headers)

# Convert response (which is in JSON) into a python dictionary
data = response.json()

# to see the keys of the dictionary e.g "area, competition, season, standings"
#print(data.keys())
#print(data)

# Extract the standings from the api dictionary
standings = data["standings"][0]["table"]
#print(standings)

#Create a dictionary of actual positions
actual_positions = {}

for entry in standings:
    team_name = entry["team"]["name"]
    position = entry["position"]
    actual_positions[team_name] = position

#print(actual_positions)

# Map prediction names to the API's official team names
name_mapping = {
    "Liverpool": "Liverpool FC",
    "Chelsea": "Chelsea FC",
    "Manchester City": "Manchester City FC",
    "Arsenal": "Arsenal FC",
    "Aston Villa": "Aston Villa FC",
    "Newcastle United": "Newcastle United FC",
    "Manchester United": "Manchester United FC",
    "West Ham United": "West Ham United FC",
    "Tottenham Hotspur": "Tottenham Hotspur FC",  
    "Crystal Palace": "Crystal Palace FC",
    "Nottingham Forest": "Nottingham Forest FC",
    "Brighton": "Brighton & Hove Albion FC",       
    "Fulham": "Fulham FC",
    "Everton": "Everton FC",
    "Burnley": "Burnley FC",
    "Bournemouth": "AFC Bournemouth",            
    "Brentford": "Brentford FC",
    "Wolves": "Wolverhampton Wanderers FC",
    "Sunderland": "Sunderland AFC",
    "Leeds": "Leeds United FC"
}

# Create a normalized actual positions dictionary (using prediction names)
normalized_actual_positions = {}
for pred_name, api_name in name_mapping.items():
    if api_name in actual_positions:
        normalized_actual_positions[pred_name] = actual_positions[api_name]

#print(normalized_actual_positions)

# Compute difference between actual position and predicted position
# Positive number means the team is higher than predicted, negative means lower
position_diff = {}
for team, pred_pos in predictions.items(): # loop through my predictions dictionary and their positions
    actual_pos = normalized_actual_positions.get(team)  # get the team's actual position from the normalized api standings
    diff = pred_pos - actual_pos    # compute the difference in predicted positions and actual positions
    position_diff[team] = diff  # add the team + the difference to the differences dictionary

# Print the differences
#print("Position differences (Actual - Predicted):")
#for team, diff in position_diff.items():
   # print(f"{team}: {diff}")


final = {}

for team, pred_pos in predictions.items():
    actual_pos = normalized_actual_positions.get(team)
    diff = pred_pos - actual_pos
    if diff > 0:
        str_diff = "+" + str(diff)
    else:
        str_diff = str(diff)
    final[team] = str(actual_pos) + " " + "(" + str_diff + ")"

for team, typeout in final.items():
    print(f"{team}: {typeout}")

import pandas as pd
import matplotlib.pyplot as plt

# Convert final dictionary into a DataFrame
df = pd.DataFrame({
    "Team": list(final.keys()),
    "Actual": [normalized_actual_positions[t] for t in final.keys()],
    "Predicted": [predictions[t] for t in final.keys()]
})

###### SCATTER PLOT #########
"""plt.figure(figsize=(8,8))
plt.scatter(df["Predicted"], df["Actual"])

for i, team in enumerate(df["Team"]):
    plt.text(df["Predicted"][i]+0.1, df["Actual"][i], team, fontsize=9)

plt.plot([1,20],[1,20], 'r--')  # diagonal = perfect prediction
plt.xlabel("Predicted Position")
plt.ylabel("Actual Position")
plt.title("Predicted vs Actual Premier League Positions")
plt.gca().invert_yaxis()
plt.show()
"""
gw_predscores = []
score = 0
for team, pos in predictions.items():
    actual_pos = normalized_actual_positions.get(team)
    diff = pos - actual_pos
    print(diff**2)
    score = score + diff**2

print(score)
gw_predscores.append(score)
print(gw_predscores)