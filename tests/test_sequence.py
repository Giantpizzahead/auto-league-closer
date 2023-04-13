import leaguecloser
import time
import pytest


def is_league_running_baseline():
    # Check if League is running
    import psutil
    for proc in psutil.process_iter(['name']):
        if proc.name() == 'LeagueClient.exe':
            return True
    return False


def test_open_league():
    """Tests the open_league function."""
    leaguecloser.open_league()
    # Wait for League to open
    time.sleep(20)
    assert is_league_running_baseline()


def test_is_league_running():
    """Tests the is_league_running function."""
    assert leaguecloser.is_league_running() == is_league_running_baseline()


def test_close_league():
    """Tests the close_league function."""
    if not is_league_running_baseline():
        leaguecloser.open_league()
        time.sleep(20)
    leaguecloser.close_league()
    time.sleep(3)
    assert not is_league_running_baseline()


if __name__ == "__main__":
    pytest.main()
