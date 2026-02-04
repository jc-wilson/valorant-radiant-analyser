from leaderboard_puuids_retriever import LeaderboardPUUIDsRetriever
from local_api import LockfileHandler
import requests
import json
import asyncio
import aiohttp

class RetrieveMatchData:
    def __init__(self):
        self.match_ids = []
        self.match_id_list = []
        self.version_data = requests.get("https://valorant-api.com/v1/version").json()
        self.match_data = []
        self.used_match_id = []
        self.modified_header = {}

    def retrieve_matches(self):
        handler = LeaderboardPUUIDsRetriever()
        handler.retrieve_puuids()

        local_api_handler = LockfileHandler()
        local_api_handler.lockfile_data_function()

        self.modified_header = local_api_handler.match_id_header
        self.modified_header["X-Riot-ClientVersion"] = self.version_data["data"]["riotClientVersion"]
        print(f"Headers Configured. Starting Async Fetch...")

        asyncio.run(self._retrieve_matches_async(handler.puuids))

    async def _retrieve_matches_async(self, puuids):
        sem = asyncio.Semaphore(10)

        async def fetch_with_retry(session, url):
            async with sem:
                while True:
                    try:
                        async with session.get(url, headers=self.modified_header) as response:
                            if response.status == 429:
                                try:
                                    retry_seconds = int(response.headers.get("Retry-After", 10))
                                except (ValueError, TypeError):
                                    retry_seconds = 10

                                print(f"Rate limit hit. Retrying in {retry_seconds}s...")
                                await asyncio.sleep(retry_seconds)
                                continue

                            if response.status == 200:
                                try:
                                    return await response.json()
                                except aiohttp.ContentTypeError:
                                    return None

                            return None

                    except aiohttp.ClientError as e:
                        print(f"Connection Error: {e}")
                        return None

        async with aiohttp.ClientSession() as session:

            print(f"Fetching match history for {len(puuids)} players...")
            history_tasks = []
            for puuid in puuids:
                url = f"https://pd.eu.a.pvp.net/match-history/v1/history/{puuid}?startIndex=0&endIndex=15&queue=competitive"
                history_tasks.append(fetch_with_retry(session, url))

            history_results = await asyncio.gather(*history_tasks)

            for player_history in history_results:
                if player_history and "History" in player_history:
                    for match in player_history["History"]:
                        self.match_id_list.append(match["MatchID"])

            unique_matches = list(set(self.match_id_list))
            matches_to_fetch = [m for m in unique_matches if m not in self.used_match_id]

            print(f"Fetching details for {len(matches_to_fetch)} matches...")

            match_tasks = []
            for match_id in matches_to_fetch:
                url = f"https://pd.eu.a.pvp.net/match-details/v1/matches/{match_id}"
                match_tasks.append(fetch_with_retry(session, url))

            if match_tasks:
                match_results = await asyncio.gather(*match_tasks)

                # Store successful results
                for match_id, result in zip(matches_to_fetch, match_results):
                    if result:
                        self.match_data.append(result)
                        self.used_match_id.append(match_id)

            print("Saving data to match_data.json...")
            with open("match_data.json", "w", encoding="utf-8") as f:
                json.dump(self.match_data, f, indent=2)
            print("Done.")