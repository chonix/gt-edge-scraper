from playwright.sync_api import sync_playwright

def get_driver_profile_html(driver_name: str) -> str:
    url = f"https://www.dg-edge.com/players/{driver_name}"
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        page.goto(url)
        # Wait for the events container
        page.wait_for_selector("#pills-events", timeout=20000)

        # Wait for at least one .result inside it
        page.wait_for_selector("#pills-events .result", timeout=20000)

        # Optional: ensure network is idle
        page.wait_for_load_state("networkidle")

        html = page.content()
        browser.close()
    return html