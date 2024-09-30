import os
import requests
from icalendar import Calendar
from datetime import datetime, timedelta
import duckdb
import json
import re

# URL of the .ics file
ics_url = "https://calendar.google.com/calendar/ical/c_rqj60henfnuin5klbati6g9kfg%40group.calendar.google.com/public/basic.ics"

# Get old releases
old_versions = duckdb.sql(
    "SELECT version_number FROM '_data/past_releases.csv';"
).fetchall()
old_versions = [v[0] for v in old_versions]

# Download .ics file
response = requests.get(ics_url)
if response.status_code == 200:
    cal = Calendar.from_ical(response.content)
    today = datetime.today().date()

    # Filter upcoming releases
    upcoming_events = []
    for event in cal.walk():
        dtstart = event.get("DTSTART")
        title = event.get("SUMMARY")
        if title is None:
            continue

        version_search = re.search("([0-9]+\\.[0-9]+\\.[0-9])", title)
        if version_search:
            upcoming_version = version_search.group(1)
            if upcoming_version in old_versions:
                continue

        if dtstart is not None and hasattr(dtstart, "dt"):
            dtstart_date = dtstart.dt
            if isinstance(dtstart_date, datetime):
                dtstart_date = dtstart_date.date()
            if dtstart_date >= today:  # Filter only future dates
                end_date = event.get("DTEND")
                upcoming_events.append(
                    {
                        "title": title,
                        "start_date": (
                            dtstart_date.isoformat()
                            if hasattr(dtstart_date, "isoformat")
                            else str(dtstart_date)
                        ),
                    }
                )

    script_dir = os.path.dirname(os.path.abspath(__file__))
    parent_dir = os.path.dirname(script_dir)
    data_dir = os.path.join(parent_dir, "_data")

    # Save the upcoming releases as JSON in _data folder
    data_file_path = os.path.join(data_dir, "upcoming_releases.json")
    with open(data_file_path, "w") as data_file:
        json.dump(upcoming_events, data_file, indent=4)
else:
    print("Error downloading .ics file:", response.status_code)
