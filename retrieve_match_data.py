from leaderboard_puuids_retriever import LeaderboardPUUIDsRetriever
from local_api import LockfileHandler
import requests
import json

class RetrieveMatchData:
    def __init__(self):
        self.match_ids = []
        self.match_id_list = []
        self.version_data = requests.get("https://valorant-api.com/v1/version").json()
        self.match_data = []

    def retrieve_matches(self):
        handler = LeaderboardPUUIDsRetriever()
        handler.retrieve_puuids()
        local_api_handler = LockfileHandler()
        local_api_handler.lockfile_data_function()

        self.modified_header = local_api_handler.match_id_header
        self.modified_header["X-Riot-ClientVersion"] = self.version_data["data"]["riotClientVersion"]
        print(local_api_handler.match_id_header)

        for puuid in handler.puuids:
            response = requests.get(f"https://pd.eu.a.pvp.net/match-history/v1/history/{puuid}?startIndex=0&endIndex=5&queue=competitive",
                         headers=local_api_handler.match_id_header).json()
            self.match_ids.append(response)

        for player in self.match_ids:
            if "History" in player:
                print(player)
                for match in player["History"]:
                    self.match_id_list.append(match["MatchID"])
            else:
                pass

        for match_id in self.match_id_list:
            self.match_data.append(requests.get(f"https://pd.eu.a.pvp.net/match-details/v1/matches/{match_id}",
                                                headers=local_api_handler.match_id_header).json())

        with open("match_data.json", "w", encoding="utf-8") as f:
            json.dump(self.match_data, f, indent=2)
