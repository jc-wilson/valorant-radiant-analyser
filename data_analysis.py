from retrieve_match_data import RetrieveMatchData
from leaderboard_puuids_retriever import LeaderboardPUUIDsRetriever
from collections import Counter

import json

class DataAnalysis:
    def __init__(self):
        self.server_data = []
        self.match_length_data = []
        self.average_match_length = None
        self.shortest_match = None
        self.longest_match = None
        self.kda_acs = []
        self.total_kills = 0
        self.total_deaths = 0
        self.total_assists = 0
        self.total_score = 0
        self.total_rounds_played = 0
        self.most_kills = 0
        self.least_kills = 0
        self.average_kills = 0
        self.most_deaths = 0
        self.least_deaths = 0
        self.average_deaths = 0
        self.most_assists = 0
        self.least_assists = 0
        self.average_assists = 0
        self.most_kd = 0
        self.least_kd = 0
        self.average_kd = 0
        self.most_acs = 0
        self.least_acs = 0
        self.average_acs = 0

    def data_analysis(self):
        # handler = RetrieveMatchData()
        # handler.retrieve_matches()

        puuid_handler = LeaderboardPUUIDsRetriever()
        puuid_handler.retrieve_puuids()

        with open("match_data.json") as a:
            self.match_data = json.load(a)

        def server_func():
            for match in self.match_data:
                self.server_data.append(match["matchInfo"]["gamePodId"])

                for index, server in enumerate(self.server_data):
                    self.server_data[index] = self.server_data[index][29:-2].capitalize()

                self.server_data = str(Counter(self.server_data))
                self.server_data = self.server_data.replace("Counter", "")

        def match_length_func():
            for match in self.match_data:
                self.match_length_data.append(match["matchInfo"]["gameLengthMillis"])
            self.average_match_length = f"{round(sum(self.match_length_data) / len(self.match_length_data) / 1000 / 60, 2)} minutes"
            print(f"average match: {self.average_match_length}")

            longest_match = 0
            shortest_match = 999999999999
            for match in self.match_length_data:
                if match < shortest_match:
                    shortest_match = match
                if match > longest_match:
                    longest_match = match
            self.longest_match = longest_match / 1000 / 60
            print(f"longest match: {round(self.longest_match, 2)} minutes")
            self.shortest_match = shortest_match / 1000 / 60
            print(f"shortest match: {round(self.shortest_match, 2)} minutes")

        def kda_acs_func():
            for puuid in puuid_handler.puuids:
                for match in self.match_data:
                    for player in match["players"]:
                        if player["subject"] == puuid:
                            self.kda_acs.append({
                                'kills': player["stats"]["kills"],
                                'deaths': player["stats"]["deaths"],
                                'assists': player["stats"]["assists"],
                                'score': player["stats"]["score"],
                                'rounds_played': player["stats"]["roundsPlayed"]
                            })

            most_kills = 0
            least_kills = 99
            most_deaths = 0
            least_deaths = 99
            most_assists = 0
            least_assists = 99

            for statline in self.kda_acs:
                self.total_kills += statline['kills']
                self.total_deaths += statline['deaths']
                self.total_assists += statline['assists']
                self.total_score += statline['score']
                self.total_rounds_played += statline['rounds_played']

                if statline['kills'] > most_kills:
                    most_kills = statline['kills']
                if statline['kills'] < least_kills:
                    least_kills = statline['kills']
                if statline['deaths'] > most_deaths:
                    most_deaths = statline['deaths']
                if statline['deaths'] < least_deaths:
                    least_deaths = statline['deaths']
                if statline['assists'] > most_assists:
                    most_assists = statline['assists']
                if statline['assists'] < least_assists:
                    least_assists = statline['assists']

            self.most_kills = most_kills
            self.least_kills = least_kills
            self.most_deaths = most_deaths
            self.least_deaths = least_deaths
            self.most_assists = most_assists
            self.least_assists = least_assists



            self.average_kills = self.total_kills / len(self.kda_acs)
            self.average_deaths = self.total_deaths / len(self.kda_acs)
            self.average_assists = self.total_assists / len(self.kda_acs)
            self.average_kd = self.total_kills / self.total_deaths
            self.average_acs = self.total_score / self.total_rounds_played

            print(f"most kills: {self.most_kills}")
            print(f"average kills: {round(self.average_kills, 2)}")
            print(f"least kills: {self.least_kills}")
            print("--------------------------------------")
            print(f"most deaths: {self.most_deaths}")
            print(f"average deaths: {round(self.average_deaths, 2)}")
            print(f"least deaths: {self.least_deaths}")
            print("--------------------------------------")
            print(f"most assists: {self.most_assists}")
            print(f"average assists: {round(self.average_assists, 2)}")
            print(f"least assists: {self.least_assists}")
            print("--------------------------------------")
            print(f"average k/d: {round(self.average_kd, 2)}")
            print(f"average acs: {round(self.average_acs, 0)}")


        kda_acs_func()
        print("--------------------------------------")
        match_length_func()