import tempfile
import pytest
from core.utils.data_loader import NBADataLoader, NBADataLoaderError
#from nba_api.stats.endpoints import leaguegamefinder
import diskcache as dc
from unittest.mock import patch, Mock
import time

def test_caches_response():
    with tempfile.TemporaryDirectory() as temp_dir:
        cache = dc.Cache(temp_dir)
        fake_game_data = {"games": [{"id": 1, "home": "Lakers"}]}

        loader = NBADataLoader(rate_limit=1, cache=cache)

        with patch('core.utils.data_loader.leaguegamefinder') as mock_api:
            mock_api.LeagueGameFinder.return_value.get_dict.return_value = fake_game_data

            result1 = loader.get_games("2024-2025")
            result2 = loader.get_games("2024-2025")

            assert mock_api.LeagueGameFinder.call_count == 1
            assert result1 == result2
        
        cache.close()

def test_respects_rate_limit():
    with tempfile.TemporaryDirectory() as temp_dir:
        cache = dc.Cache(temp_dir)
        loader = NBADataLoader(rate_limit=1, cache=cache)

        with patch('core.utils.data_loader.leaguegamefinder') as mock_api:
            mock_api.LeagueGameFinder.return_value.get_dict.return_value = {"games": []}

            start = time.time()
            result1 = loader.get_games("2023-2024")
            result2 = loader.get_games("2024-2025")
            elapsed = time.time() - start

            assert elapsed >= 1.0
        cache.close()
    
def test_player_stats_endpoint():
    with tempfile.TemporaryDirectory() as temp_dir:
        cache = dc.Cache(temp_dir)
        loader = NBADataLoader(rate_limit=1, cache=cache)

        with patch('core.utils.data_loader.leaguedashplayerstats') as mock_api:
            mock_api.LeagueDashPlayerStats.return_value.get_dict.return_value = {"player": []}

            result1 = loader.get_player_stats("2024-2025")
            result2 = loader.get_player_stats("2024-2025")

            assert mock_api.LeagueDashPlayerStats.call_count == 1
            assert result1 == result2

def test_api_error():
    with tempfile.TemporaryDirectory() as temp_dir:
        cache = dc.Cache(temp_dir)
        loader = NBADataLoader(rate_limit=1, cache=cache)

        with patch('core.utils.data_loader.leaguegamefinder') as mock_api:
            mock_api.LeagueGameFinder.side_effect = ConnectionError("Connection timeout")

            with pytest.raises(NBADataLoaderError):
                loader.get_games("2024-2025") 

def test_cache_expiration():
    with tempfile.TemporaryDirectory() as temp_dir:
        cache = dc.Cache(temp_dir)
        loader = NBADataLoader(rate_limit=1, cache=cache, expire=2)
        with patch('core.utils.data_loader.leaguedashplayerstats') as mock_api:
            mock_api.LeagueDashPlayerStats.return_value.get_dict.return_value = {"player": []}

            result1 = loader.get_player_stats("2024-2025")
            time.sleep(3)
            result2 = loader.get_player_stats("2024-2025")
            assert mock_api.LeagueDashPlayerStats.call_count == 2


