import pandas as pd
import datetime
from turtle import pd

# assume the votes and persons tables are stored as pandas dataframes called /n
# "votes" and "persons"
vote = pd.DataFrame({"ID":[253,254,255,256,257],
                    "voting_date":[2022-10-29, 11:54:15, 2022-10-29, 11:55:22, 2022-10-29,11:56:53, 2022-10-29, 11:58:23, 2022-10-29,12:13:00],
                     "chosen_person": [03400110, 03400360, 03402059, 03400565, 03400436],
                     "voter": [00108901, 00108901, 00199990, 00108941, 00108941],
                     "message": ["Vote 1", "vote 2", "Vote 3", "Vote 4", "Vote 5"],
                     "valid": [1, 0, 1, 1, 1],
                     "quality": ["entrepreneur", "entrepreneur", "partner", "developer", "developer"]})

persons = pd.DataFrame({"ID":[00108901, 00108941, 00199990, 01100003],
                        "Status": ["Active","Active", "Inactiv", "Active"],
                        "Short_Nam": ["person.one", "person.two", "person.three", "person.four"],
                        "First_Name": ["Person", "Person", "Person", "Person"],
                        "Last_Name": ["One", "Two", "Two", "Four"],
                        "Email_Address": ["person.one@gfk.com", "person.two@gfk.com", "person.three@gfk.com", "person.four@gfk.com"],
                        "Locatie": ["Germany", "France", "Brazil", "Hong Kong"]})
  

# join the tables on the ID field
merged = pd.merge(vote, persons, on="ID")

# filter out invalid votes
valid_votes = merged[merged["valid"] == 1]

# count the number of votes for each person in each location
vote_counts = valid_votes.groupby(["chosen_person", "Locatie", "quality"]).size().reset_index(name="number")

# create a new column for the period (month, quarter, or year)
vote_counts["period"] = vote_counts.apply(lambda row: datetime.datetime.strptime(row["voting_date"], "%Y-%m-%d %H:%M:%S").strftime("%B"), axis=1)
vote_counts["period"] = vote_counts.apply(lambda row: "Q" + str((int(datetime.datetime.strptime(row["voting_date"], "%Y-%m-%d %H:%M:%S").month) - 1) // 3 + 1), axis=1)
vote_counts["period"] = vote_counts.apply(lambda row: datetime.datetime.strptime(row["voting_date"], "%Y-%m-%d %H:%M:%S").strftime("%Y"), axis=1)

# group by location, period, and name to get the final report
final_report = vote_counts.groupby(["quality", "Locatie", "period", "Last_Name"]).sum().reset_index()

# format the output in the desired format and print to console
for index, row in final_report.iterrows():
    print(row["quality"], row["number"], row["Locatie"], row["period"], row["Last_Name"])
