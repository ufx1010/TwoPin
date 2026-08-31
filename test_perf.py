import time
from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page()
    page.goto("http://localhost:8080/index.html")
    page.wait_for_timeout(1000)

    # Measure export time with default kaleido (SVG with 800 density x 10 = 8000 elements)
    t0 = time.time()
    page.evaluate("exportImage(3)")
    page.wait_for_selector("#loading", state="hidden", timeout=60000)
    print(f"Export time with kaleido SVG: {time.time() - t0:.2f}s")

    # Now clear kaleido layer
    page.evaluate("clearCurrentLayer()")
    page.wait_for_timeout(200)

    t0 = time.time()
    page.evaluate("exportImage(3)")
    page.wait_for_selector("#loading", state="hidden", timeout=60000)
    print(f"Export time without kaleido SVG: {time.time() - t0:.2f}s")

    browser.close()
