from scraper.fetch import get_driver_profile_html
from scraper.parse import parse_driver_events
import json
from pathlib import Path
from datetime import datetime

def main():
    # Generate timestamp once per page
    timestamp = datetime.now().strftime("%d_%m_%Y")
    
    driver_list = ['chonix123', 'DexPip']
    
    main_events_json = {}

    for driver in driver_list:
        html = get_driver_profile_html(driver)
        events = parse_driver_events(html)

        print(f"Scraped {len(events)} events for {driver}.")

        main_events_json[driver] = {"date": timestamp, "events": events}
    
    out_path = Path("data/processed") / f"all_events.json"
    out_path.parent.mkdir(parents=True, exist_ok=True)

    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(main_events_json, f, indent=2, ensure_ascii=False)


if __name__ == "__main__":
    main()
