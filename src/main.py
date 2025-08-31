from scraper.fetch import get_driver_profile_html
from scraper.parse import parse_driver_events
import json
from pathlib import Path
from datetime import datetime

def main():
    # Generate timestamp once per page
    timestamp = datetime.now().strftime("%d_%m_%Y")
    
    # Read driver names from a file
    driver_file = Path("config") / "driver_list.txt"
    driver_list = [line.strip() for line in driver_file.read_text(encoding="utf-8").splitlines() if line.strip()]

    # Define output directory
    out_path = Path("data/processed") / f"all_events.json"
    out_path.parent.mkdir(parents=True, exist_ok=True)

    # Load existing JSON if it exists
    if out_path.exists():
        with open(out_path, "r", encoding="utf-8") as f:
            main_events_json = json.load(f)
        # Ensure all driver entries are lists for backward compatibility
        for driver, driver_data in main_events_json.items():
            if isinstance(driver_data, dict):
                main_events_json[driver] = [driver_data]
    else:
        main_events_json = {}

    new_data = {}
    for driver in driver_list:
        html = get_driver_profile_html(driver)
        events = parse_driver_events(html)
        print(f"Scraped {len(events)} events for {driver}.")
        new_data[driver] = {"date": timestamp, "events": events}
    
    # Append only if today's timestamp is not already present
    for driver, driver_data in new_data.items():
        if driver not in main_events_json:
            main_events_json[driver] = []
        # Check if today's date is already recorded
        if not any(entry.get("date") == timestamp for entry in main_events_json[driver]):
            main_events_json[driver].append(driver_data)
        else:
            print(f"Data for {driver} on {timestamp} already exists; skipping.")

    # Save back to JSON
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(main_events_json, f, indent=2, ensure_ascii=False)


if __name__ == "__main__":
    main()
