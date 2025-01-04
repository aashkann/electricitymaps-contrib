from datetime import datetime, timezone

from requests_mock import GET, POST

from electricitymap.contrib.lib.types import ZoneKey
from parsers.KPX import (
    HISTORICAL_PRODUCTION_URL,
    REAL_TIME_URL,
    fetch_consumption,
    fetch_production,
)


def test_fetch_consumption(adapter, session, snapshot):
    with open("parsers/test/mocks/KPX/realtime.html", "rb") as consumption:
        adapter.register_uri(
            GET,
            REAL_TIME_URL,
            content=consumption.read(),
        )
        consumption = fetch_consumption(
            zone_key=ZoneKey("KR"),
            session=session,
        )
    assert snapshot == [
        {
            "datetime": element["datetime"].isoformat(),
            "consumption": element["consumption"],
            "source": element["source"],
            "zoneKey": element["zoneKey"],
            "sourceType": element["sourceType"].value,
        }
        for element in consumption
    ]


def test_production_realtime(adapter, session, snapshot):
    with open("parsers/test/mocks/KPX/realtime.html", "rb") as production:
        adapter.register_uri(
            GET,
            REAL_TIME_URL,
            content=production.read(),
        )
        production = fetch_production(
            zone_key=ZoneKey("KR"),
            session=session,
        )
    assert snapshot == [
        {
            "datetime": element["datetime"].isoformat(),
            "production": element["production"],
            "storage": element["storage"],
            "source": element["source"],
            "zoneKey": element["zoneKey"],
            "sourceType": element["sourceType"].value,
        }
        for element in production
    ]


def test_production_historical(adapter, session, snapshot):
    with open("parsers/test/mocks/KPX/historical.html", "rb") as production:
        adapter.register_uri(
            POST,
            HISTORICAL_PRODUCTION_URL,
            content=production.read(),
        )
        adapter.register_uri(
            GET,
            HISTORICAL_PRODUCTION_URL,
            content=None,
        )
    production = fetch_production(
        zone_key=ZoneKey("KR"),
        session=session,
        target_datetime=datetime(2023, 9, 1, 0, 0, 0, tzinfo=timezone.utc),
    )
    assert snapshot == [
        {
            "datetime": element["datetime"].isoformat(),
            "production": element["production"],
            "storage": element["storage"],
            "source": element["source"],
            "zoneKey": element["zoneKey"],
            "sourceType": element["sourceType"].value,
        }
        for element in production
    ]
