import time
from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page()
    page.goto("http://localhost:8080/index.html")
    page.wait_for_timeout(1000)

    # Click tab 2 (圖層控制)
    page.click("text=圖層控制")
    page.wait_for_timeout(500)

    # Click bottom layer tab (底圖)
    page.click("#lTab-bottom")
    page.wait_for_timeout(500)

    print("Page loaded successfully")
    browser.close()
