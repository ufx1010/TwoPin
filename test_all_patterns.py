import time
from playwright.sync_api import sync_playwright

patterns = ['kaleido', 'grid', 'scatter', 'marsText', 'line_straight_arc', 'line_isometric_poly', 'line_flowing_wave', 'line_matrix_grid']

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page()
    page.goto("http://localhost:8080/index.html")
    page.wait_for_timeout(1000)

    page.click("text=圖層控制")

    for pat in patterns:
        page.select_option("#artStyleSel", pat)
        page.wait_for_timeout(200)
        t0 = time.time()
        page.evaluate("exportImage(3)")
        page.wait_for_selector("#loading", state="hidden", timeout=10000)
        dur = time.time() - t0
        print(f"Pattern {pat}: export time {dur:.2f}s")

    browser.close()
