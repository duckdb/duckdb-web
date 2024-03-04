import os
import requests
from icalendar import Calendar
from datetime import datetime, timedelta
import json

# URL of the .ics file
ics_url = "https://calendar.google.com/calendar/ical/c_rqj60henfnuin5klbati6g9kfg%40group.calendar.google.com/public/basic.ics"

# Download .ics file
response = requests.get(ics_url)
if response.status_code == 200:

    cal = Calendar.from_ical(response.content)
    today = datetime.today().date()

    # Filter upcoming releases
    upcoming_events = []
    for event in cal.walk():
        dtstart = event.get("DTSTART")
        if dtstart is not None and hasattr(dtstart, "dt"):
            dtstart_date = dtstart.dt
            if isinstance(dtstart_date, datetime):
                dtstart_date = dtstart_date.date()
            if dtstart_date >= today:  # Filter only future dates
                end_date = event.get("DTEND")
                upcoming_events.append(
                    {
                        "title": event.get("SUMMARY"),
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