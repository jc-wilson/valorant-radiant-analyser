from datetime import datetime
import requests
import json
import math

class UUIDHandler:
    def agent_uuid_function(self):
        try:
            with open("agent_uuids.json") as a:
                self.agent_uuids = json.load(a)
        except FileNotFoundError:
            self.agent_uuid_request = requests.get("https://valorant-api.com/v1/agents").json()
            print("requested agent uuid information from valorant-api.com")

            with open("agent_uuids.json", "w", encoding="utf-8") as f:
                json.dump(self.agent_uuid_request, f, indent=2)

            with open("agent_uuids.json") as a:
                self.agent_uuids = json.load(a)

    def weapon_uuid_function(self):
        try:
            with open ("weapon_uuids.json") as a:
                self.weapon_uuids = json.load(a)
        except FileNotFoundError:
            self.weapon_uuid_request = requests.get("https://valorant-api.com/v1/weapons").json()
            print("requested weapon uuid information from valorant-api.com")

            with open("weapon_uuids.json", "w", encoding="utf-8") as f:
                json.dump(self.weapon_uuid_request, f, indent=2)

            with open("weapon_uuids.json") as a:
                self.weapon_uuids = json.load(a)

    def armor_uuid_function(self):
        self.armor_uuids = requests.get("https://valorant-api.com/v1/gear").json()

    def weapon_converter(self, uuid):
        result = None
        for weapon in self.weapon_uuids["data"]:
            if weapon["uuid"] == uuid.lower():
                result = weapon["displayName"]
                return result
        return result

    def agent_converter(self, uuid):
        result = None
        for agent in self.agent_uuids["data"]:
            if agent["uuid"] == uuid.lower():
                result = agent["displayName"]
                return result
        return result

    def agent_role(self, uuid):
        result = None
        for agent in self.agent_uuids["data"]:
            if agent["uuid"] == uuid.lower():
                result = agent["role"]["displayName"]
                return result
        return result

    def armor_converter(self, uuid):
        result = None
        for armor in self.armor_uuids["data"]:
            if armor["uuid"] == uuid.lower():
                result = armor["displayName"]
                return result
        return result

class TimeHandler:
    def ms_to_24hr(self, ms):
        result = None
        seconds = ms / 1000
        result = datetime.fromtimestamp(seconds)
        return result.strftime("%H:%M")

    def ms_to_minutes(self, ms):
        result = None
        result = ms / 1000 / 60
        return result

class RoundingHandler:
    def round_acs(self, acs):
        result = None
        result = int(math.floor(acs / 20)) * 20
        return result