from datetime import datetime, timezone, timedelta

from timedate_practice import get_activity_status


def test_old_repository_is_stale():
    pushed_at = "2020-01-01T00:00:00Z"

    result = get_activity_status(pushed_at)

    assert result == "Stale"


def test_recent_repository_is_active():
    pushed_at = datetime.now(timezone.utc).strftime(
        "%Y-%m-%dT%H:%M:%SZ"
    )

    result = get_activity_status(pushed_at)

    assert result == "Active"


def test_repository_exactly_180_days_old_is_active():
    pushed_at = (
        datetime.now(timezone.utc) - timedelta(days=180)
    ).strftime("%Y-%m-%dT%H:%M:%SZ")

    result = get_activity_status(pushed_at)

    assert result == "Active"


def test_repository_181_days_old_is_stale():
    pushed_at = (
        datetime.now(timezone.utc) - timedelta(days=181)
    ).strftime("%Y-%m-%dT%H:%M:%SZ")

    result = get_activity_status(pushed_at)

    assert result == "Stale"