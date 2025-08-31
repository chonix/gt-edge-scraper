from scraper.fetch import get_driver_profile_html
from scraper.parse import parse_driver_events
import json
from pathlib import Path
from datetime import datetime

def main():
    # Generate timestamp once per page
    timestamp = datetime.now().strftime("%d_%m_%Y")
    
    driver = "chonix123"
    html = get_driver_profile_html(driver)
    events = parse_driver_events(html)

    out_path = Path("data/processed") / f"{driver}_events.json"
    out_path.parent.mkdir(parents=True, exist_ok=True)

    with open(out_path, "w", encoding="utf-8") as f:
        json.dump({"driver": driver, "date": timestamp, "events": events}, f, indent=2, ensure_ascii=False)

    print(f"Saved {len(events)} events for {driver}.")

if __name__ == "__main__":
    main()
