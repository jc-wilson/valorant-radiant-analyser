from retrieve_match_data import RetrieveMatchData
from leaderboard_puuids_retriever import LeaderboardPUUIDsRetriever
from utils import UUIDHandler, TimeHandler, RoundingHandler
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
        self.kill_list = []
        self.death_list = []
        self.assist_list = []
        self.acs_list = []
        self.rounds_played_list = []
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
        self.most_acs_rounded = 0
        self.least_acs = 0
        self.average_acs = 0
        self.least_rounds = 0
        self.average_rounds = 0
        self.most_rounds = 0
        self.unique_matches = 0
        self.match_times = []
        self.acs_list_rounded = []
        self.server_count = {
            'Frankfurt': 0,
            'London': 0,
            'Paris': 0,
            'Madrid': 0,
            'Stockholm': 0,
            'Warsaw': 0,
            'Istanbul': 0,
            'Bahrain': 0
        }
        self.agent_count = {
            'Astra': 0, 'Fade': 0, 'Brimstone': 0, 'Gekko': 0, 'Iso': 0,
            'Waylay': 0, 'Harbor': 0, 'Veto': 0, 'Sage': 0, 'KAY_O': 0,
            'Raze': 0, 'Neon': 0, 'Deadlock': 0, 'Phoenix': 0, 'Vyse': 0,
            'Omen': 0, 'Yoru': 0, 'Breach': 0, 'Viper': 0, 'Reyna': 0,
            'Jett': 0, 'Skye': 0, 'Chamber': 0, 'Cypher': 0, 'Sova': 0,
            'Clove': 0, 'Killjoy': 0, 'Tejo': 0
        }
        self.role_count = {
            'Controller': 0,
            'Sentinel': 0,
            'Initiator': 0,
            'Duelist': 0
        }
        self.party_size = {
            'Solo': 0,
            'Duo': 0
        }
        self.weapon_choice = {
            "Classic": 0,
            "Bandit": 0,
            "Shorty": 0,
            "Frenzy": 0,
            "Ghost": 0,
            "Sheriff": 0,
            "Stinger": 0,
            "Spectre": 0,
            "Bucky": 0,
            "Judge": 0,
            "Bulldog": 0,
            "Guardian": 0,
            "Phantom": 0,
            "Vandal": 0,
            "Marshal": 0,
            "Outlaw": 0,
            "Operator": 0,
            "Ares": 0,
            "Odin": 0,
            "Knife": 0
        }
        self.weapon_kill_count = {
            "Classic": 0,
            "Bandit": 0,
            "Shorty": 0,
            "Frenzy": 0,
            "Ghost": 0,
            "Sheriff": 0,
            "Stinger": 0,
            "Spectre": 0,
            "Bucky": 0,
            "Judge": 0,
            "Bulldog": 0,
            "Guardian": 0,
            "Phantom": 0,
            "Vandal": 0,
            "Marshal": 0,
            "Outlaw": 0,
            "Operator": 0,
            "Ares": 0,
            "Odin": 0,
            "Knife": 0
        }
        self.armor_choice = {
            "No Armor": 0,
            "Light Armor": 0,
            "Regen Shield": 0,
            "Heavy Armor": 0
        }
        self.vandal_phantom = {
            'Vandal': 0,
            'Phantom': 0
        }
        self.pistol_round_choice = {
            "Classic": 0,
            "Bandit": 0,
            "Shorty": 0,
            "Frenzy": 0,
            "Ghost": 0,
            "Sheriff": 0
        }

    def data_analysis(self):
        # handler = RetrieveMatchData()
        # handler.retrieve_matches()

        uuid_handler = UUIDHandler()
        uuid_handler.agent_uuid_function()
        uuid_handler.weapon_uuid_function()
        uuid_handler.armor_uuid_function()

        time_handler = TimeHandler()

        rounding_handler = RoundingHandler()

        with open("match_data.json") as a:
            self.match_data = json.load(a)

        with open("puuid_data.json") as a:
            self.puuid_data = json.load(a)

        self.unique_matches = len(self.match_data)
        print(f"Unique matches: {self.unique_matches}")

        def server_func():
            for puuid in self.puuid_data:
                for match in self.match_data:
                    for player in match["players"]:
                        if player["subject"] == puuid:
                            self.server_data.append(match["matchInfo"]["gamePodId"])

            for server in self.server_data:
                self.server_count[server[29:-2].capitalize()] += 1


        def match_time_length_func():
            for puuid in self.puuid_data:
                for match in self.match_data:
                    for player in match["players"]:
                        if player["subject"] == puuid:
                            self.match_length_data.append(int(round(time_handler.ms_to_minutes(match["matchInfo"]["gameLengthMillis"]), 0)))
                            self.match_times.append(time_handler.ms_to_24hr(match["matchInfo"]["gameStartMillis"]))

            self.average_match_length = sum(self.match_length_data) / len(self.match_length_data)

            print(f"average match: {self.average_match_length}")

            longest_match = 0
            shortest_match = 999999999999
            for match in self.match_length_data:
                if match < shortest_match:
                    shortest_match = match
                if match > longest_match:
                    longest_match = match
            self.longest_match = int(round(longest_match, 0))
            print(self.longest_match)
            print(f"longest match: {self.longest_match} minutes")
            self.shortest_match = int(round(shortest_match, 0))
            print(self.shortest_match)
            print(f"shortest match: {self.shortest_match} minutes")

        def kda_acs_func():
            for puuid in self.puuid_data:
                for match in self.match_data:
                    for player in match["players"]:
                        if player["subject"] == puuid:
                            self.kda_acs.append({
                                'kills': player["stats"]["kills"],
                                'deaths': player["stats"]["deaths"],
                                'assists': player["stats"]["assists"],
                                'score': player["stats"]["score"],
                                'rounds_played': match["teams"][0]["roundsPlayed"]
                            })

            most_kills = 0
            least_kills = 99
            most_deaths = 0
            least_deaths = 99
            most_assists = 0
            least_assists = 99
            most_rounds = 0
            least_rounds = 99
            most_acs_rounded = 0
            least_acs_rounded = 999

            for statline in self.kda_acs:
                self.total_kills += statline['kills']
                self.total_deaths += statline['deaths']
                self.total_assists += statline['assists']
                self.total_score += statline['score']
                self.total_rounds_played += statline['rounds_played']

                self.kill_list.append(statline['kills'])
                self.death_list.append(statline['deaths'])
                self.assist_list.append(statline['assists'])
                self.acs_list.append(statline['score'] / statline['rounds_played'])
                self.acs_list_rounded.append(rounding_handler.round_acs(statline['score'] / statline['rounds_played']))
                self.rounds_played_list.append(statline['rounds_played'])

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
                if statline['rounds_played'] > most_rounds:
                    most_rounds = statline['rounds_played']
                if statline['rounds_played'] < least_rounds:
                    least_rounds = statline['rounds_played']
                if rounding_handler.round_acs(statline['score'] / statline['rounds_played']) > most_acs_rounded:
                    most_acs_rounded = rounding_handler.round_acs(statline['score'] / statline['rounds_played'])

            self.most_kills = most_kills
            self.least_kills = least_kills
            self.most_deaths = most_deaths
            self.least_deaths = least_deaths
            self.most_assists = most_assists
            self.least_assists = least_assists
            self.most_rounds = most_rounds
            self.least_rounds = least_rounds
            self.most_acs_rounded = most_acs_rounded



            self.average_kills = self.total_kills / len(self.kda_acs)
            self.average_deaths = self.total_deaths / len(self.kda_acs)
            self.average_assists = self.total_assists / len(self.kda_acs)
            self.average_rounds = self.total_rounds_played / len(self.kda_acs)
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
            print(f"average rounds: {round(self.average_rounds, 0)}")

        def agent_func():
            for puuid in self.puuid_data:
                for match in self.match_data:
                    for player in match["players"]:
                        if player["subject"] == puuid:
                            if uuid_handler.agent_converter(player["characterId"]) == "KAY/O":
                                self.agent_count["KAY_O"] += 1
                                self.role_count["Initiator"] += 1
                            else:
                                self.agent_count[uuid_handler.agent_converter(player["characterId"])] += 1
                                self.role_count[uuid_handler.agent_role(player["characterId"])] += 1
            print(self.agent_count)

        def party_func():
            for puuid in self.puuid_data:
                for match in self.match_data:
                    for player in match["players"]:
                        if player["subject"] == puuid:
                            party_id = player["partyId"]
                            for players in match["players"]:
                                if players["subject"] != puuid and players["partyId"] == party_id:
                                    self.party_size["Duo"] += 1
            self.party_size["Solo"] = sum(self.agent_count.values()) - self.party_size["Duo"]
            print(self.party_size)

        def loadout_func():
            for puuid in self.puuid_data:
                for match in self.match_data:
                    for player in match["players"]:
                        if player["subject"] == puuid:
                            for round in match["roundResults"]:
                                for players in round["playerStats"]:
                                    if players["subject"] == puuid:
                                        try:
                                            self.weapon_choice[uuid_handler.weapon_converter(players["economy"]["weapon"])] += 1
                                        except KeyError:
                                            continue
                                        if players["economy"]["armor"] == "":
                                            self.armor_choice["No Armor"] += 1
                                        else:
                                            self.armor_choice[uuid_handler.armor_converter(players["economy"]["armor"])] += 1
                                        try:
                                            if players["economy"]["remaining"] + players["economy"]["spent"] == 800:
                                                self.pistol_round_choice[uuid_handler.weapon_converter(players["economy"]["weapon"])] += 1
                                        except KeyError:
                                            continue

                                        for kill in players["kills"]:
                                            if kill["finishingDamage"]["damageType"] == "Melee":
                                                self.weapon_kill_count["Knife"] += 1
                                            elif kill["finishingDamage"]["damageType"] == "Weapon":
                                                try:
                                                    self.weapon_kill_count[uuid_handler.weapon_converter(kill["finishingDamage"]["damageItem"])] += 1
                                                except KeyError:
                                                    continue


            print(self.weapon_choice)
            print(sum(self.pistol_round_choice.values()))
            self.vandal_phantom["Vandal"] = self.weapon_choice["Vandal"]
            self.vandal_phantom["Phantom"] = self.weapon_choice["Phantom"]

        kda_acs_func()
        print("--------------------------------------")
        match_time_length_func()
        print("--------------------------------------")
        server_func()
        print("--------------------------------------")
        agent_func()
        print("--------------------------------------")
        party_func()
        print("--------------------------------------")
        loadout_func()

        print(sum(self.server_count.values()))
        print(sum(self.agent_count.values()))