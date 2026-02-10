from nba_api.stats.endpoints import leaguegamefinder, leaguedashplayerstats
import time

class NBADataLoaderError(Exception):
    pass

class NBADataLoader:
    def __init__(self, rate_limit, cache, expire=86400):
        self.rate_limit = rate_limit
        self.cache = cache
        self.last_request_time = 0
        self.expire = expire

    def get_games(self, season):
        cache_key = f"games:{season}"
        if cache_key in self.cache:
            return self.cache[cache_key]

        elapsed_time = time.time() - self.last_request_time
        if elapsed_time < 1:
            time.sleep(1 - elapsed_time)
        
        try:
            response = leaguegamefinder.LeagueGameFinder(season_nullable=season)
        
        except Exception as e:
            raise NBADataLoaderError(f"NBA API problem: {e}")

        self.last_request_time = time.time()
        data = response.get_dict()

        self.cache.set(cache_key, data, expire=self.expire)
        return data
    
    def get_player_stats(self, season):
        cache_key = f"player_stats:{season}"
        if cache_key in self.cache:
            return self.cache[cache_key]

        elapsed_time = time.time() - self.last_request_time
        if elapsed_time < 1:
            time.sleep(1 - elapsed_time)
        response = leaguedashplayerstats.LeagueDashPlayerStats(season=season)
        self.last_request_time = time.time()
        data = response.get_dict()

        self.cache.set(cache_key, data, expire=self.expire)
        return data


