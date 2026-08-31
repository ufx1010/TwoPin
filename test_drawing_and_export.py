from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page()
    page.goto("http://localhost:8080/index.html")
    page.wait_for_timeout(1000)

    # Check current kaleido pattern drawing logic and void shape
    print("Default kaleido innerHTML length:", page.evaluate("document.getElementById('layer-kaleido').innerHTML.length"))

    browser.close()
