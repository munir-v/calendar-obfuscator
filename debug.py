#!/usr/bin/env python3

import os
import logging
from datetime import datetime, timedelta
import pytz
import caldav

import constants  # Ensure this contains your ICLOUD_USERNAME, ICLOUD_PASSWORD, etc.

logging.getLogger("root").setLevel(logging.ERROR)

# --- Global Constants and Configuration ---
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

ICLOUD_CALENDARS_TO_SKIP = constants.ICLOUD_CALENDARS_TO_SKIP
ICLOUD_USERNAME = constants.ICLOUD_USERNAME
ICLOUD_PASSWORD = constants.ICLOUD_PASSWORD

DAYS_TO_SYNC = 31

ICLOUD_CLIENT = caldav.DAVClient(
    url="https://caldav.icloud.com/",
    username=ICLOUD_USERNAME,
    password=ICLOUD_PASSWORD,
)


def fetch_icloud_events():
    """
    Fetch events from iCloud calendars (skipping those in the skip list), within the next
    DAYS_TO_SYNC days. Returns a dictionary mapping calendar names to lists of iCloud Event objects.
    """
    calendars_events = {}
    principal = ICLOUD_CLIENT.principal()
    calendars = principal.calendars()

    now_utc = datetime.now(pytz.timezone("UTC"))
    future_date = now_utc + timedelta(days=DAYS_TO_SYNC)

    print("Fetching iCloud events...")
    for calendar in calendars:
        # Skip reminders and calendars in the skip list
        if calendar.name.startswith("Reminders"):
            continue
        if calendar.name in ICLOUD_CALENDARS_TO_SKIP:
            print(f"Skipping iCloud calendar: {calendar.name}")
            continue

        try:
            events = calendar.date_search(start=now_utc, end=future_date)
            print(f"Processing calendar '{calendar.name}': Retrieved {len(events)} events.")
            for event in events:
                event.load()  # make sure the event data is loaded
            calendars_events[calendar.name] = events
        except Exception as e:
            print(f"Could not fetch events for calendar {calendar.name}: {e}")
            continue

    return calendars_events


def is_recurring_event(event):
    """
    Determine if the event has a recurrence rule (RRULE).
    """
    vevent = event.vobject_instance.vevent
    return hasattr(vevent, "rrule")


def main():
    """
    Main script entry point: Fetches events from iCloud, filters them to only recurring events,
    and prints their raw ICS data.
    """
    calendars_events = fetch_icloud_events()

    for calendar_name, events in calendars_events.items():
        print(f"\n=== Calendar: {calendar_name} ===")
        recurring_events = [evt for evt in events if is_recurring_event(evt)]

        if not recurring_events:
            print("No recurring events found in this calendar.")
            continue

        # Print full ICS data for each recurring event
        for event in recurring_events:
            # The entire ICS data is stored in `event.vobject_instance`
            # Converting that to a string will print the complete vCalendar structure
            ics_data = str(event.vobject_instance)
            print("\n--- Full ICS Data for Recurring Event ---")
            print(ics_data)
            print("-----------------------------------------")

if __name__ == "__main__":
    main()
