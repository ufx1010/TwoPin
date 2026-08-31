from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page()
    page.goto("http://localhost:8080/index.html")
    page.wait_for_timeout(1000)

    page.click("text=圖層控制")
    page.click("#lTab-bottom")

    file_input = page.locator("#bgInput")

    # Upload 1
    file_input.set_input_files("/tmp/img1.png")
    page.wait_for_timeout(300)

    # Set shape
    page.select_option("#globalVoidShapeSel", "circle")
    page.fill("#range-gHole", "50")
    page.eval_on_selector("#range-gHole", "el => el.dispatchEvent(new Event('input'))")
    page.wait_for_timeout(300)

    # Upload 2
    file_input.set_input_files("/tmp/img1.png")
    page.wait_for_timeout(300)

    print("Inline style attribute:", page.locator("#layer-bottom").evaluate("el => el.getAttribute('style')"))

    browser.close()
