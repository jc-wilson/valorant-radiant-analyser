from local_api import LockfileHandler
import requests
import json

class LeaderboardPUUIDsRetriever:
    def __init__(self):
        self.puuids = []

    def retrieve_puuids(self):
        lockfile_handler = LockfileHandler()
        lockfile_handler.lockfile_data_function()

        leaderboard = requests.get(f"https://pd.eu.a.pvp.net/mmr/v1/leaderboards/affinity/eu/queue/competitive/season/3ea2b318-423b-cf86-25da-7cbb0eefbe2d?startIndex=0&size=100",
                     headers=lockfile_handler.match_id_header).json()

        for player in leaderboard["Players"]:
            self.puuids.append(player["puuid"])

        print("Saving data to puuid_data.json...")
        with open("puuid_data.json", "w", encoding="utf-8") as f:
            json.dump(self.puuids, f, indent=2)
        print("Done.")



