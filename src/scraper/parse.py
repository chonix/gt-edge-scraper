from bs4 import BeautifulSoup
from datetime import datetime

def parse_driver_events(html: str) -> list[dict]:
    soup = BeautifulSoup(html, "lxml")
    events_div = soup.select_one('#pills-events')
    if not events_div:
        return []


    events = []
    for res in events_div.select(".result"):
        # name = result.get_text(strip=True)  # or refine this based on actual structure
        # Event name and track
        event_name_main = res.select_one(".event-name > div").get_text(strip=True)
        car_type_for_event = res.select_one(".event-name .car-type span").get_text(strip=True)
        track = res.select_one("h4").get_text(strip=True) if res.select_one("h4") else ""
        sub_track = res.select_one("h5").get_text(strip=True) if res.select_one("h5") else ""
        event_name = f"{event_name_main} - {track} - {sub_track}"

        # Lap time
        time = res.select_one(".result-stats .h4").get_text(strip=True)

        # Global result
        global_stat = res.select(".result-stats .result-stat")[0]
        result_global = global_stat.select_one("label").get_text(strip=True)
        position_global = global_stat.select_one("strong").get_text(strip=True)
        delta_global = global_stat.select_one("span").get_text(strip=True)

        # Country result
        country_stat = res.select(".result-stats .result-stat")[1]
        result_country = country_stat.select_one("label").get_text(strip=True)
        position_country = country_stat.select_one("strong").get_text(strip=True)
        delta_country = country_stat.select_one("span").get_text(strip=True)

        # Score impact
        score_impact = res.select_one(".score-impact strong").get_text(strip=True) if res.select_one(".score-impact strong") else None

        # Car
        result_car = res.select_one(".result-car").get_text(strip=False)
        
        events.append({
            "event-name": event_name,
            "car-type-for-event": car_type_for_event,
            "time": time,
            "result_global": result_global,
            "position_global": position_global,
            "delta_global": delta_global,
            "result_country": result_country,
            "position_country": position_country,
            "delta_country": delta_country,
            "score_impact": score_impact,
            "result-car": result_car
    })

    return events
